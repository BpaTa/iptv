#!/usr/bin/env python3
"""
Сборщик кастомного русского IPTV плейлиста.

Что делает:
  1. Скачивает свежий ru.m3u из iptv-org/iptv (это «верхнеуровневый» каталог
     открытых ссылок на российские каналы — обновляется самим сообществом
     несколько раз в неделю).
  2. Парсит его, фильтрует по белому списку из channels.py.
  3. При нескольких кандидатах на один канал выбирает самый качественный
     по `prefer` (1080 > 720 > 576 > 540 > 450 > 360).
  4. Пересобирает в плейлист с нашими категориями и эмодзи.
  5. Прописывает источник EPG (программа передач) в шапку.
  6. Сохраняет два файла:
       playlist.m3u       — основная копия в корне репы
       usb/playlist.m3u   — копия в папке, готовой для флешки

Запуск:  python3 build.py
"""

from __future__ import annotations

import re
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from channels import CATEGORIES, BLOCKLIST_PATTERNS

ROOT = Path(__file__).resolve().parent
SOURCE_URLS = [
    # основной — все российские каналы
    "https://iptv-org.github.io/iptv/countries/ru.m3u",
    # глобальные категории — для премиум-брендов, которых в ru.m3u нет
    # (Cinema, Paramount, BBC Earth, Nat Geo Wild, Stingray, Disney,
    # Nickelodeon, Fox Sports, Premier Sports, BBC News, Al Jazeera,
    # Беларусь 24, CGTN Русский и т.п.).
    "https://iptv-org.github.io/iptv/categories/religious.m3u",
    "https://iptv-org.github.io/iptv/categories/movies.m3u",
    "https://iptv-org.github.io/iptv/categories/news.m3u",
    "https://iptv-org.github.io/iptv/categories/documentary.m3u",
    "https://iptv-org.github.io/iptv/categories/kids.m3u",
    "https://iptv-org.github.io/iptv/categories/music.m3u",
    "https://iptv-org.github.io/iptv/categories/sports.m3u",
    "https://iptv-org.github.io/iptv/categories/entertainment.m3u",
]
EPG_URL = "https://iptvx.one/EPG"
OUT_MAIN = ROOT / "playlist.m3u"
OUT_USB = ROOT / "usb" / "playlist.m3u"
OUT_HOSTS = ROOT / "bypass-hosts.txt"

QUALITY_ORDER = ["1080", "720", "576", "540", "480", "450", "360", "240", ""]
EXTINF_RE = re.compile(r'#EXTINF:-?\d+\s*(.*),([^,]+)$')


@dataclass
class Channel:
    name: str          # отображаемое имя из исходника
    attrs: str         # сырые атрибуты EXTINF (tvg-id, tvg-logo, http-user-agent, ...)
    url: str           # URL потока


def fetch_source() -> str:
    """Скачать и склеить все источники в одну простыню."""
    parts: list[str] = []
    for url in SOURCE_URLS:
        print(f"→ скачиваю: {url}")
        req = urllib.request.Request(url, headers={"User-Agent": "iptv-builder/1.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read().decode("utf-8", errors="replace")
        print(f"  получено {len(data):,} байт")
        parts.append(data)
    return "\n".join(parts)


def parse(playlist: str) -> list[Channel]:
    channels: list[Channel] = []
    extinf: str | None = None
    for raw in playlist.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#EXTINF"):
            extinf = line
        elif line.startswith("#"):
            # любые другие директивы пропускаем (EXTM3U, EXTVLCOPT и т.п.)
            continue
        else:
            if extinf is None:
                continue
            m = EXTINF_RE.match(extinf)
            if not m:
                extinf = None
                continue
            attrs, name = m.group(1).strip(), m.group(2).strip()
            channels.append(Channel(name=name, attrs=attrs, url=line))
            extinf = None
    print(f"  распарсено {len(channels)} каналов")
    return channels


def quality_score(name: str, prefer: str) -> int:
    """Чем меньше — тем лучше. Прямое совпадение с prefer — 0."""
    m = re.search(r"\((\d{3,4})[ip]?\)", name)
    actual = m.group(1) if m else ""
    if prefer and actual == prefer:
        return 0
    try:
        return abs(QUALITY_ORDER.index(actual) - QUALITY_ORDER.index(prefer))
    except ValueError:
        return 99


def is_blocked(name: str) -> bool:
    return any(re.search(p, name) for p in BLOCKLIST_PATTERNS)


def find_channel(spec: dict, pool: list[Channel]) -> Channel | None:
    """Найти лучшее совпадение для одного канала по списку patterns."""
    for pattern in spec["patterns"]:
        rx = re.compile(pattern, re.IGNORECASE)
        candidates = [c for c in pool if rx.search(c.name) and not is_blocked(c.name)]
        if not candidates:
            continue
        candidates.sort(key=lambda c: quality_score(c.name, spec.get("prefer", "")))
        return candidates[0]
    return None


def patch_attrs(attrs: str, group: str, display: str) -> str:
    """Заменить/добавить group-title и tvg-name в атрибутах EXTINF."""
    # group-title
    if 'group-title="' in attrs:
        attrs = re.sub(r'group-title="[^"]*"', f'group-title="{group}"', attrs)
    else:
        attrs += f' group-title="{group}"'
    # tvg-name (для EPG-совмещения)
    if 'tvg-name="' in attrs:
        attrs = re.sub(r'tvg-name="[^"]*"', f'tvg-name="{display}"', attrs)
    else:
        attrs += f' tvg-name="{display}"'
    return attrs.strip()


def build_playlist(catalog: list[Channel]) -> tuple[str, list[tuple[str, str]]]:
    lines = [f'#EXTM3U url-tvg="{EPG_URL}" x-tvg-url="{EPG_URL}"']
    missing: list[tuple[str, str]] = []  # (категория, имя)
    matched = 0

    for cat in CATEGORIES:
        for spec in cat["channels"]:
            # URL-override: если в spec прописан url — берём его, не ищем
            # в iptv-org. Используется для каналов, найденных в smolnp
            # или других сторонних источниках. Логотип можно задать через
            # spec["logo"], user-agent — через spec["ua"].
            if spec.get("url"):
                logo = spec.get("logo", "")
                ua = spec.get("ua", "")
                attrs = f'tvg-name="{spec["name"]}"'
                if logo:
                    attrs += f' tvg-logo="{logo}"'
                if ua:
                    attrs += f' http-user-agent="{ua}"'
                attrs += f' group-title="{cat["title"]}"'
                lines.append(f"#EXTINF:-1 {attrs},{spec['name']}")
                lines.append(spec["url"])
                matched += 1
                continue

            ch = find_channel(spec, catalog)
            if ch is None:
                missing.append((cat["title"], spec["name"]))
                continue
            attrs = patch_attrs(ch.attrs, cat["title"], spec["name"])
            lines.append(f"#EXTINF:-1 {attrs},{spec['name']}")
            lines.append(ch.url)
            matched += 1

    print(f"  собрано: {matched}, не найдено: {len(missing)}")
    return "\n".join(lines) + "\n", missing


def extract_hosts(content: str) -> list[str]:
    """Вытащить уникальные хосты потоков для router-side PBR-bypass.

    Парсим все строки, которые выглядят как URL (http/https/rtmp), достаём
    netloc, отбрасываем порт и приводим к lower-case. Список используется
    роутером, чтобы развернуть его в IP-set и заворачивать IPTV-трафик
    мимо AWG-туннеля (см. README раздел про gео-блокировку).
    """
    hosts: set[str] = set()
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parsed = urllib.parse.urlparse(line)
        if parsed.scheme not in {"http", "https", "rtmp", "rtmps"}:
            continue
        host = parsed.hostname
        if host:
            hosts.add(host.lower())
    return sorted(hosts)


def write_outputs(content: str) -> None:
    OUT_MAIN.write_text(content, encoding="utf-8")
    OUT_USB.parent.mkdir(parents=True, exist_ok=True)
    OUT_USB.write_text(content, encoding="utf-8")
    print(f"✓ записано: {OUT_MAIN.relative_to(ROOT)}")
    print(f"✓ записано: {OUT_USB.relative_to(ROOT)}")

    hosts = extract_hosts(content)
    OUT_HOSTS.write_text("\n".join(hosts) + "\n", encoding="utf-8")
    print(f"✓ записано: {OUT_HOSTS.relative_to(ROOT)} ({len(hosts)} хостов)")


def main() -> int:
    try:
        source = fetch_source()
    except Exception as exc:
        print(f"✗ ошибка скачивания: {exc}", file=sys.stderr)
        return 1

    catalog = parse(source)
    if not catalog:
        print("✗ источник пустой", file=sys.stderr)
        return 1

    content, missing = build_playlist(catalog)
    write_outputs(content)

    if missing:
        print("\n⚠ не нашлись в источнике (значит исключены из плейлиста):")
        for cat, name in missing:
            print(f"   {cat} → {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

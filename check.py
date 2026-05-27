#!/usr/bin/env python3
"""
check.py — реальный проверщик работоспособности потоков в playlist.m3u.

Что делает:
  • Параллельно (40 потоков) пытается забрать первые ~2 КБ каждого
    стрима с теми же заголовками, которые прописаны в EXTINF (User-Agent
    может быть критичен — например, WINK для геолокированных каналов).
  • Для каждого URL решает один из трёх вердиктов:
        ✓ OK     — ответил 200 и контент похож на HLS-плейлист (#EXTM3U)
                   или TS-поток (синхро-байт 0x47)
        ⚠ WARN   — отвечает, но контент странный (можно проверить
                   вручную: некоторые серверы шлют HTML-обёртку)
        ✗ FAIL   — таймаут, DNS, 4xx/5xx, либо отказал TLS
  • Печатает сводку по группам + список нерабочих.

Режимы:
  python3 check.py                — только проверка и отчёт.
  python3 check.py --prune        — дополнительно записать
                                    playlist-working.m3u, в котором
                                    останутся только OK-каналы.

ВАЖНО про вердикты:
  Проверка показывает доступность ИЗ ТВОЕЙ СЕТИ В ДАННЫЙ МОМЕНТ. Если
  канал [Geo-blocked] и ты сейчас вне РФ — он будет помечен FAIL, но
  на ТВ в РФ заработает. И наоборот. Проверять лучше из той же сети,
  где будет стоять ТВ.
"""

from __future__ import annotations

import argparse
import re
import socket
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PLAYLIST = ROOT / "playlist.m3u"
OUT_WORKING = ROOT / "playlist-working.m3u"
TIMEOUT = 8
MAX_WORKERS = 40
PROBE_BYTES = 2048

UA_DEFAULT = "Mozilla/5.0 (SMART-TV; Linux; Tizen 6.0) AppleWebKit/537.36 Chrome/108.0.0.0 Safari/537.36"


def parse_playlist(text: str) -> list[tuple[str, str, str]]:
    """Вернуть список (group, name, url, ua) для каждого канала."""
    items: list[tuple[str, str, str, str]] = []
    extinf: str | None = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#EXTINF"):
            extinf = line
        elif line.startswith("#"):
            continue
        else:
            if not extinf:
                continue
            group = re.search(r'group-title="([^"]+)"', extinf)
            name_m = re.search(r',([^,]+)$', extinf)
            ua_m = re.search(r'http-user-agent="([^"]+)"', extinf)
            items.append((
                group.group(1) if group else "?",
                name_m.group(1).strip() if name_m else "?",
                line,
                ua_m.group(1) if ua_m else UA_DEFAULT,
            ))
            extinf = None
    return items


def classify(data: bytes, status: int) -> str:
    # 200 = ОК, 206 = Partial Content (нормальный ответ на Range-запрос),
    # оба значат «сервер успешно отдаёт байты».
    if status not in (200, 206):
        return "FAIL"
    if not data:
        return "FAIL"
    head = data[:512].lstrip()
    if head.startswith(b"#EXTM3U") or b"#EXT-X-" in data[:1024]:
        return "OK"
    # MPEG-TS поток начинается с 0x47 (sync byte), повторяющегося каждые 188 байт
    if data[:1] == b"\x47":
        return "OK"
    # Иногда DASH (XML)
    if b"<MPD" in data[:512] or b"<?xml" in data[:64]:
        return "OK"
    # HTML-обёртка — сервер вернул страницу вместо потока
    if b"<html" in data[:200].lower() or b"<!doctype" in data[:200].lower():
        return "FAIL"
    return "WARN"


def probe(url: str, ua: str) -> tuple[str, str]:
    """Вернуть (вердикт, причина)."""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": ua,
            "Range": f"bytes=0-{PROBE_BYTES-1}",
            "Accept": "*/*",
        })
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            data = r.read(PROBE_BYTES)
            return classify(data, r.status), f"http {r.status}"
    except urllib.error.HTTPError as e:
        return "FAIL", f"http {e.code}"
    except urllib.error.URLError as e:
        return "FAIL", f"url:{e.reason}"
    except socket.timeout:
        return "FAIL", "timeout"
    except Exception as e:
        return "FAIL", f"{type(e).__name__}:{e}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prune", action="store_true",
                    help="Записать playlist-working.m3u только с OK-каналами")
    args = ap.parse_args()

    if not PLAYLIST.exists():
        print("✗ Нет playlist.m3u — сначала запусти build.py", file=sys.stderr)
        return 1

    raw = PLAYLIST.read_text(encoding="utf-8")
    items = parse_playlist(raw)
    print(f"→ Проверяю {len(items)} каналов (макс {TIMEOUT}s на канал, "
          f"{MAX_WORKERS} параллельно)…\n")

    results: dict[int, tuple[str, str]] = {}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {
            pool.submit(probe, url, ua): i
            for i, (_, _, url, ua) in enumerate(items)
        }
        for n, fut in enumerate(as_completed(futures), 1):
            i = futures[fut]
            results[i] = fut.result()
            verdict = results[i][0]
            mark = {"OK": "✓", "WARN": "⚠", "FAIL": "✗"}[verdict]
            print(f"  [{n:3d}/{len(items)}] {mark} {items[i][1]}")

    # Сводка по группам
    print("\n" + "═" * 64)
    print("СВОДКА ПО КАТЕГОРИЯМ")
    print("═" * 64)
    by_group: dict[str, dict[str, int]] = {}
    for i, (group, _name, _url, _ua) in enumerate(items):
        v = results[i][0]
        by_group.setdefault(group, {"OK": 0, "WARN": 0, "FAIL": 0})[v] += 1
    for group, counts in by_group.items():
        total = sum(counts.values())
        print(f"  {group:35s}  ✓{counts['OK']:3d}  ⚠{counts['WARN']:3d}  ✗{counts['FAIL']:3d}  / {total}")

    # Список нерабочих
    fails = [(items[i], results[i]) for i in range(len(items)) if results[i][0] == "FAIL"]
    if fails:
        print(f"\n✗ Нерабочие ({len(fails)}):")
        for (group, name, _url, _ua), (_v, reason) in fails:
            print(f"   {group} → {name}   ({reason})")

    warns = [(items[i], results[i]) for i in range(len(items)) if results[i][0] == "WARN"]
    if warns:
        print(f"\n⚠ С предупреждением ({len(warns)}) — стоит проверить вручную:")
        for (group, name, _url, _ua), (_v, reason) in warns:
            print(f"   {group} → {name}   ({reason})")

    total = len(items)
    ok = sum(1 for v in results.values() if v[0] == "OK")
    print(f"\nИТОГО: ✓ {ok} / {total}   "
          f"({100*ok//total}% работают сейчас из этой сети)")

    if args.prune:
        # сохранить только работающие
        lines = ["#EXTM3U " + raw.splitlines()[0].split(" ", 1)[1]] if raw.splitlines()[0].startswith("#EXTM3U") else ["#EXTM3U"]
        for i, (_group, _name, url, _ua) in enumerate(items):
            if results[i][0] != "OK":
                continue
            # восстановить EXTINF: пройти по сырым строкам
            # проще: найти в raw блок с этим url
            pat = re.compile(r'(#EXTINF:[^\n]+)\n' + re.escape(url), re.MULTILINE)
            m = pat.search(raw)
            if m:
                lines.append(m.group(1))
                lines.append(url)
        OUT_WORKING.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"\n✓ Записан playlist-working.m3u ({ok} каналов)")

    return 0


if __name__ == "__main__":
    sys.exit(main())

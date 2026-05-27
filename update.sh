#!/usr/bin/env bash
# update.sh — пересобрать плейлист и скопировать всё на флешку.
#
# Использование:
#   ./update.sh                           — только пересобрать playlist.m3u
#   ./update.sh /Volumes/ИМЯ_ФЛЕШКИ       — пересобрать и скопировать на флешку

set -euo pipefail

cd "$(dirname "$0")"

echo "═══ 1/2  Сборка плейлиста ═══"
python3 build.py

USB_DEST="${1:-}"
if [[ -z "$USB_DEST" ]]; then
    echo
    echo "✓ Готово. playlist.m3u лежит в текущей папке и в usb/."
    echo
    echo "Полезные команды:"
    echo "  python3 check.py            — проверить какие потоки сейчас работают"
    echo "  python3 check.py --prune    — сделать playlist-working.m3u (только OK)"
    echo "  ./update.sh /Volumes/ФЛЕШКА — записать всё на флешку"
    exit 0
fi

if [[ ! -d "$USB_DEST" ]]; then
    echo "✗ Флешка не найдена: $USB_DEST"
    echo "   Проверь, что воткнута и имя совпадает. Список:"
    ls -1 /Volumes/ 2>/dev/null || true
    exit 1
fi

echo
echo "═══ 2/2  Копирование на флешку: $USB_DEST ═══"
TARGET="$USB_DEST/IPTV"
mkdir -p "$TARGET"

cp -v usb/playlist.m3u "$TARGET/"
cp -v usb/INSTALL.txt "$TARGET/" 2>/dev/null || true

if [[ -f StreamVault.apk ]]; then
    cp -v StreamVault.apk "$TARGET/"
else
    echo "  (StreamVault.apk не найден рядом со скриптом — пропускаю."
    echo "   Скачать: https://github.com/Davidona/StreamVault-IPTV/releases/latest)"
fi

# на FAT32 надо принудительно сбросить буферы
sync 2>/dev/null || true

echo
echo "✓ Готово. На флешке в папке IPTV/:"
ls -lh "$TARGET"
echo
echo "Можно вынимать (Finder → ⏏) и втыкать в ТВ."

#!/usr/bin/env bash
# setup-github.sh — полная автоматика: создаёт GitHub-репу,
# пушит проект, активирует GitHub Actions, печатает raw-URL
# плейлиста для StreamVault.
#
# После этого:
#   • плейлист пересобирается на серверах GitHub каждый день в 03:17 UTC;
#   • StreamVault с галкой "Auto-refresh: daily" подтягивает изменения сам;
#   • ничего больше делать не надо — IPTV «вечный».
#
# Использование:
#   ./setup-github.sh              — создать приватную репу iptv
#   ./setup-github.sh my-iptv      — задать своё имя репы
#   ./setup-github.sh my-iptv pub  — создать публичную репу (по умолчанию private)

set -euo pipefail
cd "$(dirname "$0")"

REPO_NAME="${1:-iptv}"
VISIBILITY="${2:-private}"

# ── проверки окружения ───────────────────────────────────────────
if ! command -v gh >/dev/null 2>&1; then
    echo "✗ Нет GitHub CLI. Установи:  brew install gh"
    exit 1
fi
if ! gh auth status >/dev/null 2>&1; then
    echo "✗ Нет логина в gh. Выполни:  gh auth login"
    exit 1
fi
if ! command -v git >/dev/null 2>&1; then
    echo "✗ Нет git. Установи Xcode CLT:  xcode-select --install"
    exit 1
fi

USERNAME="$(gh api user --jq .login)"
echo "→ Юзернейм: $USERNAME"
echo "→ Имя репы: $REPO_NAME"
echo "→ Видимость: $VISIBILITY"

# ── git init ──────────────────────────────────────────────────────
if [[ ! -d .git ]]; then
    echo "═══ git init ═══"
    git init -q -b main
    git add .
    git -c user.email="$USERNAME@users.noreply.github.com" \
        -c user.name="$USERNAME" \
        commit -q -m "Initial commit: IPTV plays catalog & builder"
fi

# ── проверка/создание репы ────────────────────────────────────────
if gh repo view "$USERNAME/$REPO_NAME" >/dev/null 2>&1; then
    echo "═══ Репа уже существует: $USERNAME/$REPO_NAME — пушу ═══"
    git remote get-url origin >/dev/null 2>&1 \
        || git remote add origin "https://github.com/$USERNAME/$REPO_NAME.git"
    git push -u origin main
else
    echo "═══ Создаю репу $USERNAME/$REPO_NAME ═══"
    gh repo create "$REPO_NAME" \
        --"$VISIBILITY" \
        --source=. \
        --remote=origin \
        --push \
        --description "Auto-built Russian IPTV playlist for StreamVault"
fi

# ── триггер первого запуска workflow ──────────────────────────────
echo "═══ Запускаю workflow для проверки ═══"
sleep 3   # GitHub нужно немного, чтобы зарегистрировать workflow после push
gh workflow run build-playlist --repo "$USERNAME/$REPO_NAME" 2>/dev/null \
    && echo "  ✓ workflow запущен" \
    || echo "  (первый запуск может появиться через 1-2 минуты — проверь вкладку Actions)"

# ── финальный отчёт ───────────────────────────────────────────────
RAW_URL="https://raw.githubusercontent.com/$USERNAME/$REPO_NAME/main/playlist.m3u"

cat <<EOF

════════════════════════════════════════════════════════════════
                        ✓ ГОТОВО
════════════════════════════════════════════════════════════════

  Репозиторий:  https://github.com/$USERNAME/$REPO_NAME
  Workflow:     https://github.com/$USERNAME/$REPO_NAME/actions

  URL плейлиста для StreamVault (скопируй):

    $RAW_URL

  Что дальше:
    1. Открой StreamVault на ТВ.
    2. Settings → Sources → Add → M3U URL → вставь ссылку ↑
    3. Поставь галку "Auto-refresh: daily".
    4. Забудь про обновления навсегда — каждый день
       в 06:17 МСК workflow пересоберёт плейлист, StreamVault
       подтянет новые ссылки сам.

  Если репа приватная — в StreamVault плейлист не загрузится
  (raw URL потребует токен). Сделай репу публичной командой:
       gh repo edit $USERNAME/$REPO_NAME --visibility public --accept-visibility-change-consequences

EOF

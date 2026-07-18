"""
Белый список каналов и категорий.

Каждый канал описывается:
  patterns - список регулярных выражений, которыми ищем канал в названии
             из исходного плейлиста iptv-org (case-insensitive).
             Первое совпадение по приоритету сверху-вниз.
  prefer   - предпочтения по качеству ('1080', '720', '576', etc.) —
             если найдено несколько вариантов канала, выберем максимально
             близкий к этому значению.
  name     - финальное имя канала в нашем плейлисте.

Категории идут в том порядке, в котором появятся на ТВ.
"""

CATEGORIES = [
    # ──────────────────────────────────────────────────────────────────
    {
        "title": "📺 Главные эфирные",
        "channels": [
            {"name": "Первый канал",        "patterns": [r"^Первый канал"],                "prefer": "1080"},
            {"name": "Россия 1",            "patterns": [r"^Россия 1(?! HD)(?! \(\+)"],    "prefer": "1080"},
            {"name": "НТВ",                 "patterns": [r"^NTV HD", r"^НТВ \("],          "prefer": "1080"},
            {"name": "Пятый канал",         "patterns": [r"^Пятый Канал"],                 "prefer": "540"},
            {"name": "ТВ Центр",            "patterns": [r"^ТВ Центр International", r"^ТВ Центр(?! International)"], "prefer": "720"},
            # РЕН ТВ / ОТР удалены: оба варианта (HD и SD) в iptv-org
            # не отвечают, в smolnp тоже мёртвы. Если когда-нибудь
            # источник обновит — вернутся через GitHub Actions.
        ],
    },
    # ──────────────────────────────────────────────────────────────────
    {
        "title": "📰 Новости",
        "channels": [
            {"name": "Россия 24",           "patterns": [r"^Россия 24"],                   "prefer": "1080"},
            {"name": "РБК",                 "patterns": [r"^РБК"],                         "prefer": "576"},
            {"name": "Мир 24",              "patterns": [r"^Мир 24"],                      "prefer": "1080"},
            {"name": "Мир",                 "patterns": [r"^Мир \(1080"],                  "prefer": "1080"},
            {"name": "360° Новости",        "patterns": [r"^360° Новости"],                "prefer": "1080"},
            {"name": "360°",                "patterns": [r"^360° \("],                     "prefer": "1080"},
            {"name": "Известия",            "patterns": [r"^Известия"],                    "prefer": "1080"},
            {"name": "Москва 24",           "patterns": [r"^Москва 24"],                   "prefer": "1080"},
            # Euronews Russian мёртв в источнике (timeout). Берём
            # английскую версию — единственный реально работающий вариант.
            {"name": "Euronews",            "patterns": [r"^Euronews English HD", r"^Euronews \(720"], "prefer": ""},
            {"name": "Вести ФМ",            "patterns": [r"^Вести ФМ"],                    "prefer": ""},
        ],
    },
    # ──────────────────────────────────────────────────────────────────
    #{
        # Международные новости — мировая повестка на разных языках.
        # CGTN Русский и Беларусь 24 — единственные крупные публичные
        # русскоязычные международные каналы в открытом доступе.
        #"title": "🌍 Международные новости",
        #"channels": [
            #{"name": "CGTN Русский",        "patterns": [r"^CGTN Русский"],                "prefer": "1080"},
            #{"name": "Беларусь 24",         "patterns": [r"^Беларусь 24"],                 "prefer": "1080"},
            # Беларусь 2 удалён: сервер закрывает соединение во время
            # ответа (исчерпан где-то у источника). Беларусь 24 жива.
            # BBC News (1080p) выдаёт 404. Североамериканский поток жив.
            #{"name": "BBC News",            "patterns": [r"^BBC News North America", r"^BBC News \(1080"], "prefer": "1080"},
            #{"name": "Al Jazeera English",  "patterns": [r"^Al Jazeera English"],          "prefer": "1080"},
            #{"name": "DW English",          "patterns": [r"^DW English"],                  "prefer": "1080"},
            #{"name": "France 24 English",   "patterns": [r"^France 24 English"],           "prefer": "1080"},
            #{"name": "CGTN English",        "patterns": [r"^CGTN \(1080"],                 "prefer": "1080"},
            #{"name": "TV BRICS Russian",    "patterns": [r"^TV BRICS Russian"],            "prefer": "1080"},
            #{"name": "Euronews English",    "patterns": [r"^Euronews English HD"],         "prefer": ""},
            #{"name": "TRT World",           "patterns": [r"^TRT World"],                   "prefer": "1080"},
            #{"name": "Reuters",             "patterns": [r"^Reuters \(1080"],              "prefer": "1080"},
            #{"name": "i24NEWS English",     "patterns": [r"^i24NEWS English USA"],         "prefer": "1080"},
            #{"name": "ABC News",            "patterns": [r"^ABC News \(720"],              "prefer": "720"},
            #{"name": "CBS News",            "patterns": [r"^CBS News 24/7"],               "prefer": "720"},
        #],
    #},
    # ──────────────────────────────────────────────────────────────────
    {
        "title": "🎭 Развлекательные",
        "channels": [
            {"name": "СТС",                 "patterns": [r"^СТС \("],                      "prefer": "576"},
            {"name": "ТНТ",                 "patterns": [r"^ТНТ \("],                      "prefer": "576"},
            {"name": "ТНТ4",                "patterns": [r"^ТНТ4"],                        "prefer": "576"},
            {"name": "Пятница!",            "patterns": [r"^Пятница! International", r"^Пятница! \("], "prefer": "576"},
            {"name": "ТВ-3",                "patterns": [r"^ТВ-3"],                        "prefer": "540"},
            {"name": "Домашний",            "patterns": [r"^Домашний International", r"^Домашний \("], "prefer": "720"},
            {"name": "2x2",                 "patterns": [r"^2x2 \("],                      "prefer": "576"},
            {"name": "Че!",                 "patterns": [r"^Че! \("],                      "prefer": "576"},
            {"name": "Поехали!",            "patterns": [r"^Поехали!"],                    "prefer": "1080"},
            {"name": "Субботa!",            "patterns": [r"^Subbota!"],                    "prefer": "1080"},
            {"name": "STS Love",            "patterns": [r"^STS Love"],                    "prefer": "576"},
        ],
    },
    # ──────────────────────────────────────────────────────────────────
    {
        "title": "😄 Юмор",
        "channels": [
            {"name": "КВН ТВ",              "patterns": [r"^КВН ТВ"],                      "prefer": "576"},
            # alpha Funny удалён: стрим отдаёт 404.
            # viju+ Comedy: iptv-org стрим мёртв. Прямой URL из smolnp/IPTVru.
            {"name": "viju+ Comedy", "patterns": [],
             "url": "http://176.118.197.101/Komediya/index.m3u8",
             "logo": "https://i.imgur.com/y0mxv1V.png"},
            {"name": "alpha Moretime",      "patterns": [r"^alpha Moretime"],              "prefer": "1080"},
            {"name": "Твое ТВ Юмор",        "patterns": [r"^Твое ТВ Юмор"],                "prefer": "1080"},
            {"name": "Kinokomedija",        "patterns": [r"^Kinokomedija"],                "prefer": "576"},
        ],
    },
    # ──────────────────────────────────────────────────────────────────
    #{
        #"title": "🎵 Музыка",
        #"channels": [
            #{"name": "Муз ТВ",              "patterns": [r"^Муз ТВ"],                      "prefer": "450"},
            #{"name": "Europa Plus TV",      "patterns": [r"^Europa Plus TV"],              "prefer": "1080"},
            #{"name": "RU.TV",               "patterns": [r"^RU\.TV"],                      "prefer": "1080"},
            #{"name": "BRIDGE",              "patterns": [r"^BRIDGE \("],                   "prefer": "576"},
            # BRIDGE Deluxe удалён: единственный стрим мёртв.
            #{"name": "BRIDGE Hits",         "patterns": [r"^BRIDGE Hits"],                 "prefer": "576"},
            #{"name": "BRIDGE Classic",      "patterns": [r"^BRIDGE Classic"],              "prefer": "576"},
            #{"name": "Жара TV",             "patterns": [r"^Жара TV"],                     "prefer": "576"},
            # «Музыка Первого» удалена: стрим в источнике отдаёт 404
            # (проверено check.py). Если в источнике восстановят —
            # вернётся автоматически через GitHub Action.
            #{"name": "Первый Музыкальный",  "patterns": [r"^Первый Музыкальный Канал HD"], "prefer": "1080"},
            # MCM Top удалён: стрим мёртв.
            #{"name": "VIVA Russia",         "patterns": [r"^VIVA Russia"],                 "prefer": "1080"},
            #{"name": "15+ Music",           "patterns": [r"^15\+ Music"],                  "prefer": "1080"},
            # MusicBox Gold удалён: стрим мёртв.
            #{"name": "Радио Шансон",        "patterns": [r"^Радио Шансон"],                "prefer": "720"},
            #{"name": "Deluxe Music",        "patterns": [r"^Deluxe Music"],                "prefer": "720"},
            # MTV (1080p) и MTV HD — оба варианта мёртвы. Заменены на
            # рабочие тематические MTV-каналы из глобального каталога.
            #{"name": "MTV Biggest Pop",     "patterns": [r"^MTV Biggest Pop"],             "prefer": "1080"},
            #{"name": "MTV Spankin' New",    "patterns": [r"^MTV Spankin' New"],            "prefer": "1080"},
            #{"name": "MTV Ridiculousness",  "patterns": [r"^MTV Ridiculousness"],          "prefer": ""},
            #{"name": "Матур ТВ",            "patterns": [r"^Матур ТВ"],                    "prefer": "1080"},
            # FON Music: iptv-org мёртв. URL из smolnp (на самом деле
            # это поток TNT Music под брендом FON Music).
            #{"name": "FON Music", "patterns": [],
            # "url": "https://cdn-01.bonus-tv.ru/tntmusic/playlist.m3u8"},
        #],
    #},
    # ──────────────────────────────────────────────────────────────────
    #{
        # Премиум-музыка Stingray — фоновое слушание по жанрам без
        # ведущих и рекламы. Канадская премиум-сеть, обычно доступна
        # только в платных пакетах кабельных операторов; здесь — открытые
        # FAST-стримы. Все 1080p, 24/7.
        #"title": "🎼 Премиум-музыка (Stingray)",
        #"channels": [
            #{"name": "Stingray Hit List",          "patterns": [r"^Stingray Hit List"],          "prefer": "1080"},
            #{"name": "Stingray Greatest Hits",     "patterns": [r"^Stingray Greatest Hits"],     "prefer": "1080"},
            #{"name": "Stingray Pop Adult",         "patterns": [r"^Stingray Pop Adult"],         "prefer": "1080"},
            #{"name": "Stingray Flashback 70s",     "patterns": [r"^Stingray Flashback 70s"],     "prefer": "1080"},
            #{"name": "Stingray Remember the 80s",  "patterns": [r"^Stingray Remember the 80s"],  "prefer": "1080"},
            #{"name": "Stingray Nothin' But 90s",   "patterns": [r"^Stingray Nothin' But 90s"],   "prefer": "1080"},
            #{"name": "Stingray Classic Rock",      "patterns": [r"^Stingray Classic Rock"],      "prefer": "1080"},
            #{"name": "Stingray Classica",          "patterns": [r"^Stingray Classica"],          "prefer": "1080"},
            #{"name": "Stingray DJAZZ",             "patterns": [r"^Stingray DJAZZ"],             "prefer": "1080"},
            #{"name": "Stingray Easy Listening",    "patterns": [r"^Stingray Easy Listening"],    "prefer": "1080"},
            #{"name": "Stingray Hot Country",       "patterns": [r"^Stingray Hot Country"],       "prefer": "1080"},
            #{"name": "Stingray CMusic",            "patterns": [r"^Stingray CMusic"],            "prefer": "1080"},
            #{"name": "Stingray Naturescape",       "patterns": [r"^Stingray Naturescape"],       "prefer": "1080"},
            #{"name": "Stingray Karaoke",           "patterns": [r"^Stingray Karaoke"],           "prefer": "1080"},
        #],
    #},
    # ──────────────────────────────────────────────────────────────────
    {
        "title": "👶 Детям",
        "channels": [
            {"name": "Карусель",            "patterns": [r"^Carousel"],                    "prefer": "1080"},
            {"name": "Мульт",               "patterns": [r"^Мульт \("],                    "prefer": "1080"},
            {"name": "Мульт и Музыка",      "patterns": [r"^Мульт и Музыка"],              "prefer": "576"},
            {"name": "Мультимания",         "patterns": [r"^Мультимания"],                 "prefer": "576"},
            # STS Kids удалён: стрим мёртв (facecast.io хост лежит).
            {"name": "Радость моя",         "patterns": [r"^Радость моя"],                 "prefer": "576"},
            {"name": "TiJi",                "patterns": [r"^TiJi"],                        "prefer": "576"},
            # Mama удалён: стрим мёртв.
            {"name": "Солнце",              "patterns": [r"^Солнце"],                      "prefer": "576"},
            {"name": "Ani",                 "patterns": [r"^Ani \("],                      "prefer": "576"},
            # Шаян ТВ удалён: стрим 403 (видимо геофильтр на самом
            # источнике, ВПН-bypass не помог).
            {"name": "Disney Channel",      "patterns": [r"^Disney Channel \(1080"],       "prefer": "1080"},
            {"name": "Disney Junior",       "patterns": [r"^Disney Jr\. \(1080", r"^Disney Junior \("], "prefer": "1080"},
            {"name": "Nickelodeon",         "patterns": [r"^Nickelodeon \(1080"],          "prefer": "1080"},
            {"name": "Nickelodeon Junior",  "patterns": [r"^Nickelodeon Junior"],          "prefer": "1080"},
            # Tiny Pop удалён: 403 — UK-only, ВПН-bypass не помог.
        ],
    },
    # ──────────────────────────────────────────────────────────────────
    #{
        #"title": "⚽ Спорт",
        #"channels": [
            #{"name": "Матч! Планета",       "patterns": [r"^Матч! Планета"],               "prefer": "720"},
            #{"name": "МАТЧ! Арена",         "patterns": [r"^МАТЧ! Арена"],                 "prefer": "720"},
            #{"name": "МАТЧ! Игра",          "patterns": [r"^МАТЧ! Игра"],                  "prefer": "720"},
            # Матч! Боец удалён: стрим мёртв (нет в smolnp).
            #{"name": "Матч! Страна",        "patterns": [r"^Match! Strana"],               "prefer": "720"},
            #{"name": "КХЛ",                 "patterns": [r"^KHL \("],                      "prefer": "720"},
            #{"name": "КХЛ Прайм",           "patterns": [r"^KHL Prime"],                   "prefer": "720"},
            #{"name": "Футбол",              "patterns": [r"^Футбол"],                      "prefer": "720"},
            #{"name": "Бокс ТВ",             "patterns": [r"^Бокс ТВ"],                     "prefer": "720"},
            #{"name": "MMA TV",              "patterns": [r"^MMA TV"],                      "prefer": "1080"},
            # viju+ Sport: iptv-org мёртв. Прямой URL из smolnp.
            #{"name": "viju+ Sport", "patterns": [],
            # "url": "http://93.84.115.174:10181/viasatsport"},
            # Russian Extreme удалён: ни iptv-org, ни smolnp не отвечают.
            #{"name": "Fox Sports 1",        "patterns": [r"^Fox Sports 1"],                "prefer": "1080"},
            # Premier Sports 1/2 удалены: UK-only, 403.
            #{"name": "DAZN Combat",         "patterns": [r"^DAZN Combat"],                 "prefer": "1080"},
            #{"name": "ESPN8 The Ocho",      "patterns": [r"^ESPN8 The Ocho"],              "prefer": "1080"},
        #],
    #},
    # ──────────────────────────────────────────────────────────────────
    {
        "title": "🎬 Кино и сериалы",
        "channels": [
            {"name": "Дом Кино",                "patterns": [r"^Дом Кино(?! Премиум)"],       "prefer": "576"},
            {"name": "Дом Кино Премиум",        "patterns": [r"^Дом Кино Премиум"],           "prefer": "1080"},
            {"name": "КИНО ТВ",                 "patterns": [r"^КИНО ТВ"],                    "prefer": "720"},
            {"name": "Hollywood HD",            "patterns": [r"^Hollywood HD"],               "prefer": "1080"},
            {"name": "alpha Cinema",            "patterns": [r"^alpha Cinema"],               "prefer": "1080"},
            {"name": "Кинопоказ",               "patterns": [r"^Кинопоказ"],                  "prefer": "576"},
            {"name": "Кинеко",                  "patterns": [r"^Кинеко"],                     "prefer": "1080"},
            {"name": "Иллюзион+",               "patterns": [r"^Иллюзион\+"],                 "prefer": "576"},
            {"name": "Русский Иллюзион",        "patterns": [r"^Русский Иллюзион"],           "prefer": "576"},
            {"name": "Русский Бестселлер",      "patterns": [r"^Русский Бестселлер"],         "prefer": "576"},
            {"name": "Русский Детектив",        "patterns": [r"^Русский Детектив"],           "prefer": "576"},
            {"name": "Русский Роман",           "patterns": [r"^Русский Роман"],              "prefer": "1080"},
            {"name": "Новый Русский",           "patterns": [r"^Новый Русский"],              "prefer": "720"},
            # viju-семейство удалено целиком: общий хост
            # cdn-evacoder-tv.facecast.io не отвечает (5 каналов: viju
            # TV1000, viju TV1000 русское/action, viju+ Megahit/Premiere).
            # Если хост поднимется — вернуть.
            {"name": "Мир Сериала",             "patterns": [r"^Мир Сериала"],                "prefer": "576"},
            {"name": "НТВ Сериал",              "patterns": [r"^НТВ Сериал"],                 "prefer": "576"},
            {"name": "НТВ Хит",                 "patterns": [r"^НТВ Хит"],                    "prefer": "576"},
            # Amedia Premium: iptv-org мёртв. URL из smolnp.
            {"name": "Amedia Premium", "patterns": [],
             "url": "http://45.145.32.13:20440/amedia_premium_hd/index.m3u8?token=test"},
            {"name": "Amedia Hit",              "patterns": [r"^Amedia Hit"],                 "prefer": "720"},
            {"name": "Смотрим Честный Детектив","patterns": [r"^Смотрим Честный Детектив"],   "prefer": "1080"},
            # Смотрим 100% Классика/Любовь/Мужское удалены: возвращают
            # 403, серверу smotrim.ru нужны куки сессии (этот плеер
            # работает только из браузера с авторизацией).
        ],
    },
    # ──────────────────────────────────────────────────────────────────
    {
        # Премиум-кино — мировые бренды. Все 24/7, без geo-block.
        # Cinema — мировой канал классики и блокбастеров.
        # Paramount — голливудские студийные фильмы.
        "title": "💎 Премиум-кино",
        "channels": [
            {"name": "Cinema",                  "patterns": [r"^Cinema \(1080"],              "prefer": "1080"},
            {"name": "Paramount Movie Channel", "patterns": [r"^Paramount Movie Channel"],    "prefer": ""},
            {"name": "Paramount+ Picks",        "patterns": [r"^Paramount\+ Picks"],          "prefer": ""},
            {"name": "FX Movie Channel",        "patterns": [r"^FX Movie Channel"],           "prefer": "720"},
            {"name": "CinemaWorld",             "patterns": [r"^CinemaWorld"],                "prefer": "720"},
            # Sony Entertainment HD удалён: 400, Indian gео-блок.
            # Universal Cinema / Universal Comedy удалены:
            # сервер отказывает в соединении (Connection refused).
            {"name": "FilmRise Westerns",       "patterns": [r"^FilmRise Westerns"],          "prefer": "720"},
            {"name": "MovieSphere",             "patterns": [r"^MovieSphere \(1080"],         "prefer": "1080"},
            {"name": "MovieSphere UK",          "patterns": [r"^MovieSphere UK"],             "prefer": "1080"},
        ],
    },
    # ──────────────────────────────────────────────────────────────────
    {
        "title": "📚 Культура и наука",
        "channels": [
            {"name": "Россия К",            "patterns": [r"^Россия К"],                    "prefer": "1080"},
            {"name": "Звезда",              "patterns": [r"^Звезда \("],                   "prefer": "1080"},
            {"name": "Звезда Плюс",         "patterns": [r"^Звезда Плюс"],                 "prefer": "1080"},
            {"name": "История",             "patterns": [r"^История"],                     "prefer": "576"},
            {"name": "НАУКА",               "patterns": [r"^НАУКА"],                       "prefer": "1080"},
            # Da Vinci удалён: стрим мёртв.
            {"name": "Моя Планета",         "patterns": [r"^Моя Планета"],                 "prefer": "720"},
            {"name": "Travel+Adventure",    "patterns": [r"^Travel\+Adventure"],           "prefer": "1080"},
            # viju Nature / History удалены: facecast.io хост лежит.
            {"name": "RT Documentary",      "patterns": [r"^RT Documentary"],              "prefer": "1080"},
            {"name": "Terra HD",            "patterns": [r"^Terra HD"],                    "prefer": "720"},
            {"name": "365 Дней",            "patterns": [r"^365 Дней"],                    "prefer": "576"},
            {"name": "Живая Планета",       "patterns": [r"^Живая Планета"],               "prefer": "576"},
            {"name": "Театр",               "patterns": [r"^Театр"],                       "prefer": "576"},
            # Смотрим 100% Факты удалён по той же причине (smotrim 403).
        ],
    },
    # ──────────────────────────────────────────────────────────────────
    {
        # Премиум-документальные — мировые бренды (BBC, History,
        # National Geographic). Часть Nat Geo гео-блокирована для РФ,
        # но варианты "HD" / "HD East" обычно работают.
        "title": "🌎 Премиум док.",
        "channels": [
            {"name": "BBC Earth",                  "patterns": [r"^BBC Earth"],                     "prefer": "1080"},
            # History Channel и оба Nat Geo удалены: ВСЕ варианты в
            # iptv-org мёртвы (timeout/404), включая Japan, East, Finland.
            # History Hit живой — оставляем.
            {"name": "History Hit",                "patterns": [r"^History Hit"],                   "prefer": "1080"},
            {"name": "History Asia",               "patterns": [r"^History Asia"],                  "prefer": ""},
            # Curiosity Now удалён: 403 — US-only Pluto.
            {"name": "Top Gear",                   "patterns": [r"^Top Gear"],                      "prefer": "720"},
            {"name": "Adventure Earth",            "patterns": [r"^Adventure Earth"],               "prefer": "1080"},
            {"name": "Backstage",                  "patterns": [r"^Backstage \("],                  "prefer": "1080"},
            {"name": "Autentic History",           "patterns": [r"^Autentic History"],              "prefer": "1080"},
            {"name": "Bloomberg Originals",        "patterns": [r"^Bloomberg Originals"],           "prefer": "1080"},
            {"name": "BritBox Mysteries",          "patterns": [r"^BritBox Mysteries"],             "prefer": "1080"},
            {"name": "CGTN Documentary",           "patterns": [r"^CGTN Documentary"],              "prefer": "1080"},
        ],
    },
    # ──────────────────────────────────────────────────────────────────
    #{
        # Криминал, расследования, реалити в стиле «true crime».
        # Это FAST-каналы крупных американских и британских брендов:
        # Court TV (CNN-сеть, прямые трансляции громких процессов),
        # Dateline 24/7 (NBC News flagship reality), Deadly Women
        # (Investigation Discovery), DangerTV (экстрим). Все 1080p, 24/7.
        #"title": "🔍 Криминал и расследования",
        #"channels": [
            #{"name": "Court TV",            "patterns": [r"^Court TV"],                    "prefer": "1080"},
            #{"name": "Dateline 24/7",       "patterns": [r"^Dateline 24/7"],               "prefer": "1080"},
            #{"name": "Deadly Women",        "patterns": [r"^Deadly Women"],                "prefer": "1080"},
            #{"name": "DangerTV",            "patterns": [r"^DangerTV"],                    "prefer": "720"},
        #],
    #},
    # ──────────────────────────────────────────────────────────────────
    {
        "title": "🍳 Дом и стиль",
        "channels": [
            {"name": "Кухня ТВ",            "patterns": [r"^Кухня ТВ"],                    "prefer": "576"},
            {"name": "Телекафе",            "patterns": [r"^Телекафе"],                    "prefer": "720"},
            {"name": "FoodTime",            "patterns": [r"^FoodTime"],                    "prefer": "1080"},
            {"name": "Доктор",              "patterns": [r"^Доктор \("],                   "prefer": "1080"},
            {"name": "ЖИВИ!",               "patterns": [r"^ЖИВИ!"],                       "prefer": "1080"},
            {"name": "Здоровое ТВ",         "patterns": [r"^Здоровое ТВ"],                 "prefer": "576"},
            {"name": "FASHION & LIFESTYLE", "patterns": [r"^FASHION & LIFESTYLE"],         "prefer": "1080"},
            # Усадьба: iptv-org мёртв. URL из smolnp.
            {"name": "Усадьба", "patterns": [],
             "url": "https://stream8.cinerama.uz/1427/tracks-v1a1/mono.m3u8"},
            {"name": "Зоопарк",             "patterns": [r"^Zoopark"],                     "prefer": "576"},
            {"name": "Pro100TV",            "patterns": [r"^Pro100TV"],                    "prefer": "576"},
            # «Конный Мир» удалён: стрим отдаёт 404.
        ],
    },
    # ──────────────────────────────────────────────────────────────────
    #{
        #"title": "🚗 Авто и путешествия",
        #"channels": [
            # Auto Plus удалён: стрим мёртв.
            #{"name": "Drive",               "patterns": [r"^Drive \("],                    "prefer": "576"},
            #{"name": "RTG TV",              "patterns": [r"^RTG TV"],                      "prefer": "720"},
            #{"name": "Телепутешествия",     "patterns": [r"^Телепутешествия"],             "prefer": "576"},
            #{"name": "Охотник и рыболов",   "patterns": [r"^Ohotnik i rybolov"],           "prefer": "576"},
        #],
    #},
    # ──────────────────────────────────────────────────────────────────
    {
        # Региональные эфирные — даю обзорно по самым крупным регионам.
        # ТНВ-Планета (Казань) — спутниковая версия татарстанского
        # государственного канала, программы на татарском и русском.
        "title": "🏛 Регионы",
        "channels": [
            {"name": "ТНВ-Планета (Казань)","patterns": [r"^ТНВ-Планета"],                 "prefer": "576"},
            #{"name": "Башкортостан 24",     "patterns": [r"^Башкортостан 24"],             "prefer": "1080"},
            #{"name": "Курай (Уфа)",         "patterns": [r"^Курай"],                       "prefer": "576"},
            #{"name": "Дагестан",            "patterns": [r"^Дагестан"],                    "prefer": "1080"},
            #{"name": "Ингушетия ТВ",        "patterns": [r"^Ингушетия ТВ"],                "prefer": "1080"},
            #{"name": "Осетия Ирыстон",      "patterns": [r"^Осетия Ирыстон"],              "prefer": "1080"},
            #{"name": "Кавказ 24",           "patterns": [r"^Кавказ 24"],                   "prefer": "576"},
            # «Крым 24» удалён: SSL-сертификат сервера невалидный.
            # Дон 24: iptv-org версия 403. URL из smolnp.
            #{"name": "Дон 24", "patterns": [],
            # "url": "https://donmedia.bonus-tv.ru/cdn/donmedia/playlist_sdmid.m3u8"},
            #{"name": "Аист ТВ",             "patterns": [r"^Аист ТВ"],                     "prefer": "1080"},
            #{"name": "Югра",                "patterns": [r"^Югра"],                        "prefer": "1080"},
            #{"name": "Санкт-Петербург",     "patterns": [r"^Санкт-Петербург \("],          "prefer": "576"},
        ],
    },
    # ──────────────────────────────────────────────────────────────────
    # Категория «Православие» удалена по запросу пользователя.
    # Если когда-нибудь понадобится вернуть — добавь:
    #   Спас (^Спас \(), Союз (^Союз \(), Надежда, Три Ангела.
    # ──────────────────────────────────────────────────────────────────
    #{
        # Исламские каналы — только английские (Peace TV, Huda) и
        # прямые трансляции главных мечетей Мекки и Медины с чтением
        # Корана (на арабском, но это сама литургия — язык там вторичен).
        # Принципиально без urdu/индонезийских/бенгальских вариантов —
        # пользователь читает по-русски и по-английски.
        #"title": "🕌 Ислам",
        #"channels": [
            # Прямая трансляция из Заповедной мечети (аль-Харам), Мекка.
            # Круглосуточно: пятикратный намаз, таравих в Рамадан,
            # чтение Корана между молитвами. Саудовский гос. канал.
            #{"name": "Al Quran Al Kareem (Мекка)",
            # "patterns": [r"^Al Quran Al Kareem"], "prefer": "1080"},

            # Прямая трансляция из Мечети Пророка (аль-Масджид
            # ан-Набави), Медина. Круглосуточно, тот же формат.
            #{"name": "Al Sunnah Al Nabawiyah (Медина)",
            # "patterns": [r"^Al Sunnah Al Nabawiyah"], "prefer": "720"},

            # Peace TV — самый известный исламский dawah-канал
            # на английском (шейх Закир Найк).
            #{"name": "Peace TV English",
            # "patterns": [r"^Peace TV English"], "prefer": "1080"},

            # Huda TV — английский, исламский образовательный,
            # проповеди, ответы на вопросы.
            #{"name": "Huda TV",
            # "patterns": [r"^Huda TV"], "prefer": "720"},
        #],
    #},
]

# Глобальный «чёрный список»: даже если канал попадёт в выборку по белому
# списку, отсеем, если в его исходном имени совпадёт любой из этих паттернов.
# Защита от взрослого контента и непредназначенных вариантов.
BLOCKLIST_PATTERNS = [
    r"(?i)\b18\+",
    # «adult» только если он маркер контента, а не «adult contemporary»
    # (Stingray Pop Adult — это просто поп-музыка для взрослой аудитории).
    r"(?i)\badult\s+(?:video|content|channel|tv|hits|night|xxx)",
    r"(?i)\bxxx\b",
    r"(?i)erotic",
    r"(?i)эротик",
    r"(?i)playboy",
    r"(?i)hustler",
    r"(?i)brazzers",
    r"(?i)russkaya noch",
    r"(?i)night club",
    r"(?i)шалун",
]

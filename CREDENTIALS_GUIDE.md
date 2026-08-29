# 🔑 Полная инструкция по получению API-ключей и настройке сокетов (SoketAEO)

В этом руководстве пошагово расписано, как получить ключи для каждого сервиса, где нужен аккаунт, где он **НЕ** нужен, и как работают веб-сокеты реального времени.

---

## 📌 Сводная таблица по сервисам

| Сервис | Нужен ли аккаунт? | Есть ли прямой веб-сокет? | Что мониторит |
| :--- | :---: | :---: | :--- |
| **Bluesky** | ❌ **НЕТ (0 ключей)** | ✅ **Да (Jetstream Firehose)** | 100% всех публичных постов в мире в реальном времени |
| **Reddit** | ✅ Да (существующий) | ✅ **Да (Live Stream)** | Все посты из `r/all` или списка сабреддитов |
| **Telegram (Парсер)** | ✅ Да (существующий) | ✅ **Да (MTProto Socket)** | Все группы, чаты и каналы, в которых ты состоишь |
| **Telegram (Бот)** | ✅ Да | ✅ Да (Telegram Bot API) | Личный чат или закрытый канал для мгновенных алертов |
| **Discord** | ✅ Да (существующий) | ✅ **Да (Gateway WebSocket)** | Все серверы и каналы, где есть бот или твой аккаунт |
| **Slack** | ✅ Да (существующий) | ✅ **Да (Socket Mode)** | Воркспейсы и каналы (#seo, #growth, #saas) |

---

## 1. 🦋 Bluesky (Ключи НЕ нужны!)
* **Аккаунт:** **НЕ ТРЕБУЕТСЯ** для чтения.
* **Как работает сокет:** Bluesky построен на открытом протоколе AT Protocol. В проект `SoketAEO` уже встроен публичный сокет **Jetstream Firehose**:
  `wss://jetstream2.us-east.bsky.network/subscribe?wantedCollections=app.bsky.feed.post`
* **Что он делает:** Перехватывает **каждый пост в мире** в миллисекунду его публикации, проверяет ключевые слова (AEO, GEO, ChatGPT SEO, Target Ads) и моментально присылает лид.
* **Что заполнять в `.env`:** Поля `BLUESKY_HANDLE` и `BLUESKY_APP_PASSWORD` можно оставить **пустыми**!

---

## 2. 🤖 Telegram Bot (Куда слать алерты о лидах)

### Шаг 1: Создание бота через @BotFather
1. Открой Telegram и найди бота [@BotFather](https://t.me/BotFather).
2. Нажми **Start** и отправь команду `/newbot`.
3. Введи имя бота (например: `Soket Lead Alert`).
4. Введи юзернейм бота (должен заканчиваться на `bot`, например: `soketaeo_leads_bot`).
5. Скопируй полученный **HTTP API Token** (формат: `7123456789:AAHk...`).
   👉 Вставь в `.env` в `TELEGRAM_NOTIFY_BOT_TOKEN`.
6. Обязательно нажми на ссылку на своего бота и нажми **Start**, чтобы бот имел право писать тебе.

### Шаг 2: Узнать свой Chat ID
1. В Telegram найди бота [@userinfobot](https://t.me/userinfobot) (или [@raw_data_bot](https://t.me/raw_data_bot)).
2. Нажми **Start**. Бот пришлет твой цифровой `Id` (например: `584920194`).
   *(Если хочешь слать в закрытую группу — добавь бота в группу, напиши что-то, и скопируй ID группы, он начинается с `-100...`)*.
   👉 Вставь в `.env` в `TELEGRAM_NOTIFY_CHAT_ID`.

---

## 3. 📱 Telegram User Client (Чтение твоих групп через Telethon)

Это позволяет слушать **все чаты и группы**, в которые ты вступишь, в режиме реального времени через постоянный бинарный сокет MTProto.

1. Зайди на официальный портал: **[https://my.telegram.org](https://my.telegram.org)**.
2. Введи свой номер телефона в международном формате (например, `+7701...` или `+7999...`).
3. В Telegram тебе придет сервисный код авторизации — скопируй его и войди на сайт.
4. Нажми на **"API development tools"**.
5. Заполни форму (можно написать любые названия):
   - **App title:** `SoketAEO`
   - **Short name:** `soketaeo`
   - **Platform:** `Desktop`
6. Нажми **"Create application"**.
7. Ты получишь:
   - **`App api_id`** (число, например `28471920`) ➔ вставь в `TELEGRAM_API_ID`.
   - **`App api_hash`** (строка из 32 символов) ➔ вставь в `TELEGRAM_API_HASH`.
   - Твой номер телефона ➔ вставь в `TELEGRAM_PHONE`.

---

## 4. 🔴 Reddit API (Мониторинг постов и r/all)

Reddit позволяет через сокетный стрим слушать как конкретные сабреддиты (`SEO`, `SaaS`, `startups`), так и вообще весь Reddit (`r/all`).

1. Зайди на страницу приложений: **[https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)** (убедись, что залогинен).
2. Прокрути страницу в самый низ и нажми кнопку **"are you a developer? create an app..."** (или **"create another app..."**).
3. Заполни поля:
   - **name:** `soketaeo`
   - **тип (выбери радиокнопку):** обязательно **`script`**!
   - **description:** `lead search`
   - **about url:** (оставь пустым)
   - **redirect uri:** `http://localhost:8080` (обязательно написать этот адрес).
4. Нажми **"create app"**.
5. Получение ключей:
   - **Client ID:** находится прямо под надписью *"personal use script"* (набор букв и цифр, например `k8xL_9QwerTY12`).
     👉 Вставь в `REDDIT_CLIENT_ID`.
   - **Client Secret:** строка напротив поля `secret:` (например `98234jkhsdf89234jh_kjh`).
     👉 Вставь в `REDDIT_CLIENT_SECRET`.
   - `REDDIT_USER_AGENT`: напиши `soketaeo:lead_finder:v1.0 (by /u/твой_логин_на_реддит)`.

---

## 5. 🎮 Discord (Мониторинг серверов)

### Вариант 1: Через официального Бота (Рекомендуется)
1. Открой **[Discord Developer Portal](https://discord.com/developers/applications)**.
2. Нажми **"New Application"** в правом верхнем углу ➔ введи имя `SoketAEO` ➔ Create.
3. В левом меню перейди во вкладку **"Bot"**.
4. Нажми **"Reset Token"** (или **"Copy Token"**) ➔ это твой `DISCORD_TOKEN`.
5. Прокрути чуть ниже до раздела **"Privileged Gateway Intents"**:
   - ✅ Включи **`Message Content Intent`** (ОБЯЗАТЕЛЬНО, иначе бот не видит текст сообщений).
   - ✅ Включи **`Server Members Intent`**.
6. Нажми **"Save Changes"**.
7. Чтобы добавить бота на сервер: В левом меню **OAuth2** ➔ **URL Generator** ➔ выбери scope `bot` ➔ permissions `Read Messages/View Channels`, `Read Message History` ➔ скопируй сгенерированную ссылку и открой в браузере.

### Вариант 2: Через User Token (для серверов, куда нельзя пригласить бота)
1. Открой Discord в веб-браузере Google Chrome.
2. Нажми `F12` (Инструменты разработчика) ➔ вкладка **Network**.
3. Кликни на любой канал в Discord.
4. В списке сетевых запросов найди любой запрос к `api/v9/...` ➔ найди заголовок **`Authorization`**.
5. Скопируй значение токена ➔ вставь в `DISCORD_TOKEN`, а параметр `DISCORD_IS_USER_TOKEN` установи в `true`.

---

## 6. 💼 Slack (Мониторинг комьюнити-воркспейсов)

Slack использует **Socket Mode** — постоянное WebSocket-соединение без необходимости иметь публичный белый IP-адрес.

1. Зайди на **[https://api.slack.com/apps](https://api.slack.com/apps)**.
2. Нажми **"Create New App"** ➔ выбери **"From scratch"**.
3. Назови приложение `SoketAEO` и выбери нужный воркспейс.
4. В левом меню нажми **"Socket Mode"** ➔ переключи тумблер в **Enable Socket Mode**:
   - Появится окно создания App-Level токена. Назови его `socket` и нажми **Generate**.
   - Скопируй токен (начинается на `xapp-...`).
   👉 Вставь в `SLACK_APP_TOKEN`.
5. В левом меню перейди в **"OAuth & Permissions"**:
   - Прокрути до **"Bot Token Scopes"** и добавь:
     - `channels:history` (читать публичные каналы)
     - `channels:read`
     - `groups:history` (читать приватные каналы)
     - `groups:read`
6. Прокрути вверх этой же страницы и нажми **"Install to Workspace"** ➔ нажми **Allow**.
7. Скопируй **Bot User OAuth Token** (начинается на `xoxb-...`).
   👉 Вставь в `SLACK_BOT_TOKEN`.

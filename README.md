# 🚀 SoketAEO (Multi-Source Lead Aggregator)

**SoketAEO** — это высокоскоростной асинхронный сокет-сервис для мониторинга в реальном времени сообщений, постов и вакансий из **Telegram, Reddit, Bluesky, Discord и Slack**.

Сервис отслеживает запросы на услуги:
* 🤖 **AEO / GEO / AI SEO**: "how to rank in ChatGPT", "Perplexity optimization", "GEO specialist", "SearchGPT ranking", "AI search".
* 🎯 **Target Ads (US / Global / RU)**: Запуск таргетированной рекламы, Meta/FB Ads, Google Ads в США, Европе, РФ.
* 💼 **SaaS Founders & Growth**: Прямые лиды от основателей и маркетологов.

---

## 🏗 Архитектура

```
[ Telegram Groups (Telethon) ]  ──────┐
[ Reddit Stream (PRAW API)   ]  ──────┤
[ Bluesky Jetstream (Firehose)] ──────┼──► [ Keyword Matcher / Filter ] ──► [ Telegram Alert Bot / Channel ]
[ Discord Gateway (Events)   ]  ──────┤
[ Slack Socket Mode          ]  ──────┘
```

---

## 🔑 Необходимые ключи (Credentials) & Где их взять

| Платформа | Нужные ключи | Где получить |
| :--- | :--- | :--- |
| **Telegram (Уведомления)** | `TELEGRAM_NOTIFY_BOT_TOKEN`<br>`TELEGRAM_NOTIFY_CHAT_ID` | 1. [@BotFather](https://t.me/BotFather) -> `/newbot`<br>2. [@userinfobot](https://t.me/userinfobot) -> узнать свой ID |
| **Telegram (Парсер чатов)** | `TELEGRAM_API_ID`<br>`TELEGRAM_API_HASH`<br>`TELEGRAM_PHONE` | 1. Зайти на [my.telegram.org](https://my.telegram.org)<br>2. Раздел **API development tools**<br>3. Создать приложение |
| **Reddit** | `REDDIT_CLIENT_ID`<br>`REDDIT_CLIENT_SECRET`<br>`REDDIT_USER_AGENT` | 1. [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)<br>2. Кнопка **create another app...**<br>3. Выбрать тип **script**, ввести redirect URI `http://localhost:8080` |
| **Bluesky** | `BLUESKY_HANDLE`<br>`BLUESKY_APP_PASSWORD` | 1. Зарегистрироваться на [bsky.app](https://bsky.app)<br>2. **Settings** -> **Privacy and Security** -> **App Passwords**<br>*(Jetstream Firehose слушает публичную ленту даже без пароля!)* |
| **Discord** | `DISCORD_TOKEN` | 1. [discord.com/developers/applications](https://discord.com/developers/applications)<br>2. Создать бота и включить **Message Content Intent**<br>*(Либо использовать User Token для существующих серверов)* |
| **Slack** | `SLACK_BOT_TOKEN`<br>`SLACK_APP_TOKEN` | 1. [api.slack.com/apps](https://api.slack.com/apps)<br>2. Включить **Socket Mode** и добавить permissions `channels:history`, `groups:history` |

---

## 🛡 Лимиты и безопасность (Anti-Ban Guide)

| Платформа | Макс. групп/серверов | Лимит вступлений в день | Правила безопасности |
| :--- | :--- | :--- | :--- |
| **Telegram** | 500 (обычный) / 1000 (Premium) | **10–15 групп в сутки** (новые аккаунты: 3–5) | Чтение чатов через Telethon полностью пассивное и **не банится**, если не спамить в ответ в личку автоматически. Отвечать вручную. |
| **Reddit** | Неограниченно subreddits в потоке | Чтение через API: **60–100 запросов в минуту** | Официальный PRAW API полностью легален. Стрим `subreddit.stream.submissions()` читает ленту без риска бана. |
| **Bluesky** | Весь мировой поток через Firehose | Неограниченно | Использует публичный сокет Jetstream. Бан невозможен. |
| **Discord** | 100 серверов (обычный) / 200 (Nitro) | **3–5 серверов в сутки** | При использовании User Token нельзя делать частые запросы (Discord запрещает селф-ботов). Читать пассивно через Gateway. |
| **Slack** | Неограниченно воркспейсов | **1–2 воркспейса в день** | В каждый воркспейс нужно вступать по инвайту и мониторить каналы `#general`, `#seo`, `#growth`. |

---

## 🚀 Быстрый старт

1. Склонировать репозиторий:
```bash
git clone https://github.com/amanvelikiigmailcom/sokettg.git soketaeo
cd soketaeo
```

2. Установить зависимости:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Настроить окружение:
```bash
cp .env.example .env
# Отредактировать .env и вставить полученные ключи
```

4. Запустить сервис:
```bash
python3 -m src.main
```

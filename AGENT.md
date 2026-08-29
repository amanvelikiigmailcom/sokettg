# AGENT.md — Project Overview & Agent Instructions

## 📌 Project: SoketAEO
**SoketAEO** is an asynchronous real-time lead generation aggregator and socket daemon designed to monitor multiple social platforms and community channels for high-intent client requests related to:
1. **AEO / GEO & AI SEO**: Optimizing brand presence in LLM answer engines (ChatGPT, Perplexity, Claude, SearchGPT).
2. **Target Advertising**: Meta / Facebook Ads, Google Ads / PPC targeting US, global, and Russian markets.

---

## 🏗 Architecture & Tech Stack

- **Language & Runtime**: Python 3.10+ (AsyncIO)
- **Telegram Monitoring**: Telethon (MTProto client for passive listening of user groups & channels)
- **Reddit Monitoring**: `asyncpraw` (Real-time submission stream across target subreddits)
- **Bluesky Monitoring**: `websockets` connected directly to public Jetstream Firehose (`wss://jetstream2.us-east.bsky.network`)
- **Discord Monitoring**: `discord.py` (Gateway event listener)
- **Slack Monitoring**: `slack_sdk` (Socket Mode client for subscribed workspaces)
- **Alert Dispatcher**: `aiohttp` Telegram Bot API notifier (HTML formatted alerts with direct deep-links)
- **Configuration**: `pydantic` + `python-dotenv`

---

## 📁 Repository Structure

```
soketaeo/
├── .env                       # Active credentials (IGNORED IN GIT)
├── .env.example               # Template for credentials
├── .gitignore                 # Excludes .env, *.session, logs, caches
├── requirements.txt           # Python dependencies
├── AGENT.md                   # Instructions for AI agents (this file)
├── CLAUDE.md                  # Context file for Claude Code
├── README.md                  # Human-readable guide & anti-ban rules
└── src/
    ├── config.py              # Configuration loader & validator
    ├── main.py                # Concurrent AsyncIO runner for all listeners
    ├── listeners/             # Platform socket & event listeners
    │   ├── telegram_listener.py   # Telethon client for joined groups
    │   ├── reddit_listener.py     # Subreddit stream listener
    │   ├── bluesky_listener.py    # Jetstream firehose listener
    │   ├── discord_listener.py    # Discord gateway listener
    │   └── slack_listener.py      # Slack socket mode client
    ├── matcher/
    │   └── keyword_matcher.py # Fast category matcher & regex/substring engine
    ├── notifier/
    │   └── telegram_notifier.py # Real-time alert sender to Telegram
    └── storage/
        └── db.py              # Deduplication & event persistence (planned)
```

---

## ⚙️ Environment Variables (`.env`)

The system uses `.env` for secrets. Any unconfigured service is automatically skipped at runtime without crashing other listeners.

| Key | Description |
| :--- | :--- |
| `TELEGRAM_NOTIFY_BOT_TOKEN` | Bot token from @BotFather for sending alerts |
| `TELEGRAM_NOTIFY_CHAT_ID` | Telegram User ID or Channel ID to receive alerts |
| `TELEGRAM_API_ID` / `TELEGRAM_API_HASH` | Credentials from my.telegram.org for Telethon |
| `TELEGRAM_PHONE` | Phone number for user session |
| `REDDIT_CLIENT_ID` / `REDDIT_CLIENT_SECRET` | Reddit Script App credentials |
| `REDDIT_SUBREDDITS` | Comma-separated subreddits to monitor |
| `BLUESKY_HANDLE` / `BLUESKY_APP_PASSWORD` | Optional (Jetstream works publicly) |
| `DISCORD_TOKEN` | Bot or User token |
| `DISCORD_IS_USER_TOKEN` | Boolean (`true` or `false`) |
| `SLACK_BOT_TOKEN` / `SLACK_APP_TOKEN` | Slack App credentials |
| `KEYWORDS_AEO_GEO` | Comma-separated keywords for AEO/GEO intent |
| `KEYWORDS_TARGET` | Comma-separated keywords for Ad/Targeting intent |

---

## 🎯 Current Implementation Status

- [x] Initial repository scaffolding & `.gitignore`
- [x] Pydantic configuration loader (`src/config.py`)
- [x] Keyword matching engine with category assignment (`src/matcher/keyword_matcher.py`)
- [x] Async Telegram alert notifier (`src/notifier/telegram_notifier.py`)
- [x] Bluesky Jetstream WebSocket firehose listener (`src/listeners/bluesky_listener.py`)
- [x] Telegram Telethon group listener (`src/listeners/telegram_listener.py`)
- [x] Reddit AsyncPRAW stream listener (`src/listeners/reddit_listener.py`)
- [x] Discord Gateway listener (`src/listeners/discord_listener.py`)
- [x] Slack Socket Mode listener (`src/listeners/slack_listener.py`)
- [x] Async concurrent runner (`src/main.py`)

---

## 🚀 Roadmap & Next Steps for Future Tasks

1. **Message Deduplication**: Add SQLite/aiosqlite database in `src/storage/db.py` to prevent duplicate alerts if the same lead is posted across multiple groups.
2. **AI Lead Classifier (LLM Scoring)**: Optional integration with Gemini / Claude / OpenAI to score lead intent (High Intent Client vs Job Seeker vs Self-promotion) before notifying.
3. **Auto-Summary & Pitch Suggestion**: Include a 1-sentence draft reply / pitch in the Telegram alert.
4. **Web UI / Dashboard**: Optional lightweight FastAPI dashboard for viewing captured leads history.

---

## 🛠 Useful Commands

```bash
# Setup environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run all active listeners
python3 -m src.main
```

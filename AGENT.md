# AGENT.md — Primary Single Source of Truth & Instructions

> 📌 **Note for all AI agents**: This file is the definitive guide and source of truth for the **SoketAEO** project. All agents (including Claude, Antigravity, etc.) must read and follow the specifications, rules, and roadmap laid out here.

---

## 🎯 1. Project Mission & Goals
**SoketAEO** is a high-speed real-time lead generation engine and socket daemon. It aggregates streams and events from multiple platforms (**Telegram, Reddit, Bluesky, Discord, Slack**) to catch high-intent client inquiries for:
1. **AEO / GEO & AI SEO**: Optimizing websites and brands to be cited and recommended by AI answer engines (ChatGPT, Perplexity, Claude, SearchGPT).
2. **Target Advertising & Media Buying**: Running targeted ad campaigns (Meta / Facebook Ads, Google Ads / PPC) in the US, global tier-1 markets, and RU.
3. **SaaS & Founder Growth Inquiries**: Identifying founders asking questions like *"how to rank in ChatGPT"*, *"how to get traffic in US"*, *"looking for media buyer/targetologist"*.

---

## 🏗 2. Tech Stack & Architecture

- **Language & Runtime**: Python 3.10+ (AsyncIO)
- **Telegram Monitoring**: Telethon (MTProto client for passive listening of user groups & channels)
- **Reddit Monitoring**: `asyncpraw` (Real-time submission stream across target subreddits)
- **Bluesky Monitoring**: `websockets` connected directly to public Jetstream Firehose (`wss://jetstream2.us-east.bsky.network`)
- **Discord Monitoring**: `discord.py` (Gateway event listener for channels)
- **Slack Monitoring**: `slack_sdk` (Socket Mode client for subscribed workspaces)
- **Alert Dispatcher**: `aiohttp` Telegram Bot API notifier (HTML formatted alerts with direct deep-links)
- **Configuration**: `pydantic` + `python-dotenv`
- **Persistence & Deduplication**: SQLite (`aiosqlite`) for deduplication

```
[ Telegram Groups (Telethon) ]  ──────┐
[ Reddit Stream (PRAW API)   ]  ──────┤
[ Bluesky Jetstream (Firehose)] ──────┼──► [ Keyword Matcher ] ──► [ Deduplication DB ] ──► [ Telegram Alert Bot ]
[ Discord Gateway (Events)   ]  ──────┤
[ Slack Socket Mode          ]  ──────┘
```

---

## 📁 3. Project Structure

```
soketaeo/
├── .env                       # Active credentials (IGNORED IN GIT)
├── .env.example               # Template for credentials
├── .gitignore                 # Excludes .env, *.session, logs, caches
├── requirements.txt           # Python dependencies
├── AGENT.md                   # Single source of truth (this file)
├── CLAUDE.md                  # Claude redirect to AGENT.md
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
        └── db.py              # Deduplication & event persistence
```

---

## 📋 4. Detailed Roadmap & Step-by-Step Plan

### ✅ Phase 1: Core Architecture & Scaffolding (COMPLETED)
- [x] Initialized project structure and Git repository.
- [x] Implemented modular listener architecture for Telegram, Reddit, Bluesky, Discord, and Slack.
- [x] Built instant keyword matching engine (`src/matcher/keyword_matcher.py`).
- [x] Implemented Telegram alert notification system with rich HTML formatting (`src/notifier/telegram_notifier.py`).
- [x] Created Bluesky Jetstream Firehose listener (`src/listeners/bluesky_listener.py`).
- [x] Created `.env` template and `.gitignore` security rules.

### 🔄 Phase 2: Credentials & Connection Validation (IN PROGRESS)
- [ ] User fills in API keys and tokens in `.env`.
- [ ] Test individual socket listeners on real live streams.
- [ ] Connect and push to GitHub repository with valid Personal Access Token.

### 🚀 Phase 3: Deduplication & Message Storage (UPCOMING)
- [ ] Create `src/storage/db.py` using `aiosqlite`.
- [ ] Implement message hash / URL deduplication with a 48-hour TTL window to prevent repetitive notifications when a user crossposts across multiple groups/platforms.

### 🧠 Phase 4: AI Lead Scoring & Intent Filtering (UPCOMING)
- [ ] Implement LLM filter (Gemini / OpenAI / Claude) to classify post intent:
  - **HOT LEAD**: Client actively looking to hire an AEO/GEO agency or target ad specialist.
  - **WARM LEAD**: Founder asking advice on how to rank in ChatGPT or scale ads.
  - **COLD / NOISE**: Specialist selling services or generic news (filtered out).
- [ ] Generate 1-sentence recommended personalized outreach pitch inside the Telegram notification.

### ⚡ Phase 5: Group Expansion & Anti-Ban Management (UPCOMING)
- [ ] Add auto-discovery of new relevant Telegram chats, subreddits, and Discord servers.
- [ ] Strictly enforce safety limits (10–15 Telegram groups/day, 3–5 Discord servers/day).

---

## 🔒 5. Development & Security Rules
1. **Never commit `.env` or `*.session` files**: Secrets and user sessions must remain strictly local.
2. **Graceful Degradation**: If any service's credentials are empty in `.env`, its listener must log an informational message and skip initialization without blocking other streams.
3. **Fully Async**: All network I/O, socket connections, and database operations must use non-blocking `asyncio`.
4. **Resilient Reconnections**: Every listener loop must handle disconnects gracefully with exponential backoff / retry.

---

## 🛠 6. Quick Commands

```bash
# Setup virtualenv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run all active listeners
python3 -m src.main
```

# CLAUDE.md — Context & Instructions for Claude

## Project Context
This is **SoketAEO**, an asynchronous Python daemon that monitors real-time sockets and streams (Telegram, Reddit, Bluesky, Discord, Slack) to capture business leads for **AEO/GEO (Answer Engine Optimization)** and **Target Ads (US/RU)**.

For full architectural details, roadmap, and design notes, refer to [`AGENT.md`](./AGENT.md).

## Development Guidelines & Rules
1. **Never commit `.env` or `*.session` files**: Secrets and user sessions must remain strictly local.
2. **Graceful Degradation**: If a service's credentials are not present in `.env`, its listener must log a warning and skip initialization without blocking the event loop.
3. **Async / Non-blocking**: All networking, socket streams, and database calls must be fully async (using `asyncio`, `aiohttp`, `asyncpraw`, `telethon`, etc.).
4. **Error Handling**: Listeners must have auto-reconnect logic in loops so that a temporary network disconnect does not kill the entire daemon.

## Quick Commands
- **Install deps**: `pip install -r requirements.txt`
- **Run daemon**: `python3 -m src.main`
- **Check environment**: View or update [`.env`](./.env)

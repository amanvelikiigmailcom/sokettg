import os
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class Config(BaseModel):
    # Telegram Notifications
    notify_bot_token: str = os.getenv("TELEGRAM_NOTIFY_BOT_TOKEN", "")
    notify_chat_id: str = os.getenv("TELEGRAM_NOTIFY_CHAT_ID", "")

    # Telegram Parser (Telethon)
    tg_api_id: int = int(os.getenv("TELEGRAM_API_ID", "0")) if os.getenv("TELEGRAM_API_ID") else 0
    tg_api_hash: str = os.getenv("TELEGRAM_API_HASH", "")
    tg_phone: str = os.getenv("TELEGRAM_PHONE", "")

    # Reddit
    reddit_client_id: str = os.getenv("REDDIT_CLIENT_ID", "")
    reddit_client_secret: str = os.getenv("REDDIT_CLIENT_SECRET", "")
    reddit_user_agent: str = os.getenv("REDDIT_USER_AGENT", "soketaeo:lead_finder:v1.0")
    reddit_subreddits: List[str] = [
        s.strip() for s in os.getenv("REDDIT_SUBREDDITS", "SEO,marketing,SaaS,startups,entrepreneur").split(",") if s.strip()
    ]

    # Bluesky
    bluesky_handle: str = os.getenv("BLUESKY_HANDLE", "")
    bluesky_app_password: str = os.getenv("BLUESKY_APP_PASSWORD", "")

    # Discord
    discord_token: str = os.getenv("DISCORD_TOKEN", "")
    discord_is_user_token: bool = os.getenv("DISCORD_IS_USER_TOKEN", "false").lower() == "true"

    # Slack
    slack_user_token: str = os.getenv("SLACK_USER_TOKEN", "")
    slack_bot_token: str = os.getenv("SLACK_BOT_TOKEN", "")
    slack_app_token: str = os.getenv("SLACK_APP_TOKEN", "")

    # Keywords
    keywords_aeo_geo: List[str] = [
        k.strip().lower() for k in os.getenv("KEYWORDS_AEO_GEO", "AEO,GEO,AI SEO,ChatGPT SEO,rank in ChatGPT").split(",") if k.strip()
    ]
    keywords_target: List[str] = [
        k.strip().lower() for k in os.getenv("KEYWORDS_TARGET", "targetologist,target ads,facebook ads,таргетолог,таргет сша").split(",") if k.strip()
    ]

config = Config()

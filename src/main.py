import asyncio
import sys
from loguru import logger
from src.matcher.keyword_matcher import KeywordMatcher
from src.notifier.telegram_notifier import TelegramNotifier
from src.listeners.bluesky_listener import BlueskyListener
from src.listeners.telegram_listener import TelegramListener
from src.listeners.reddit_listener import RedditListener
from src.listeners.discord_listener import DiscordListener
from src.listeners.slack_listener import SlackListener

logger.remove()
logger.add(sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>", colorize=True)

async def main():
    logger.info("==========================================")
    logger.info("   Starting SOKETAEO Lead Aggregator      ")
    logger.info("==========================================")

    matcher = KeywordMatcher()
    notifier = TelegramNotifier()

    listeners = [
        BlueskyListener(matcher, notifier).start(),
        TelegramListener(matcher, notifier).start(),
        RedditListener(matcher, notifier).start(),
        DiscordListener(matcher, notifier).start(),
        SlackListener(matcher, notifier).start(),
    ]

    await asyncio.gather(*listeners, return_exceptions=True)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Shutting down SOKETAEO...")

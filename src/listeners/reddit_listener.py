import asyncio
from loguru import logger
import asyncpraw
from src.config import config
from src.matcher.keyword_matcher import KeywordMatcher
from src.notifier.telegram_notifier import TelegramNotifier

class RedditListener:
    def __init__(self, matcher: KeywordMatcher, notifier: TelegramNotifier):
        self.matcher = matcher
        self.notifier = notifier

    async def start(self):
        if not config.reddit_client_id or not config.reddit_client_secret:
            logger.warning("[Reddit] Client ID/Secret not provided. Reddit listener disabled.")
            return

        async with asyncpraw.Reddit(
            client_id=config.reddit_client_id,
            client_secret=config.reddit_client_secret,
            user_agent=config.reddit_user_agent,
        ) as reddit:
            subs_str = "+".join(config.reddit_subreddits)
            subreddit = await reddit.subreddit(subs_str)
            logger.info(f"[Reddit] Streaming submissions from: {subs_str}")

            async for submission in subreddit.stream.submissions(skip_existing=True):
                full_text = f"{submission.title}\n{submission.selftext}"
                res = self.matcher.match(full_text)
                if res.is_match:
                    logger.info(f"[Reddit] Match found in r/{submission.subreddit.display_name} for '{res.matched_keyword}'")
                    await self.notifier.send_lead(
                        source=f"Reddit (r/{submission.subreddit.display_name})",
                        category=res.category or "General",
                        keyword=res.matched_keyword or "",
                        author_name=str(submission.author),
                        content=full_text,
                        url=f"https://reddit.com{submission.permalink}"
                    )

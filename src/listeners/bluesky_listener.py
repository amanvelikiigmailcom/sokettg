import json
import asyncio
import websockets
from loguru import logger
from src.matcher.keyword_matcher import KeywordMatcher
from src.notifier.telegram_notifier import TelegramNotifier

class BlueskyListener:
    # Bluesky Jetstream public firehose (real-time stream of all public posts)
    JETSTREAM_URL = "wss://jetstream2.us-east.bsky.network/subscribe?wantedCollections=app.bsky.feed.post"

    def __init__(self, matcher: KeywordMatcher, notifier: TelegramNotifier):
        self.matcher = matcher
        self.notifier = notifier

    async def start(self):
        logger.info("[Bluesky] Starting Jetstream Firehose listener...")
        while True:
            try:
                async with websockets.connect(self.JETSTREAM_URL) as ws:
                    logger.success("[Bluesky] Connected to Jetstream Firehose!")
                    async for message in ws:
                        try:
                            data = json.loads(message)
                            if data.get("kind") == "commit" and data.get("commit", {}).get("operation") == "create":
                                record = data.get("commit", {}).get("record", {})
                                text = record.get("text", "")
                                if not text:
                                    continue

                                res = self.matcher.match(text)
                                if res.is_match:
                                    did = data.get("did", "")
                                    rkey = data.get("commit", {}).get("rkey", "")
                                    post_url = f"https://bsky.app/profile/{did}/post/{rkey}" if did and rkey else ""
                                    logger.info(f"[Bluesky] Match found for keyword: {res.matched_keyword}")
                                    await self.notifier.send_lead(
                                        source="Bluesky (Firehose)",
                                        category=res.category or "General",
                                        keyword=res.matched_keyword or "",
                                        author_name=did,
                                        content=text,
                                        url=post_url
                                    )
                        except Exception as parse_err:
                            continue
            except Exception as e:
                logger.error(f"[Bluesky] Connection error: {e}. Reconnecting in 5s...")
                await asyncio.sleep(5)

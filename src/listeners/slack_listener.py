import asyncio
from loguru import logger
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.socket_mode.aiohttp import SocketModeClient
from src.config import config
from src.matcher.keyword_matcher import KeywordMatcher
from src.notifier.telegram_notifier import TelegramNotifier

class SlackListener:
    def __init__(self, matcher: KeywordMatcher, notifier: TelegramNotifier):
        self.matcher = matcher
        self.notifier = notifier

    async def start(self):
        if not config.slack_app_token and not config.slack_bot_token and not config.slack_user_token:
            logger.warning("[Slack] Slack tokens not configured. Slack listener disabled.")
            return

        if config.slack_app_token and config.slack_bot_token:
            # Socket Mode
            client = AsyncWebClient(token=config.slack_bot_token)
            socket_client = SocketModeClient(app_token=config.slack_app_token, web_client=client)

            async def process(client: SocketModeClient, req):
                if req.type == "events_api":
                    event = req.payload.get("event", {})
                    if event.get("type") == "message" and "subtype" not in event:
                        text = event.get("text", "")
                        res = self.matcher.match(text)
                        if res.is_match:
                            user_id = event.get("user", "Unknown")
                            channel_id = event.get("channel", "Unknown")
                            logger.info(f"[Slack] Match found for keyword: {res.matched_keyword}")
                            await self.notifier.send_lead(
                                source=f"Slack (Channel {channel_id})",
                                category=res.category or "General",
                                keyword=res.matched_keyword or "",
                                author=user_id,
                                content=text,
                                url=""
                            )
            socket_client.socket_mode_request_listeners.append(process)
            logger.info("[Slack] Starting Socket Mode client...")
            await socket_client.connect()
        else:
            logger.info("[Slack] Polling or user token configured.")

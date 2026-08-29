import asyncio
from loguru import logger
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.socket_mode.aiohttp import SocketModeClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest
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

            async def process(client: SocketModeClient, req: SocketModeRequest):
                if req.type == "events_api":
                    # Acknowledge the request anyway
                    response = SocketModeResponse(envelope_id=req.envelope_id)
                    await client.send_socket_mode_response(response)

                    event = req.payload.get("event", {})
                    if event.get("type") == "message" and "subtype" not in event:
                        text = event.get("text", "")
                        res = self.matcher.match(text)
                        
                        # Only allow English matches for Slack
                        if res.is_match and res.matched_keyword.isascii():
                            user_id = event.get("user", "Unknown")
                            channel_id = event.get("channel", "Unknown")
                            
                            # Retrieve user info from Slack API
                            author_name = user_id
                            author_username = ""
                            try:
                                user_info = await client.web_client.users_info(user=user_id)
                                if user_info and user_info.get("ok"):
                                    u = user_info["user"]
                                    author_name = u.get("real_name") or u.get("name") or user_id
                                    author_username = u.get("name", "")
                            except Exception as e:
                                logger.error(f"[Slack] Error fetching user info: {e}")

                            logger.info(f"[Slack] Match found for keyword: {res.matched_keyword}")
                            
                            await self.notifier.send_lead(
                                source=f"Slack",
                                source_id=channel_id,
                                category=res.category or "General",
                                keyword=res.matched_keyword or "",
                                author_name=author_name,
                                author_username=author_username,
                                author_id=user_id,
                                is_premium=False,
                                content=text,
                                url=""
                            )
            socket_client.socket_mode_request_listeners.append(process)
            logger.info("[Slack] Starting Socket Mode client...")
            await socket_client.connect()
            # Keep it running
            await asyncio.sleep(float('inf'))
        else:
            logger.info("[Slack] Polling or user token configured.")

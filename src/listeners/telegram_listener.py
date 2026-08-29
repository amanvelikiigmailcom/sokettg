import asyncio
from loguru import logger
from telethon import TelegramClient, events
from src.config import config
from src.matcher.keyword_matcher import KeywordMatcher
from src.notifier.telegram_notifier import TelegramNotifier

class TelegramListener:
    def __init__(self, matcher: KeywordMatcher, notifier: TelegramNotifier):
        self.matcher = matcher
        self.notifier = notifier
        self.client = None

    async def start(self):
        if not config.tg_api_id or not config.tg_api_hash:
            logger.warning("[Telegram] TG_API_ID or TG_API_HASH not provided. Telegram listener disabled.")
            return

        session_name = "soketaeo_session"
        self.client = TelegramClient(session_name, config.tg_api_id, config.tg_api_hash)

        @self.client.on(events.NewMessage(incoming=True))
        async def handler(event):
            try:
                chat = await event.get_chat()
                
                # Ignore our own notification chat
                if str(chat.id) == str(config.notify_chat_id):
                    return

                sender = await event.get_sender()
                
                # Ignore bots (prevents infinite loops if bots reply)
                if getattr(sender, 'bot', False):
                    return

                text = event.raw_text or ""
                res = self.matcher.match(text)
                
                if res.is_match:
                    chat_title = getattr(chat, 'title', getattr(chat, 'username', 'Private/Group'))
                    sender_name = getattr(sender, 'username', getattr(sender, 'first_name', 'Unknown'))

                    # Build link 
                    msg_link = ""
                    if getattr(chat, 'username', None):
                        # Public group link
                        msg_link = f"https://t.me/{chat.username}/{event.id}"
                    else:
                        # Private supergroup link
                        chat_id_str = str(chat.id)
                        if chat_id_str.startswith("-100"):
                            chat_id_str = chat_id_str[4:]
                        msg_link = f"https://t.me/c/{chat_id_str}/{event.id}"

                    logger.info(f"[Telegram] Lead detected in '{chat_title}' by @{sender_name} for '{res.matched_keyword}'")
                    await self.notifier.send_lead(
                        source=f"Telegram ({chat_title})",
                        category=res.category or "General",
                        keyword=res.matched_keyword or "",
                        author=f"@{sender_name}" if sender_name else "Anonymous",
                        content=text,
                        url=msg_link
                    )
            except Exception as e:
                logger.error(f"[Telegram] Error processing message: {e}")

        logger.info("[Telegram] Starting Telethon client...")
        await self.client.start(phone=config.tg_phone if config.tg_phone else None)
        logger.success("[Telegram] Telethon client connected and listening!")
        await self.client.run_until_disconnected()

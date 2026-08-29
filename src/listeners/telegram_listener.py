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
                # 1. Ignore private personal messages (DMs)
                if event.is_private:
                    return

                chat = await event.get_chat()
                
                # Ignore our own notification chat to avoid infinite loops
                if str(chat.id) == str(config.notify_chat_id):
                    return

                sender = await event.get_sender()
                
                # Ignore bots
                if getattr(sender, 'bot', False):
                    return

                text = event.raw_text or ""
                res = self.matcher.match(text)
                
                if res.is_match:
                    chat_title = getattr(chat, 'title', getattr(chat, 'username', 'Private/Group'))
                    chat_id_str = str(chat.id)
                    
                    # Author info
                    author_name = getattr(sender, 'first_name', '')
                    if getattr(sender, 'last_name', None):
                        author_name += f" {sender.last_name}"
                    author_name = author_name.strip() or "Unknown"
                    
                    author_username = getattr(sender, 'username', '')
                    author_id = str(getattr(sender, 'id', ''))
                    is_premium = getattr(sender, 'premium', False)

                    # Build link 
                    msg_link = ""
                    if getattr(chat, 'username', None):
                        # Public group link
                        msg_link = f"https://t.me/{chat.username}/{event.id}"
                    else:
                        # Private supergroup link
                        clean_chat_id = chat_id_str[4:] if chat_id_str.startswith("-100") else chat_id_str
                        msg_link = f"https://t.me/c/{clean_chat_id}/{event.id}"

                    logger.info(f"[Telegram] Lead detected in '{chat_title}' by {author_name} for '{res.matched_keyword}'")
                    await self.notifier.send_lead(
                        source=f"Telegram ({chat_title})",
                        source_id=chat_id_str,
                        category=res.category or "General",
                        keyword=res.matched_keyword or "",
                        author_name=author_name,
                        author_username=author_username,
                        author_id=author_id,
                        is_premium=is_premium,
                        content=text,
                        url=msg_link
                    )
            except Exception as e:
                logger.error(f"[Telegram] Error processing message: {e}")

        logger.info("[Telegram] Starting Telethon client...")
        await self.client.start(phone=config.tg_phone if config.tg_phone else None)
        logger.success("[Telegram] Telethon client connected and listening!")
        await self.client.run_until_disconnected()

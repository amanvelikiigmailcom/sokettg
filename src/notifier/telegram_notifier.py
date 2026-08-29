import aiohttp
from loguru import logger
from src.config import config

class TelegramNotifier:
    def __init__(self):
        self.bot_token = config.notify_bot_token
        self.chat_id = config.notify_chat_id
        self.thread_id = config.notify_thread_id

    async def send_lead(self, source: str, category: str, keyword: str, content: str, 
                        author_name: str = "Anonymous", author_username: str = "", 
                        author_id: str = "", is_premium: bool = False, source_id: str = "", url: str = ""):
        
        if not self.bot_token or not self.chat_id:
            logger.warning(f"[Notifier] Bot token or chat_id not configured. Lead found from {source}: {content[:60]}...")
            return

        premium_star = " ⭐️" if is_premium else ""
        author_username_str = f" (@{author_username})" if author_username else ""
        source_id_str = f" <code>[{source_id}]</code>" if source_id else ""
        author_id_str = f" <code>[ID: {author_id}]</code>" if author_id else ""
        
        # Make the name clickable via tg://user?id= if we have the ID
        author_link = f"<a href='tg://user?id={author_id}'>{author_name}</a>" if author_id else author_name

        message = (
            f"🔥 <b>НАЙДЕН НОВЫЙ ЛИД!</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📱 <b>Источник:</b> {source}{source_id_str}\n"
            f"🗂 <b>Ниша:</b> {category}\n"
            f"🔑 <b>Сработал ключ:</b> <code>{keyword}</code>\n"
            f"👤 <b>Автор:</b> {author_link}{premium_star}{author_username_str}{author_id_str}\n"
        )
        
        if url:
            message += f"🔗 <a href='{url}'>Перейти к сообщению</a>\n"
        
        message += f"━━━━━━━━━━━━━━━━━━\n\n💬 <b>Текст сообщения:</b>\n<i>{content[:1500]}</i>"

        api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }
        if self.thread_id:
            payload["message_thread_id"] = self.thread_id

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(api_url, json=payload, timeout=10) as resp:
                    if resp.status != 200:
                        err_text = await resp.text()
                        logger.error(f"[Notifier] Telegram API error: {err_text}")
                    else:
                        logger.success(f"[Notifier] Lead sent to Telegram topic ({source})")
        except Exception as e:
            logger.error(f"[Notifier] Failed to send Telegram notification: {e}")

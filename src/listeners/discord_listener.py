import asyncio
import discord
from loguru import logger
from src.config import config
from src.matcher.keyword_matcher import KeywordMatcher
from src.notifier.telegram_notifier import TelegramNotifier

class DiscordListener:
    def __init__(self, matcher: KeywordMatcher, notifier: TelegramNotifier):
        self.matcher = matcher
        self.notifier = notifier

    async def start(self):
        if not config.discord_token:
            logger.warning("[Discord] Discord token not provided. Discord listener disabled.")
            return

        # Use discord.py self-bot fork for user tokens, but standard discord.py doesn't officially support user tokens well anymore.
        # However, we will try with standard discord.py and see if it auths.
        intents = discord.Intents.default()
        intents.message_content = True
        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            logger.success(f"[Discord] Connected as {client.user} across {len(client.guilds)} servers.")

        @client.event
        async def on_message(message):
            if message.author == client.user:
                return

            text = message.content
            res = self.matcher.match(text)
            if res.is_match:
                server_name = message.guild.name if message.guild else "Direct Message"
                channel_name = message.channel.name if hasattr(message.channel, 'name') else "DM"
                guild_id = str(message.guild.id) if message.guild else ""
                
                logger.info(f"[Discord] Lead in {server_name} #{channel_name} for '{res.matched_keyword}'")
                await self.notifier.send_lead(
                    source=f"Discord ({server_name} #{channel_name})",
                    source_id=guild_id,
                    category=res.category or "General",
                    keyword=res.matched_keyword or "",
                    author_name=message.author.display_name,
                    author_username=message.author.name,
                    author_id=str(message.author.id),
                    is_premium=False,
                    content=text,
                    url=message.jump_url
                )

        try:
            logger.info("[Discord] Starting Discord client...")
            await client.start(config.discord_token)
        except Exception as e:
            logger.error(f"[Discord] Discord listener error: {e}")

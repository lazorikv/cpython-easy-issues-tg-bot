import os
import logging
from telegram import Bot
from telegram.error import TelegramError

logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(self) -> None:
        self.token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.channel_id: str = os.getenv("TELEGRAM_CHANNEL_ID", "")
        self.bot: Bot = Bot(token=self.token)
        logger.info("Initialized Telegram bot")
        
    async def send_message(self, message: str) -> bool:
        """Send message to Telegram channel"""
        try:
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=message,
                parse_mode="HTML"
            )
            return True
        except TelegramError as e:
            logger.error(f"Error sending message to Telegram: {e}")
            return False
            
    async def start(self) -> None:
        """Start the bot"""
        logger.info("Starting Telegram bot")
        await self.bot.initialize()
        
    async def stop(self) -> None:
        """Stop the bot"""
        logger.info("Stopping Telegram bot")
        await self.bot.shutdown()

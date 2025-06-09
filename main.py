import asyncio
import logging
from dotenv import load_dotenv
from bot.telegram_bot import TelegramBot
from bot.github import GitHubClient
from bot.scheduler import Scheduler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main() -> None:
    # Load environment variables
    load_dotenv()
    
    # Initialize components
    github_client = GitHubClient()
    telegram_bot = TelegramBot()
    scheduler = Scheduler(github_client, telegram_bot)
    
    try:
        # Start scheduler
        await scheduler.start()
    except Exception as e:
        logger.error(f"Error in main loop: {e}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")

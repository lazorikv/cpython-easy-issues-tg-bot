import os
import asyncio
import logging
from typing import NoReturn
from aiohttp import web
from dotenv import load_dotenv
from bot.github import GitHubClient
from bot.telegram_bot import TelegramBot
from bot.scheduler import Scheduler

# Load environment variables from .env file if it exists
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger: logging.Logger = logging.getLogger(__name__)


async def healthcheck_handler(request: web.Request) -> web.Response:
    """Healthcheck endpoint handler"""
    return web.Response(text="OK")


async def start_background_tasks(app: web.Application) -> None:
    """Start background tasks"""
    github_client: GitHubClient = GitHubClient()
    telegram_bot: TelegramBot = TelegramBot()
    scheduler: Scheduler = Scheduler(github_client, telegram_bot)
    
    # Start the scheduler
    app["scheduler"] = asyncio.create_task(scheduler.start())


async def cleanup_background_tasks(app: web.Application) -> None:
    """Cleanup background tasks"""
    scheduler_task: asyncio.Task = app["scheduler"]
    scheduler_task.cancel()
    try:
        await scheduler_task
    except asyncio.CancelledError:
        pass


async def init_app() -> web.Application:
    """Initialize application"""
    app: web.Application = web.Application()
    app.router.add_get("/", healthcheck_handler)
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    return app


def main() -> NoReturn:
    """Main entry point"""
    try:
        app: web.Application = asyncio.run(init_app())
        web.run_app(
            app,
            host="0.0.0.0",
            port=int(os.getenv("PORT", "8080"))
        )
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        raise SystemExit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

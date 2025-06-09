import os
import logging
import asyncio
from typing import Set
from datetime import datetime, timezone
from bot.database import Database
from bot.github import GitHubClient
from bot.telegram_bot import TelegramBot

logger = logging.getLogger(__name__)


class Scheduler:
    def __init__(self, github_client: GitHubClient, telegram_bot: TelegramBot) -> None:
        self.github_client: GitHubClient = github_client
        self.telegram_bot: TelegramBot = telegram_bot
        self.interval: int = int(os.getenv("CHECK_INTERVAL_MINUTES", 30)) * 60  # Convert minutes to seconds
        
        # Convert minutes to seconds (default 6 hours)
        self.notification_interval: int = int(os.getenv("NOTIFICATION_INTERVAL_MINUTES", 360)) * 60
        self.last_notification_time: float = 0
        self.db: Database = Database()
        self.posted_issues: Set[int] = self.db.get_posted_issues()
        logger.info(
            f"Initialized scheduler with check interval: {self.interval} seconds ({self.interval/60} minutes), "
            f"notification interval: {self.notification_interval/60} minutes"
        )
        
    async def send_no_issues_notification(self) -> None:
        """Send notification about no issues found"""
        current_time: float = datetime.now(timezone.utc).timestamp()
        if current_time - self.last_notification_time >= self.notification_interval:
            message: str = (
                f"📢 No new \"{os.getenv('GITHUB_LABEL', 'easy')}\" issues found in CPython repository today.\n"
                f"Next check in {self.notification_interval/60} minutes."
            )
            if await self.telegram_bot.send_message(message):
                self.last_notification_time = current_time
                logger.info("Sent \"no issues\" notification")
        
    async def check_new_issues(self) -> None:
        """Check for new issues"""
        try:
            logger.info("Starting check for new issues")
            new_issues, latest_issue = await self.github_client.get_new_issues()
            
            if latest_issue:
                logger.info(
                    f"Latest issue: #{latest_issue['number']} - {latest_issue['title']} "
                    f"(created at {latest_issue['created_at']})"
                )
            else:
                logger.info("No issues found for today")
                await self.send_no_issues_notification()
            
            for issue in new_issues:
                if issue["id"] not in self.posted_issues:
                    message = self.github_client.format_issue_message(issue)
                    if await self.telegram_bot.send_message(message):
                        self.posted_issues.add(issue["id"])
                        self.db.add_posted_issue(issue["id"], issue["number"])
                        logger.info(f"Posted issue #{issue['number']}")
                        
        except Exception as e:
            logger.error(f"Error checking new issues: {e}")
            
    async def start(self) -> None:
        """Start the scheduler"""
        logger.info("Starting scheduler")
        await self.telegram_bot.start()
        
        while True:
            await self.check_new_issues()
            logger.info(f"Waiting {self.interval} seconds ({self.interval/60} minutes) before next check")
            await asyncio.sleep(self.interval)

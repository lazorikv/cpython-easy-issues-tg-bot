import os
import logging
import aiohttp
import ssl
import certifi
from typing import List, Dict, Any, Tuple
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


class GitHubClient:
    def __init__(self) -> None:
        self.token: str = os.getenv("GITHUB_TOKEN", "")
        self.owner: str = os.getenv("GITHUB_OWNER", "python")
        self.repo: str = os.getenv("GITHUB_REPO", "cpython")
        self.label: str = os.getenv("GITHUB_LABEL", "easy")
        self.ssl_context: ssl.SSLContext = ssl.create_default_context(cafile=certifi.where())
        self.headers: Dict[str, str] = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {self.token}" if self.token else "",
        }
        logger.info(f"Initialized GitHub client for {self.owner}/{self.repo} with label: {self.label}")
        
    async def get_new_issues(self) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """Get new issues from GitHub"""
        try:
            # Get today's date in UTC
            today: datetime = datetime.now(timezone.utc).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            today_str: str = today.isoformat()

            # Construct query to find issues created today with the specified label
            query: str = (
                f"repo:{self.owner}/{self.repo} "
                f"is:issue "
                f"is:open "
                f"label:{self.label} "
                f"created:>={today_str}"
            )

            logger.info(f"Searching issues with query: {query}")

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://api.github.com/search/issues",
                    params={"q": query},
                    headers=self.headers,
                    ssl=self.ssl_context,
                ) as response:
                    if response.status == 200:
                        data: Dict[str, Any] = await response.json()
                        issues: List[Dict[str, Any]] = data.get("items", [])
                        latest_issue: Dict[str, Any] = issues[0] if issues else {}
                        logger.info(f"Found {len(issues)} new issues")
                        return issues, latest_issue
                    else:
                        error_text: str = await response.text()
                        logger.error(f"GitHub API error: {response.status} - {error_text}")
                        return [], {}

        except Exception as e:
            logger.error(f"Error fetching issues: {e}")
            return [], {}

    # noinspection PyMethodMayBeStatic
    def format_issue_message(self, issue: Dict[str, Any]) -> str:
        """Format issue data into a message"""
        return (
            f"🐍 New Easy Issue Found!\n\n"
            f"📌 Issue #{issue['number']}: {issue['title']}\n"
            f"🔗 Link: {issue['html_url']}\n"
            f"⏰ Created: {issue['created_at']}\n"
            f"👤 Author: {issue['user']['login']}\n"
            f"🏷️ Labels: {', '.join(label['name'] for label in issue['labels'])}"
        )

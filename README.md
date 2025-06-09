# CPython Easy Issues Telegram Bot

Telegram bot for monitoring new issues in the CPython repository with a specified label.

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd cpython-easy-issues-tg-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file with the following variables:
```
TELEGRAM_TOKEN=your_telegram_token_here
TELEGRAM_CHANNEL_ID=your_channel_id_here
CHECK_INTERVAL_MINUTES=30
GITHUB_LABEL=easy
```

4. Initialize the database:
```bash
python storage/init_db.py
```

## Running

```bash
python main.py
```

## Project Structure

```
project_root/
│
├── bot/
│   ├── __init__.py
│   ├── github.py      # GitHub API integration
│   ├── telegram_bot.py # Telegram messaging
│   ├── scheduler.py   # Task scheduler
│   └── database.py    # SQLite database operations
│
├── storage/
│   ├── issues.db      # SQLite database
│   └── init_db.py     # Database initialization script
│
├── main.py           # Entry point
├── .env             # Environment variables
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.7+
- python-telegram-bot
- python-dotenv
- aiohttp 
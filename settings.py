import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

@dataclass
class SlackSettings:
    app_token: str = os.getenv("SLACK_APP_TOKEN")
    bot_token: str = os.getenv("SLACK_BOT_TOKEN")
    channel: str = os.getenv("SLACK_CHANNEL")
    mode: str = "Socket"
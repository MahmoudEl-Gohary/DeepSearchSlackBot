import asyncio
from datetime import datetime

from settings import SlackSettings
from src.tools.slack import SlackBot

async def main():

    slack = SlackBot(
        app_token=SlackSettings.app_token,
        bot_token=SlackSettings.bot_token,
        channel=SlackSettings.channel,
    )
    current_datetime = datetime.now()
    formatted_time = current_datetime.strftime("%H:%M:%S on %A")

    await slack.send_to_channel(f"{formatted_time} | Hello everyone! Praxi is online and ready to help. 😊")
    await slack.start()

if __name__ == "__main__":
    asyncio.run(main())

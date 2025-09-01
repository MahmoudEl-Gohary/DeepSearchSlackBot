# import os, aiohttp
import re
from src.agent import graph
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.errors import SlackApiError
from slack_bolt.app.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

class SlackClient:
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.web_client = AsyncWebClient(token=bot_token)

    async def get_user_info(self, user_id: str) -> dict | None:
        try:
            info = await self.web_client.users_info(user=user_id)
            user = info["user"]
            return {
                "id": user.get("id"),
                "name": user.get("name"),
                "real_name": user.get("real_name"),
                "email": user.get("profile", {}).get("email"),
            }
        except SlackApiError as e:
            print("[SLACK] user_info failed: %s", e.response["error"])
            return None

    async def send_message(self, channel: str, text: str) -> bool:
        try:
            await self.web_client.chat_postMessage(channel=channel, text=text, mrkdwn=True, parse_mode="mrkdwn")
            return True
        except SlackApiError as e:
            print(f"[SLACK] send_message failed: {e.response['error']}")
            return False

    # async def send_file(self, file_path: str, channel: str) -> bool:
    #     try:
    #         file_size = os.path.getsize(file_path)
    #         filename = os.path.basename(file_path)
    #
    #         upload_url_response = await self.web_client.files_getUploadURLExternal(
    #             filename=filename,
    #             length=file_size
    #         )
    #
    #         upload_url = upload_url_response["upload_url"]
    #         file_id = upload_url_response["file_id"]
    #
    #         async with aiohttp.ClientSession() as session:
    #             with open(file_path, 'rb') as file_data:
    #                 async with session.post(upload_url, data=file_data) as upload_response:
    #                     if upload_response.status != 200:
    #                         print(f"[SLACK] File upload failed with status: {upload_response.status}")
    #                         return False
    #
    #         await self.web_client.files_completeUploadExternal(
    #             files=[{
    #                 "id": file_id,
    #                 "title": filename
    #             }],
    #             channel_id="C0982FR6Q4R"
    #         )
    #
    #         return True
    #
    #     except SlackApiError as e:
    #         print(f"[SLACK] send_file failed: {e.response['error']}")
    #         return False
    #     except FileNotFoundError:
    #         print(f"[SLACK] send_file failed: File not found at {file_path}")
    #         return False
    #     except Exception as e:
    #         print(f"[SLACK] send_file failed: {str(e)}")
    #         return False

class CommandHandler:
    def __init__(self, client: SlackClient):
        self.client = client

    async def handle_ping(self, event, say):
        uid = event["user"]
        user = await self.client.get_user_info(uid)
        text = f"Pong! Hello {user['real_name']} 👋" if user else "Pong! 🤖"
        await say(text)

    async def handle_search(self, event, say, query):
        uid = event["user"]
        user = await self.client.get_user_info(uid)
        text = (
            f"{user['real_name']} just submitted a new Query:\n"
            f"Query: \"{query}\"\n"
            "Thanks for reaching out! We'll get back to you soon."
        )
        await say(text)

        await say("Starting deep research... This may take a few minutes. Please wait.")

        state = graph.invoke({
            "messages": [{
                "role": "user",
                "content": f"{query}"
            }],
            "max_research_loops": 2,
            "initial_search_query_count": 3
        })

        await say("Research completed. Preparing the summary...")

        await self.client.send_message(channel="ai-powered-services",
                                       text=re.sub(r'\*{2,}', '*', state["messages"][-1].content))

    async def handle_deep_search(self, ack, body, say, respond):
        await ack()

        uid = body["user_id"]
        user = await self.client.get_user_info(uid)

        query = body.get("text", "")
        text = (
            f"{user['real_name']} just submitted a new Query:\n"
            f"Query: \"{query}\"\n"
            "Thanks for reaching out! We'll get back to you soon."
        )
        await say(text)

        await say("Starting deep research... This may take a few minutes. Please wait.")

        state = graph.invoke({
            "messages": [{
                "role": "user",
                "content": f"{query}"
            }],
            "max_research_loops": 2,
            "initial_search_query_count": 3
        })

        await say("Research completed. Preparing the summary...")

        await self.client.send_message(channel="ai-powered-services", text=re.sub(r'\*{2,}', '*', state["messages"][-1].content))


class SlackBot:
    def __init__(self, app_token: str, bot_token: str, channel: str):
        self.app_token, self.bot_token, self.channel = app_token, bot_token, channel
        self.app = AsyncApp(token=bot_token)
        self.client = SlackClient(bot_token)
        self.handler = CommandHandler(self.client)
        self._setup_routes()

    async def _search_message_handler(self, message, say):
        match = re.match(r"^search:\s*(.*)", message["text"])
        if match:
            content = match.group(1)
            await self.handler.handle_search(message, say, content)

    def _setup_routes(self):
        self.app.message("ping")(self.handler.handle_ping)
        self.app.command("/deep-search")(self.handler.handle_deep_search)
        self.app.message(re.compile(r"^search:\s*(.*)"))(self._search_message_handler)

    async def send_to_channel(self, text: str) -> bool:
        return await self.client.send_message(self.channel, text)

    async def start(self):
        print(f"[SLACK] Starting Socket‑Mode for channel {self.channel}")
        socket_handler = AsyncSocketModeHandler(self.app, self.app_token)
        await socket_handler.start_async()
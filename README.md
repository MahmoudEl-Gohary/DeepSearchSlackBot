# SlackBot 🤖

A sophisticated AI-powered Slack bot built with Python that integrates advanced conversational capabilities using LangGraph for intelligent responses and workflow management.

## 🚀 Features

- **AI-Powered Conversations**: Advanced natural language processing for intelligent responses
- **Slack Integration**: Seamless integration with Slack workspaces using Socket Mode
- **Agent-Based Architecture**: Built with LangGraph for complex workflow management
- **Asynchronous Operations**: High-performance async/await implementation
- **Real-time Communication**: Live message processing and responses
- **Modular Design**: Clean, maintainable code structure with separation of concerns

## 📋 Prerequisites

- Python 3.8+
- Slack workspace with admin permissions
- Slack app with appropriate permissions and tokens

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/DeepSearchSlackBot.git
   cd DeepSearchSlackBot
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the root directory copy the content form .env.example and add your tokens, API keys.

## Configuration and API key
    Refer to API Integration & Configuration Guide.pdf for detailed instructions on setting up your Slack app and obtaining API keys.


## 🚀 Usage

1. **Start the bot**
   ```bash
   python main.py
   ```

2. **Invite the bot to your channel**
   ```
   /invite @your-bot-name
   ```

3. **Start chatting!**
   - The bot will announce when it comes online
   - use `/deep-search` on the channel or send direct messages to interact

## 📁 Project Structure

```
PraxiSlackBot/
├── main.py                 # Entry point
├── settings.py             # Configuration (not in repo)
├── requirements.txt        # Dependencies
├── .gitignore             # Git ignore rules
├── README.md              # This file
└── src/
    ├── __init__.py
    ├── agent/             # AI agent components
    │   ├── __init__.py
    │   ├── configuration.py
    │   ├── graph.py       # LangGraph workflow
    │   ├── prompts.py     # AI prompts
    │   ├── state.py       # State management
    │   ├── tools_and_schemas.py
    │   └── utils.py
    └── tools/             # Utility tools
        ├── __init__.py
        └── slack.py       # Slack integration
```

## 🔧 Configuration

The bot uses a `settings.py` file for configuration. Create this file with your Slack credentials:

```python
class SlackSettings:
    app_token = "xapp-1-xxxxx"      # App-Level Token
    bot_token = "xoxb-xxxxx"        # Bot User OAuth Token
    channel = "#general"            # Default channel
```

## 🧩 Architecture

### Agent System
- **LangGraph Integration**: Uses LangGraph for complex conversation flows
- **State Management**: Maintains conversation context and state
- **Tool Integration**: Extensible tool system for various capabilities

### Slack Integration
- **AsyncWebClient**: For API calls and message sending
- **Socket Mode**: Real-time event handling
- **Event Processing**: Handles various Slack events and interactions

## 🔍 Key Components

### `main.py`
Entry point that initializes the bot and starts the Slack connection.

### `src/tools/slack.py`
Core Slack integration handling:
- Message sending and receiving
- Event processing
- Socket mode connection management

### `src/agent/`
AI agent components:
- **graph.py**: LangGraph workflow definition
- **state.py**: Conversation state management
- **prompts.py**: AI prompt templates
- **configuration.py**: Agent configuration

## 🛡️ Security

- **Token Management**: Keep your Slack tokens secure and never commit them to version control
- **Environment Variables**: Use environment variables or secure configuration files
- **Permissions**: Follow the principle of least privilege for Slack permissions

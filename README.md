☠️ NUKER | ZeroDev

A customizable Discord server nuking tool built with Python, Discord.py, Asyncio, and Rich.

NUKER is a terminal-based Discord tool featuring a colorful dashboard, server information panels, configurable settings, and asynchronous task execution.

✨ Features

- Rich Dashboard — A terminal interface with panels, tables, colors, and status displays.
- Server Information — View server name, ID, member count, channels, roles, and bot administrator status.
- Configurable Settings — Customize the server name, message content, channel names, channel count, role names, and messages per channel.
- Asynchronous Execution — Uses Python's "asyncio" for concurrent task handling.
- Server Selection — Select a server from the bot's available server list.
- Interactive Menu — Navigate between the main menu, settings, and exit options.
- Customizable Interface — Modify the dashboard and terminal styling to match your preferred theme.

🧰 Requirements

- Python 3.10+
- A Discord bot token
- "discord.py"
- "rich"

📦 Installation

Install the required dependencies:

pip install -r requirements.txt

🚀 Usage

1. Install Python and the required dependencies.
2. Configure your Discord bot through the Discord Developer Portal.
3. Run the Python entry-point file.
4. Enter your bot token when prompted.
5. Select an available server and navigate the menu.

⚙️ Configuration

The "CFG" dictionary in the Python source contains settings for the server name, message content, channel names, channel count, role names, and messages per channel.

You can adjust the values in the source code or use the built-in settings menu where available.

🔐 Security

- Never publish your Discord bot token.
- Do not commit credentials to a public repository.
- Grant bots only the permissions they require.
- Test in a private server you own or are authorized to manage.
- Respect Discord's Terms of Service and API rate limits.

⚠️ Disclaimer

This project is provided for educational purposes and authorized testing. The user is responsible for ensuring that its use complies with Discord's rules and applicable laws.

Built with Python by ZeroDev.
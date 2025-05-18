# CoEHP-Discord-Bot

## Overview
CoEHP-Discord-Bot is a Discord bot designed to gather analytics on student engagement in a summer Discord server. It analyzes message activity, tracks engagement by week, and generates a chart of weekly student participation. The bot focuses on users with the 'Verified Student' role and excludes staff, bots, and other non-student roles.

### Features
- Counts total students and messages sent by students
- Tracks number of students who have engaged (sent at least one message)
- Provides weekly engagement statistics
- Generates a chart (`engagement_chart.png`) visualizing weekly student engagement

## Requirements
- Python 3.8+
- Discord bot token
- The dependencies listed in `requirements.txt` (notably `discord.py` and `matplotlib`)

## Setup & Usage

1. **Clone the repository**
   ```sh
   git clone <repo-url>
   cd CoEHP-Discord-Bot
   ```

2. **Install dependencies**
   It is recommended to use a virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure the bot**
   - Open `main.py` and replace `REPLACE_WITH_YOUR_DISCORD_BOT_TOKEN` with your actual Discord bot token.
   - (Optional) Adjust `STUDENT_ROLE_NAME`, `DOORBELL_CHANNEL_NAME`, and `DOORBELL_BOT_NAME` as needed for your server.

4. **Run the bot**
   ```sh
   python main.py
   ```
   The bot will log in, process the server, and output analytics to the console. If `matplotlib` is installed, it will also save a chart as `engagement_chart.png` in the project directory.

## Notes
- The bot requires permission to read message history and member roles in your Discord server.
- The bot will automatically close after processing and generating analytics.
- Make sure your bot is invited to the server with the necessary permissions.

## License
See [LICENSE](LICENSE) for details.

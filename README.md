# Arma 3 Discord Bot

My cousins play on the Arma 3 server I built even when I'm not around — which is great, until something needs restarting or a modset needs switching. Asking them to SSH into a Linux server was never going to work. They're already in Discord every time they play, so that's where the controls should live. This bot gives them a simple interface to check server status, start it if it's down, and stop it when they're done — all without touching the underlying infrastructure. Built with Python and discord.py, restricted to a private admin channel and specific Discord roles so only the right people can run commands.

A Discord bot for controlling an Arma 3 server via Discord commands. Built with Python and discord.py, running as a systemd service on Ubuntu.

## Features

- Check Arma 3 server status
- Start and stop the Arma 3 server
- Role restricted commands (Admin only)
- Channel restricted commands
- Runs as a systemd service on boot

## Requirements

- Ubuntu 24.04
- Python 3.13+
- uv
- A Discord bot token
- Arma 3 server running as a systemd service

## Project Structure

```
arma-bot/
├── bot.py
├── .env
├── pyproject.toml
└── README.md
```

## Setup

### 1. Clone the repository

```bash
sudo su - steam
cd /home/steam
git clone <your-repo-url> arma-bot
cd arma-bot
```

### 2. Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
```

### 3. Create the .env file

```bash
nano .env
```

Add your Discord bot token:

```
API_KEY="your_bot_token_here"
```

### 4. Set up sudoers

Create a sudoers rule to allow the steam user to control the Arma 3 server without a password prompt:

```bash
sudo visudo -f /etc/sudoers.d/arma-bot
```

Add the following:

```
steam ALL=(ALL) NOPASSWD: /usr/bin/systemctl start arma3server.service
steam ALL=(ALL) NOPASSWD: /usr/bin/systemctl stop arma3server.service
steam ALL=(ALL) NOPASSWD: /usr/bin/systemctl status arma3server.service
```

### 5. Set up the systemd service

Create the service file:

```bash
sudo nano /etc/systemd/system/arma3-bot.service
```

Add the following:

```ini
[Unit]
Description=Arma 3 Discord Bot

[Service]
Type=simple
User=steam
Group=steam
WorkingDirectory=/home/steam/arma-bot
ExecStart=/home/steam/.local/bin/uv run /home/steam/arma-bot/bot.py
Restart=on-failure
RestartSec=30s
SuccessExitStatus=143
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable arma3-bot
sudo systemctl start arma3-bot
```

## Discord Setup

### Create a bot application

1. Go to https://discord.com/developers/applications
2. Click **New Application** and give it a name
3. Go to **Bot** in the left sidebar
4. Click **Add Bot**
5. Copy the bot token and add it to your `.env` file
6. Enable the **Message Content Intent** under Privileged Gateway Intents

### Invite the bot to your server

1. Go to **OAuth2** in the left sidebar
2. Under **Scopes** check `bot`
3. Under **Bot Permissions** check `Send Messages` and `Read Message History`
4. Copy the generated URL and open it in your browser
5. Select your server and click **Authorize**

### Discord server setup

1. Create an `Admin` role and assign it to yourself
2. Create a channel called `arma-controls`
3. Restrict the channel so only the Admin role can see and use it

## Commands

All commands require the `Admin` role and must be used in the `arma-controls` channel.

| Command | Description |
|---------|-------------|
| `!status` | Shows the current status of the Arma 3 server |
| `!start` | Starts the Arma 3 server |
| `!stop` | Stops the Arma 3 server |

## Managing the bot

```bash
# Check bot status
sudo systemctl status arma3-bot

# Stop the bot
sudo systemctl stop arma3-bot

# Start the bot
sudo systemctl start arma3-bot

# Restart the bot
sudo systemctl restart arma3-bot

# View logs
sudo journalctl -u arma3-bot -f
```

## Development

The bot is developed on Windows using WSL2 and Zed. To update the bot on the homelab:

```bash
# On the homelab as steam
cd /home/steam/arma-bot
git pull
sudo systemctl restart arma3-bot
```

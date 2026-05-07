import asyncio
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()


discord_key = os.getenv("API_KEY")

if not discord_key:
    print("no discord key")
    raise ValueError("No API_KEY found in .env file")

intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
@commands.has_role("Admin")
async def status(ctx):
    arma_status = await asyncio.create_subprocess_shell(
        "sudo systemctl status arma3server.service",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    status_output, error_output = await arma_status.communicate()
    status_output = status_output.decode()
    error_output = error_output.decode()
    if status_output:
        if len(status_output) > 2000:
            await ctx.send(status_output[:2000])
        else:
            await ctx.send(status_output)
    if error_output:
        if len(error_output) > 2000:
            await ctx.send(error_output[:2000])
        else:
            await ctx.send(error_output)


bot.run(discord_key)

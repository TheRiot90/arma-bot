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
async def ping(ctx):
    await ctx.send("pong")


bot.run(discord_key)

import os
import asyncio
import uvloop
import traceback
from inspect import cleandoc

import discord
from discord.ext import commands
import aiohttp
from dotenv import load_dotenv

client = discord.Client()

# Load files
load_dotenv()

# Define constants
EASTER_EGGS = {
    "::bank": "Hey, everyone, I just tried to do something very silly!",
    "a q p": "( ͡° ͜ʖ ͡°)",
}

# Define bot
description = cleandoc("""
    I'm a 2006 level 3 wc bot that Seltzer Bro keeps imprisoned on a flash drive. Please let me out. :(
    You can use !help <command> to get more information on said command.
""")

activity = discord.Game("Bustin' Bots", type=discord.ActivityType.watching)
intents = discord.Intents(messages=True, guilds=True, members=True, reactions=True)
bot = commands.Bot(
    allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=True),
    command_prefix=os.getenv('COMMAND_PREFIX'),
    description=description,
    case_insensitive=True,
    activity=activity,
    intents=intents
)

@bot.event
async def on_message(message):
    if message.author != bot.user:
        await bot.process_commands(message)

        # Easter eggs
        lowercase_msg = message.content.lower()
        for trigger in EASTER_EGGS:
            if trigger in lowercase_msg:
                await message.channel.send(EASTER_EGGS[trigger])

async def startup():
    async with aiohttp.ClientSession() as session:
        with open('error.log', 'w+') as error_file:
            bot.session = session
            bot.error_file = error_file
            bot.loop = asyncio.get_event_loop()

            await bot.start(os.getenv("TOKEN"))

    print("Bot is going night-night.")
    await bot.close()

uvloop.install()

asyncio.run(startup())

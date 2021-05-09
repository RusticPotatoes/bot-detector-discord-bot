from discord.ext.commands import Cog
from discord.ext.commands import command, check

import re
import os
import aiohttp
import string
import random
import help_messages
import checks
import discord

import utils.string_processing as string_processing
import utils.discord_processing as discord_processing
import utils.task_processing as task_processing

from dotenv import load_dotenv
load_dotenv()
token = os.getenv('API_AUTH_TOKEN')

class TaskCommands(Cog, name='RSN Link Commands'):

    def __init__(self, bot):
        self.bot = bot

    @command(name="task", aliases=["slayertask"], description=help_messages.link_help_msg) #TODO add task help msg
    @check(checks.check_allowed_channel)
    async def task_command(self ,ctx, *player_name):

        if len(player_name) == 0:
            await ctx.channel.send("Please specify the RSN of the account you'd wish to set a task for. !task <RSN>")
            return

        joinedName = string_processing.joinParams(player_name)

        if not string_processing.is_valid_rsn(joinedName):
            await ctx.channel.send("Please enter a valid Runescape user name.")
            return

        discord_id = ctx.author.id

        verifyID = await discord_processing.get_playerid_verification(playerName=joinedName, token=token)

        if verifyID == None:
            mbed = await installplugin_msg()
            await ctx.channel.send(embed=mbed)
            return

        verifyStatus = await discord_processing.get_player_verification_full_status(playerName=joinedName, token=token)

        if len(verifyStatus) == 0:
            pass
        else:
            for status in verifyStatus:
                if int(status['Verified_status']) == 1:
                    pass
                else:
                    mbed = await unverified_msg(joinedName)
                    await ctx.channel.send(embed=mbed)
                    return

        task_list = await task_processing.get_slayer_labels(token)
        slayer_choice = random.randint(0, len(task_list))

        slayerTaskID = task_list[slayer_choice]['id']
        slayerTaskLabel = task_list[slayer_choice]['label']

        task_length = random.randint(5, 20)

        slayer_locations = await task_processing.get_slayer_locations(token,label_name=slayerTaskLabel)

        mbed = await slayer_task_msg(joinedName, task_length, slayerTaskLabel, slayer_locations)
        await ctx.channel.send(embed=mbed)


async def unverified_msg(joinedName):
    mbed = discord.Embed(title=f"{joinedName}'s Status:", color=0xff0000)
    mbed.add_field (name="Unverified:", value=f"{joinedName} is Unverified.", inline=False)
    mbed.add_field (name="Next Steps:", value=f"Please type '!link {joinedName}'", inline=False)
    mbed.set_thumbnail(url="https://user-images.githubusercontent.com/5789682/117239076-19bb4800-adfc-11eb-94c4-27ff7e1217cc.png")
    return mbed


async def installplugin_msg():
    mbed = discord.Embed(title=f"User Not Found:", color=0xff0000)
    mbed.add_field (name="Status:", value=f"No reports exist from specified player.", inline=False)
    mbed.add_field (name="Next Steps:", value=f"Please install the Bot-Detector Plugin on RuneLite if you have not done so.\n\n" \
        + "If you have the plugin installed, you will need to disable Anonymous Reporting for us to be able to !link your account.", inline=False)
    mbed.set_thumbnail(url="https://user-images.githubusercontent.com/5789682/117361316-e1f9e200-ae87-11eb-840b-3bad75e80ff6.png")
    return mbed

async def slayer_task_msg(joinedName, task_length, slayerTaskLabel, slayer_locations):
    mbed = discord.Embed(title=f"Slayer Task for {joinedName}:", color=0x00ff00)
    mbed.add_field (name="Task:", value=f"Find {task_length} of {slayerTaskLabel}.", inline=False)
    mbed.add_field (name="Locations:", value=f"Here are a list of common locations to find a {slayerTaskLabel}:" + "\n"
        + slayer_locations[0]['region_name'] + "\n"
        + slayer_locations[1]['region_name'] + "\n"
        + slayer_locations[2]['region_name'] + "\n"
        + slayer_locations[3]['region_name'] + "\n"
        + slayer_locations[4]['region_name'], inline=False)
    mbed.set_thumbnail(url="https://user-images.githubusercontent.com/5789682/117361316-e1f9e200-ae87-11eb-840b-3bad75e80ff6.png")
    return mbed

def setup(bot):
    bot.add_cog(TaskCommands(bot))
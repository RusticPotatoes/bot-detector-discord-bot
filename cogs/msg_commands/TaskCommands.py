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
        slayer_choice = random.randint(0, len(task_list)-1)
        slayerTaskID = task_list[slayer_choice]['id']
        slayerTaskLabel = task_list[slayer_choice]['label']
        task_length = random.randint(5, 20)

        print(verifyStatus)

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
    mbed = discord.Embed(description=f"Find {task_length} {slayerTaskLabel}.", color=0x00ff00)
    mbed.set_author(name=f"[WORK IN PROGRESS DOES NOT ACTUALLY WORK] Slayer Master Ferrariic (Easy) - {joinedName}", icon_url='https://user-images.githubusercontent.com/5789682/117591275-c437b180-b101-11eb-907d-59056cf277e3.png')
    mbed.add_field (name=f"Locations where you might find a {slayerTaskLabel}:", value=f"\n" 
        + "1. " + slayer_locations[0]['region_name'] + "\n"
        + "2. " + slayer_locations[1]['region_name'] + "\n"
        + "3. " + slayer_locations[2]['region_name'] + "\n"
        + "4. " + slayer_locations[3]['region_name'] + "\n"
        + "5. " + slayer_locations[4]['region_name'] + "\n"
        + "6. " + slayer_locations[5]['region_name'] + "\n"
        + "7. " + slayer_locations[6]['region_name'] + "\n"
        + "8. " + slayer_locations[7]['region_name'] + "\n"
        + "9. " + slayer_locations[8]['region_name'] + "\n"
        + "10. " + slayer_locations[9]['region_name'], inline=False)


    url_image = await get_image_link(slayerTaskLabel)
    mbed.set_image(url=url_image)


    url_image = await get_image_link(slayerTaskLabel)
    mbed.set_image(url=url_image)

    return mbed

async def get_image_link(slayerTaskLabel):
    image_dict = {
        "Agility_bot"               : "https://user-images.githubusercontent.com/5789682/117589241-694c8d00-b0f6-11eb-987e-d3e4cc41e556.gif",
        "Bot"                       : "https://user-images.githubusercontent.com/5789682/117589243-6b165080-b0f6-11eb-8952-037f6d828909.gif",
        "Cooking_bot"               : "https://user-images.githubusercontent.com/5789682/117589244-6c477d80-b0f6-11eb-847e-bb59cd7d655b.gif",
        "PVM_Melee_bot"             : "https://user-images.githubusercontent.com/5789682/117589245-6e114100-b0f6-11eb-9649-8f5b794113b1.gif",
        "Magic_bot"                 : "https://user-images.githubusercontent.com/5789682/117589247-6f426e00-b0f6-11eb-9cc3-6fed6c6fe581.gif",
        "Mining_bot"                : "https://user-images.githubusercontent.com/5789682/117589250-70739b00-b0f6-11eb-8a15-59251d8322a2.gif",
        "Runecrafting_bot"          : "https://user-images.githubusercontent.com/5789682/117589251-72d5f500-b0f6-11eb-85f0-a31a3cada6b0.gif",
        "Wintertodt_bot"            : "https://user-images.githubusercontent.com/5789682/117589254-749fb880-b0f6-11eb-9777-64057c1fd187.gif",
        "Woodcutting_bot"           : "https://user-images.githubusercontent.com/5789682/117589255-75d0e580-b0f6-11eb-98c4-a6223ef9c41e.gif",
        "PVM_Ranged_Magic_bot"      : "https://user-images.githubusercontent.com/5789682/117589259-78cbd600-b0f6-11eb-8804-0bf21d5dd6b3.gif",
        "Herblore_bot"              : "https://user-images.githubusercontent.com/5789682/117591248-a36f5c00-b101-11eb-9519-fc359c2205db.gif",
        "Crafting_bot"              : "https://user-images.githubusercontent.com/5789682/117591462-a159cd00-b102-11eb-95f8-d6b3657516f3.gif",
        "Fishing_bot"               : "https://user-images.githubusercontent.com/5789682/117593332-5db69180-b109-11eb-8322-c17cbd61c383.gif",
        "Fishing_Cooking_bot"       : "https://user-images.githubusercontent.com/5789682/117593332-5db69180-b109-11eb-8322-c17cbd61c383.gif" 
    }
    try:
        url = image_dict[slayerTaskLabel]
    except KeyError:
        url = image_dict["Bot"]

    return url

def setup(bot):
    bot.add_cog(TaskCommands(bot))
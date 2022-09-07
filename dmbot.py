# dmbot.py
# Author: Leon Breidt
# Date: 17.08.2022
import os

import discord
import random
import yaml

import traceback as tb

from character import *

with open('bot.yml', 'r') as file:
    config_data = yaml.safe_load(file)

TOKEN = config_data["bot"]["token"]
log_channel = config_data["bot"]["logchannel"]

intents = discord.Intents.all()
client = discord.Client(command_prefix='.',intents=intents)

def isDungeonMaster(member):
    for role in member.roles:
        if role.name == config_data["roles"]["dungeon_master"]:
            return True
    return False

async def getMessageForMainBotChannel(message):
    if isDungeonMaster(message.author):
        response = "Gute Antwort! :)"
        await message.channel.send(response)
        return

    if "leben" in message.content.lower() and "universum" in message.content.lower() and "alles" in message.content.lower():
        response = "42"
        await message.channel.send(response)
        return

    if "oder" in message.content.lower():
        response = "Bitte würfel einen D20?"
        await message.channel.send(response)
        return

    if "nicht" in message.content.lower():
        response = "Das macht 3 Schadenspunkte"
        await message.channel.send(response)
        return

    if message.content.isdigit():
        response = "Das ist nicht des Rätsels Lösung"
        await message.channel.send(response)
        return

    if "ich" in message.content.lower():
        response = "Auf so eine Idee können wirklich nur Spieler kommen"
        await message.channel.send(response)
        return


    if "?" in message.content:
        response = "Das ist eine dumme Frage!"
        await message.channel.send(response)
    else:
        response = "Das ist keine Frage..."
        await message.channel.send(response)

async def getMessageForAllOtherChannels(message):
    
    if "characterdice" in message.content.lower():
        numbers = [random.randint(1, 6) for i in range(4)]
        actual = numbers
        for num in actual:
            if min(actual) == num:
                actual.remove(num)
                break
    
        relevant_sum = int(sum(actual))
        response = f"```markdown\n# {relevant_sum}\nDetails:[4d6 ({actual[0]}, {actual[1]}, {actual[2]}, [{min(numbers)}])]```"
        await message.channel.send(response)
    elif "dice" in message.content.lower():
        number = random.randint(1, 20)
        response = f"```markdown\n# {number}\nDetails:[d20 ({number})]```"
        await message.channel.send(response)
        return
    

@client.event
async def on_ready():
    print('[D] Bot gestartet')

@client.event
async def on_message(message):
    global client
    try:
        if message.author == client.user:
            return
        
        if message.content.lower().startswith("!char"):
            await handleCharacterCommand(message)
        elif config_data["bot"]["channel"] in message.channel.name:
            await getMessageForMainBotChannel(message)
        else:
            await getMessageForAllOtherChannels(message)
    except Exception as e:
        errorchannel = client.get_channel(log_channel)
        await errorchannel.send(''.join(tb.format_exception(None, e, e.__traceback__)))

#@client.event
#async def on_error(event, *args, **kwargs):
#    print(event)
#    print(args)
#    print(kwargs)
#    with open('err.log', 'a') as f:
#        if event == 'on_message':
#            f.write(f'Unhandled message: {args[0]}\n')
#        else:
#            raise

client.run(TOKEN)


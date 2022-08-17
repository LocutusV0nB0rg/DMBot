# dmbot.py
# Author: Leon Breidt
# Date: 17.08.2022
import os

import discord

import yaml

with open('bot.yml', 'r') as file:
    config_data = yaml.safe_load(file)

TOKEN = config_data["bot"]["token"]

client = discord.Client()

def isDungeonMaster(member):
    for role in member.roles:
        if role.name == config_data["roles"]["dungeon_master"]:
            return True
    return False

@client.event
async def on_ready():
    print('[D] Bot gestartet')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if config_data["bot"]["channel"] not in message.channel.name:
        return

    if isDungeonMaster(message.author):
        response = "Gute Antwort! :)"
        await message.channel.send(response)
        return

    if "?" in message.content:
        response = "Das ist eine dumme Frage!"
        await message.channel.send(response)
    else:
        response = "Das ist keine Frage..."
        await message.channel.send(response)

@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

client.run(TOKEN)


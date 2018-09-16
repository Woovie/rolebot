import discord
import asyncio
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')

client = discord.Client()

@client.event
async def on_ready():
    print('barkbot ready')
    await update_status()

async def update_status():
    await client.change_presence(game=discord.Game(name=f"type {config['command-settings']['prefix']}{config['command-settings']['helper']}"))

@client.event
async def on_message(message):
    for command in config['commands']:
        if message.content == f"{config['command-settings']['prefix']}{command}":
            await client.send_message(message.channel, config['commands'][command])
    for member in message.server.members:
        if message.content == f"{config['command-settings']['prefix']}{member.nick}":
            await client.send_message(message.channel, f"<@{member.id}>")
client.run(config['discord']['token'])

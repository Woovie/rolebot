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
    await client.change_presence(game=discord.Game(name='type !doorbell'))

@client.event
async def on_message(message):
    if message.content == '!bark':
        await client.send_message(message.channel, '*woof*')
    if message.content == '!bork':
        await client.send_message(message.channel, '***bork***')
    if message.content == '!doorbell':
        await client.send_message(message.channel, '**W͏OOF ẂOOF̵ WƠOF ҉WOOF W̶OO͟F **')
    for member in message.server.members:
        if message.content == f"!{member.nick}":
            await client.send_message(message.channel, f"<@{member.id}>")
client.run(config['discord']['token'])

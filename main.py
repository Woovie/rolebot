#!/usr/bin/env python3.6
import discord
import asyncio
import configparser
import random
import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler as asyncsched

config = configparser.ConfigParser()
config.read('settings.ini')

discordconf = configparser.ConfigParser()
discordconf.read('discord-token.ini')

scheduler = asyncsched()

client = discord.Client()

tick = 0
word = ["helo", "yes", "this", "is", "dog", f"type {config['command-settings']['prefix']}{config['command-settings']['helper']}"]

@client.event
async def on_ready():
    print('barkbot ready')
    job = scheduler.add_job(random_status, 'interval', seconds=10)
    scheduler.start()

async def random_status():
    global tick
    await client.change_presence(game=discord.Game(name=f"{word[tick]}"))
    if tick == len(word)-1:
        tick = 0
    else:
        tick = tick+1

@client.event
async def on_message(message):
    if message.content == f"{config['command-settings']['prefix']}{config['command-settings']['helper']}":#Embed
        if len(config['commands']) > 0:
            embed = discord.Embed(title="Available commands")
            for command in config['commands']:
                embed.add_field(name=command, value=f"```{config['commands'][command]}```", inline=False)
            await client.send_message(message.channel, embed=embed)
    for command in config['commands']:
        if message.content.lower() == f"{config['command-settings']['prefix']}{command}":
            await client.send_message(message.channel, config['commands'][command])
    for member in message.server.members:
        if message.content == f"{config['command-settings']['prefix']}{member.nick}":
            await client.send_message(message.channel, f"<@{member.id}>")

client.run(discordconf['discord']['token'])

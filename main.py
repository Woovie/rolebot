#!/usr/bin/env python3.6
import discord
import asyncio
import configparser
import random
import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler as asyncsched

configFileName = 'settings.ini'

config = configparser.ConfigParser()
config.read(configFileName)

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
        embed = discord.Embed(title=f"Help for {config['command-settings']['botname']}")
        embed.set_footer(text=f"Bot by {config['command-settings']['author']}, source code at {config['command-settings']['source']}")
        embed.add_field(name="Prefix symbol", value=config['command-settings']['prefix'], inline=False)
        embed.add_field(name=config['command-settings']['helper'], value="Returns this message.", inline=False)
        embed.add_field(name=config['command-settings']['add'], value=f"Add a new command.\nFormat: `{config['command-settings']['prefix']}{config['command-settings']['add']} <command-name> ...`\nRequires 3 arguments, everything past the `<command-name>` is what will return.\nUse `{config['command-settings']['splitter']}` to separate values for random value selection.", inline=False)
        embed.add_field(name=config['command-settings']['rem'], value=f"Remove an existing command.\nFormat: `{config['command-settings']['prefix']}{config['command-settings']['rem']} <command-name>`", inline=False)
        embed.add_field(name=config['command-settings']['commands'], value="Returns available commands.")
        await client.send_message(message.channel, embed=embed)
    if message.content == f"{config['command-settings']['prefix']}{config['command-settings']['commands']}":
        if len(config['commands']) > 0:
            embed = discord.Embed(title="Available commands")
            for command in config['commands']:
                embed.add_field(name=command, value=f"```{config['commands'][command]}```", inline=False)
            await client.send_message(message.channel, embed=embed)
        else:
            await client.send_message(message.channel, f"No commands available :( Try adding a new one with `{config['command-settings']['prefix']}{config['command-settings']['add']}`")
    for command in config['commands']:
        if message.content.lower() == f"{config['command-settings']['prefix']}{command}":
            commandArray = config['commands'][command].split(config['command-settings']['splitter'])
            messageToSend = commandArray[random.randint(0,len(commandArray)-1)]
            await client.send_message(message.channel, messageToSend)
    for member in message.server.members:
        if message.content == f"{config['command-settings']['prefix']}{member.nick}":
            await client.send_message(message.channel, f"<@{member.id}>")
    if message.content.startswith(f"{config['command-settings']['prefix']}{config['command-settings']['add']}"):
        splitMessage = message.content.split()
        if len(splitMessage) >= 3:
            commandString = splitMessage[1]
            commandResult = ' '.join(splitMessage[2:])
            config['commands'][commandString] = commandResult
            with open(configFileName, 'w') as configFile:
                config.write(configFile)
            embed = discord.Embed(title="Added new command")
            embed.add_field(name=commandString, value=f"```{commandResult}```", inline=False)
            await client.send_message(message.channel, embed=embed)
    if message.content.startswith(f"{config['command-settings']['prefix']}{config['command-settings']['rem']}"):
        splitMessage = message.content.split()
        if len(splitMessage) == 2:
            commandString = splitMessage[1]
            if commandString in config['commands']:
                config.remove_option('commands', commandString)
                with open(configFileName, 'w') as configFile:
                    config.write(configFile)
                await client.send_message(message.channel, f"Command {commandString} removed.")

client.run(discordconf['discord']['token'])

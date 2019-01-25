#!/usr/bin/env python3.6
import discord
import asyncio
import configparser

configFileName = 'settings.ini'

config = configparser.ConfigParser()
config.read(configFileName)

botname = config['command-settings']['botname']
prefix = config['command-settings']['prefix']
helper = config['command-settings']['helper']
author = config['command-settings']['author']
source = config['command-settings']['source']
cmdhelper = f"{prefix}{helper}"

discordconf = configparser.ConfigParser()
discordconf.read('discord-token.ini')
client = discord.Client()

@client.event
async def on_ready():
    print(f"{botname} ready")
    await client.change_presence(game=discord.Game(name=f"{botname} | {cmdhelper}"))

@client.event
async def on_message(message):
    if message.content == f"{cmdhelper}":#Embed
        embed = discord.Embed(title=f"Help for {botname}")
        embed.set_footer(text=f"Bot by {author}, source code at {source}")
        embed.add_field(name="Prefix symbol", value=prefix, inline=False)
        embed.add_field(name=helper, value="Returns this message.", inline=False)
        await client.send_message(message.channel, embed=embed)
client.run(discordconf['discord']['token'])

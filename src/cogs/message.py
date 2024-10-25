import re
import shlex
import discord
import os
import time
import random
import requests, json
import aiohttp
import asyncio
import sys
import subprocess
import urllib.request
from discord import Option
from datetime import timedelta
from discord.ext import commands, tasks
from discord.ext.commands import MissingPermissions
from itertools import cycle
import openai
from discord.utils import find
from cogs import app, vars
from cogs.vars import *
import google.generativeai as genai

bot = app.bot
whitelisted_ids = [716390085896962058]

async def _message(message):
  global wumbee
  # Prevents spam via other bots
  if message.author.bot and message.author.id not in whitelisted_ids:
    return

  # Prevents chaining
  if message.author == bot.user:
    return

  msg = message.content.lower()

  # Start of Bash section
  if message.content.startswith('exec'):
    split_cmd = message.content.split(' ')
    split_cmd = [word for word in split_cmd if word != 'exec']
    cmd = ' '.join(split_cmd)
    await message.channel.send(exec(cmd))
  
  if message.content.startswith('sudo'):
    split_cmd = shlex.split(message.content)
    split_cmd = [word for word in split_cmd if word != 'sudo']
    cmd = ' '.join(split_cmd)
    command = f'docker run ubuntu bash -c "{cmd}"'
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30, universal_newlines=True)
    stdout_result = result.stdout
    stdout_error = result.stderr
    if result.returncode != 0:
      await message.reply('An error has occurred!')
      await message.channel.send(f'Error: {stdout_error}\n\nCode: {result.returncode}')
    else:
      await message.reply('Your Bashchan Output!')
      await message.channel.send(f'Result: {stdout_result}\n\nCode: {result.returncode}')
  # End of bash section
  
  # Poketwo cheating
  if "the pokémon is" in msg and message.author.id == 716390085896962058:
    with open("pokemon_names.json", "r") as pk:
      pokemon_names = json.load(pk)
    hint = message.content
    hint = hint.replace('\\', '')
    pattern = re.search(r'(?<=is )[^.]*', hint).group()
    pattern = pattern.replace('_', '.')
    pattern = pattern.lower()
    matches = [name for name in pokemon_names if re.match(pattern, name)]
    if len(matches) != 1:
      return_string = f"Several matches were discovered: ||{matches}||"
      await message.channel.send(return_string)
    else:
      await message.channel.send(f"The pokemon is: ||{matches[0]}|| (If you needed this, you're gay)")
  
  if message.author.id == 716390085896962058:
    embeds = message.embeds 
    for embed in embeds:
      embed = embed.to_dict()
      if "Guess the pokémon" in embed['description']:
        s_role = discord.utils.get(message.guild.roles, name="spawn")
        await message.channel.send(f"{s_role.mention}, a wild Pokémon appears!")
  # End of poketwo cheating

  # Start of response section
  if message.content.lower() == "when.":
    def file_handler(filename, strings = None):
      if strings:
        file = open(filename, "w")
        file.write(str(strings))
      else:
        file = open(filename, "r")
        return file.read()
    tttr = int(file_handler("tttr"))
    tttr += 1
    file_handler("tttr", tttr)
    sent_message = await message.channel.send(embed=discord.Embed(title="Congratulations...", description=f"{message.author.mention} added another hour to the amount of time till whatever they were waiting for, nice work. The collective total of the hours added by impatience is now {file_handler('tttr')}"))
    await asyncio.sleep(3)
    await sent_message.delete()
    await message.delete()
  
  def json_handler(filename):
    with open(filename, "r") as read_file:
      data = json.load(read_file)
    return data
  censors = json_handler("censor.json")
  
  if message:
    for v in censors.values():
      if v != None:
        if v in msg:
          await message.delete()
          await message.channel.send(f"{message.author.mention} said a censored word")
  
  number = app.number	
  if message.content.isdigit() and number != None:
    if int(message.content) == number:
      await message.reply("Epic!")
      app.number = None
      return
    if int(message.content) >= number:
      await message.reply("Lower!")
    if int(message.content) <= number:
      await message.reply("Higher!")
      
  if "<@830863280237969438>" == message.content:
    await message.reply('Fuck off!')
     
  if "cool cool very epic" in msg:
    await message.channel.send('<:stretchreaction:1140646501157183489>:thumbsup:')

  if "bee" == message.content.lower():
    await message.channel.send('buzz buzz mfer')

  if message.content.lower() == "no.":
    await message.channel.send('***Y E S!***')

  if message.content.lower() == "real":
    await message.channel.send('<:wumstreetch:1112090292963778651>')

  if message.content.lower() == "snek":
    await message.reply('$ beesudo bee install snek <:streeeetch:1099963307550572545>')

  if "<:streeeetched:1099963307550572545>" in msg:
    await message.channel.send('<:wumstretch:1112286819103547444>')

  if "stfu" in msg:
    await message.reply('***NEVER!***')

  if "hsr" in msg:
    await message.reply(f"{message.author.mention} should play genshin")
    
  if "bumblin" in msg:
    await message.channel.send('https://tenor.com/view/bumblin-lmfao-bee-bumblebee-gif-22508972')
  # End of response section

  # Gemini implementation
  if message.reference:
    referenced_message = await message.channel.fetch_message(message.reference.message_id)
    if message.reference.resolved.author == bot.user:
      genai.configure(api_key=os.environ["GEMINI_API_KEY"])
      model = genai.GenerativeModel('gemini-1.5-flash')
      prompt = f"This is being sent through a discord bot (the bots/your name is Wumbot and you were made using pycord by Wumbee), please generate an answer according to the following: this was YOUR previous message: '{referenced_message.content}' and this is the reply to YOUR message: '{message.content}' and the reply was sent by '{message.author.name}', now generate a reply according to the above"
      response = model.generate_content(f"{prompt}")
      await message.reply(response.text)
      pass

  # Channel bridging
  chatmode = app.chatmode
  chat_user = app.chat_user
  chat_user_id = app.chat_user_id
  chatter = app.chatter
  channel_id = app.channel_id
  ch_channel = app.ch_channel
  if chatter != None and chatmode != None and chat_user != None:
    if isinstance(message.channel, discord.DMChannel) and message.author.id == chat_user_id:
      await ch_channel.send(message.content)
      return
    if isinstance(message.channel, discord.TextChannel) and message.channel.id == chat_user_id:
      await ch_channel.send(f"{message.author.name}: {message.content}")
      return
    if message and message.channel.id == channel_id:
      if isinstance(chat_user, discord.TextChannel):
        await chat_user.send(f"{message.author.name}: {message.content}")
        return
      await chat_user.send(f"{message.author.name}: {message.content}")
  else:
    pass

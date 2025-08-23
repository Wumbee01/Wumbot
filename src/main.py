from cogs import command, vars
from cogs.message import _message
from cogs.message_edit import _message_edit
import discord
import os
from cogs.vars import *
import asyncio

asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

bot = command.bot

@bot.event
async def on_message(message):
  if not os.path.exists("disabled.txt"):
    await _message(message)
  msg = message.content.lower()
  if "cum" == msg:
    if message.author.id != wumbee:
      await message.reply("Tf?")
      return
    if os.path.exists("disabled.txt"):
      await message.reply("*Wtf bro im full*")
      return
    with open('disabled.txt', 'w'):
      pass
    await message.reply("*Mouth is full*")
  if "uncum" == msg:
    if message.author.id != wumbee:
      await message.reply("Bro?")
      return
    if not os.path.exists("disabled.txt"):
      await message.reply("Tf am I supposed to swallow?")
      return
    os.remove('disabled.txt')
    await message.reply("*Swallowed*")
  await bot.process_commands(message)

@bot.event
async def on_message_edit(before, after):
  await _message_edit(before, after)
  await bot.process_commands(after)
  await _message(after)
  
bot.run(os.environ['TOKEN'])

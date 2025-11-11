import discord
import re
import shlex
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
from cogs import vars
from cogs.vars import *

bot = vars.bot
number = None

# Silly commands section
@bot.slash_command(name = "quote")
async def quotestore(interaction):
  pass

@bot.slash_command(name = "whatisdeez", description = "True ultimate command")
async def deez(interaction):
  await interaction.response.send_message("heh... DEEZ NUTS")

@bot.slash_command(name = 'echo', description = "Makes the bot say stuff")
async def echo_slash(interaction, message: str):
  bad_words = ["nigga", "nigger", "@everyone", "@here", "tranny", "fag", "faggot", "clanker", "@"]
  for word in bad_words:
    if word in message.lower():
      message = message.replace(word, 'CENSORED')
  await interaction.channel.send(f'{interaction.user.mention} wanted me to say "{message}"! :3')
  await interaction.response.send_message("Hehehe", ephemeral=True)

@bot.slash_command(name = 'lag', description = "Makes the bot lag you (spam)")
async def spam(interaction):
  await interaction.channel.send("<a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800><a:congaparroter:1142006542175047800>")
  await interaction.response.send_message("Hehehe", ephemeral=True)

@bot.slash_command(name = "ping", description = "Ping somebody indirectly")
async def ping_pong(interaction, member: discord.Member, reason: Option(str, required = False)):
  if reason == None:
    await interaction.response.send_message(f"<@{interaction.user.mention} why'd you ping?")
    await interaction.channel.send(f"{member.mention}, you've been pinged by {interaction.user.name}")
  await interaction.response.send_message(f"{member.mention}, {interaction.user.mention} pinged you for '{reason}'")

@bot.slash_command(name = "poke", description = "Dont do it")
async def poke(interaction):
  poke_r = [f"Hey! don't do that, {interaction.user.mention}", "Bro stop, thats gay", f"{interaction.user.mention} LIKES BOTHERING INNOCENT BOTS!", "I AM IN YOUR WALLS", "AAAAAAAAAAAAAAAA, DONT DO THAT", "*stares menacingly* <:unrelatable:1115559275301978152> <:unrelatable:1115559275301978152> <:unrelatable:1115559275301978152>"]
  await interaction.response.send_message(random.choice(poke_r))
# End of silly commands section

# Bridging command section
@bot.slash_command(name="chatmode", description="Dm someone with the bot (Only use User ID, not mention)")
async def chatmode_slash(ctx, user: str = None, silence: str = None):
  global chatmode
  global chat_user
  global chat_user_id
  global chatter
  global ch_channel
  global channel_id
  if chatmode == None:
    chatmode = "Active"
    channel_id = ctx.channel.id
    if user != None:
      chat_user = await bot.fetch_user(int(user))
      chat_user_id = int(user)
    chatter = ctx.author.id
    ch_channel = discord.utils.get(ctx.guild.channels, id=ctx.channel.id)
    if silence == None:
      await ctx.respond("Chatmode is now active")
    return
  if user == None:
    if chatmode != None:
      chatmode = None
      if silence == None:
        await ctx.respond("Chatmode is now ded")
    else:
      if silence == None:
        await ctx.respond("There is an error or you haven't started chatmode yet")

@bot.slash_command(name="bridge", description="Bridges channels together (Uses Channel ID)")
async def bridge(ctx, channel: str = None, silence: str = None):
  global chatmode
  global chat_user
  global chat_user_id
  global chatter
  global ch_channel
  global channel_id
  if chatmode == None:
    chatmode = "Active"
    channel_id = ctx.channel.id
    if channel != None:
      chat_user = discord.utils.get(bot.get_all_channels(), id=int(channel))
      chat_user_id = int(channel)
    chatter = ctx.author.id
    ch_channel = discord.utils.get(ctx.guild.channels, id=ctx.channel.id)
    if silence != None:
      await ctx.respond("Bridge is now active", ephemeral=True)
      return
    await ctx.respond("Bridge is now active")
    return
  if chatmode != None:
    chatmode = None
    if silence != None:
      await ctx.respond("Bridge is now ded", ephemeral=True)
      return
    await ctx.respond("Bridge is now ded")
  else:
    if silence != None:
      await ctx.respond("There is an error or you haven't started a bridge yet", ephemeral=True)
      return
    await ctx.respond("There is an error or you haven't started a bridge yet")
# End of bridging section

# Help section
class MyView(discord.ui.View):
    def __init__(self):
      super().__init__()
      self.add_item(discord.ui.Button(label="Github", style=discord.ButtonStyle.link, url="https://github.com/Wumbee01/Wumbot", row=1))
    @discord.ui.button(label="Random", row=0, style=discord.ButtonStyle.blurple)
    async def first_button_callback(self, button, interaction):
      FunEmbed = discord.Embed(title="Random commands!", description="*Well, I think they are fun...*", color=0x9d89c9)
      FunEmbed.add_field(name="***Echo:***", value=" **•** (Prefix command) format: !echo <message>, Makes the bot say something", inline=False)
      FunEmbed.add_field(name="***Sudo:***", value=" **•** (Chat command) format: sudo <command>, Linux terminal, but in discord :D", inline=False)
      FunEmbed.add_field(name="***Bash:***", value=" **•** (Prefix command) format: !bash <command>, Linux terminal, but in discord :D (Commmand version)", inline=False)
      FunEmbed.add_field(name="***Cal:***", value=" **•** (Prefix command) format: !cal <number1> <number2> <(optional)operand1> <(optional)operand2>", inline=False)
      FunEmbed.add_field(name="***Ipgrab:***", value=" **•** (Prefix command) format: !ipgrab <user>, Grabs user ip (real)", inline=False)
      FunEmbed.add_field(name="***Flavour:***", value=" **•** (Prefix command) format: !flavour, Choose a flavour!", inline=False)
      FunEmbed.add_field(name="***Spawnping:***", value=" **•** (Slash command) Adds poketwo spawn pings and a spawn role", inline=False)        
      FunEmbed.add_field(name="***Spam:***", value=" **•** (Prefix command) format: !spam <amount> <message>, Sends a message repeatedly (Has major limits)", inline=False)
      FunEmbed.add_field(name="***Spamton:***", value=" **•** (Prefix command) format: !spamton <amount> <message>, Only for me", inline=False)
      FunEmbed.add_field(name="***Mosie Nuke:***", value=" **•** (Prefix command) format: !mosie_nuke, Only for me", inline=False)
      FunEmbed.add_field(name="***Lag:***", value=" **•** (Slash command) Parrot party", inline=False)
      FunEmbed.add_field(name="***Ping:***", value=" **•** (Slash command) Pings Bee", inline=True)
      FunEmbed.add_field(name="***Poke:***", value=" **•** (Slash command) Pokes Wumbot", inline=False)
      FunEmbed.add_field(name="***Support:***", value=" **•** (Slash command) Provides Mali™ support", inline=False)        
      FunEmbed.add_field(name="***Waifuimg:***", value=" **•** (Slash command) Sends a Waifu image (Use /waifuhelp)(Ignore, API stuff practice)", inline=False)
      FunEmbed.add_field(name="***Waifubomb:***", value=" **•** (Slash command) Sends 5 random waifu images(Ignore, API stuff practice)", inline=False)    
      FunEmbed.add_field(name="***Waifuhelp:***", value=" **•** (Slash command) Lists all categories", inline=False)
      FunEmbed.add_field(name="***Bees:***", value=" **•** (Slash command) Sends a Bee image", inline=False)
      FunEmbed.add_field(name="***Raccoons:***", value=" **•** (Slash command) Sends a Raccon image", inline=False)
      FunEmbed.add_field(name="***Whatisdeez:***", value=" **•** (Slash command) Heh...", inline=False)
      FunEmbed.add_field(name="***DMSpam:***", value=" **•** (Prefix command)format: !dmspam <member> <message>, Dont try it lol", inline = False)
      FunEmbed.add_field(name="***Chatmode:***", value=" **•** (Slash command) Links a DM and a channel together", inline = False)
      FunEmbed.add_field(name="***Bridge:***", value=" **•** (Slash command) Links two channels together, can be from different servers", inline = False)
      FunEmbed.add_field(name="***(VC)Join:***", value=" **•** (Prefix command) format: !p <type(url, or search)> <url/search term>, eg: !p search rickroll, Plays a song", inline = False)
      FunEmbed.add_field(name="***(VC)Leave:***", value=" **•** (Prefix command) format: !l, Makes bot leave the vc", inline = False)
      FunEmbed.set_footer(text="Wumbot™")  
      button.disabled = True
      await interaction.response.edit_message(view=self)
      await interaction.followup.send(embed=FunEmbed)
    @discord.ui.button(label="Games", row=0, style=discord.ButtonStyle.blurple)
    async def fourth_button_callback(self, button, interaction):
      GameEmbed = discord.Embed(title="Game commands!", description="*Yep, these exist*", color=0x9d89c9)
      GameEmbed.add_field(name="***Help_ut:***", value=" **•** (Prefix command) format: !help_ut, Help/info on the game", inline=False)
      GameEmbed.add_field(name="***Join_ut:***", value=" **•** (Prefix command) format: !join_ut <character>, Join the game with x character", inline=False)
      GameEmbed.add_field(name="***Start_ut:***", value=" **•** (Prefix command) format: !start_ut, Starts the game", inline=False)
      GameEmbed.add_field(name="***Fight_ut:***", value=" **•** (Prefix command) format: !fight_ut, Fight opponent", inline=False)
      GameEmbed.add_field(name="***Act_ut:***", value=" **•** (Prefix command) format: !act_ut, Use a random action", inline=False)
      GameEmbed.add_field(name="***Mercy_ut:***", value=" **•** (Prefix command) format: !mercy_ut, Spare the player", inline=False)
      GameEmbed.add_field(name="***Stats_ut:***", value=" **•** (Prefix command) format: !stats_ut, See your stats", inline=False)
      GameEmbed.add_field(name="***2ball:***", value=" **•** (Slash command) Yes or no", inline=False)
      GameEmbed.add_field(name="***8ball:***", value=" **•** (Slash command) Classic 8ball", inline=False)
      GameEmbed.add_field(name="***RPS:***", value=" **•** (Slash command) Fancy Rock Paper Scissors", inline=False)
      GameEmbed.add_field(name="***Coinflip:***", value=" **•** (Slash command) Flips a coin", inline=False)
      GameEmbed.add_field(name="***Dice:***", value=" **•** (Prefix command) format: !dice <number>, Chooses a random number from 1 to whatever you chose", inline=False)
      GameEmbed.add_field(name="***Guess:***", value=" **•** (Slash command) Guess a number from 1~10", inline = False)
      GameEmbed.set_footer(text="Wumbot™")  
      button.disabled = True
      await interaction.response.edit_message(view=self)
      await interaction.followup.send(embed=GameEmbed)
    @discord.ui.button(label="Moderation", row=0, style=discord.ButtonStyle.red)
    async def second_button_callback(self, button, interaction):
      embedVar = discord.Embed(title="Moderation", description="Useful for keeping the server clean", color=0x9d89c9)
      embedVar.add_field(name="***Help:***", value=" **•** (Slash command) This command right here", inline=False)              
      embedVar.add_field(name="***Banana:***", value=" **•** (Slash command) Bans an user", inline=False)        
      embedVar.add_field(name="***Unbanana:***", value=" **•** Unbans an user (needs ID)", inline=False)  
      embedVar.add_field(name="***Roleadd:***", value=" **•** (Slash command) Adds a role", inline=False)
      embedVar.add_field(name="***Roleremove:***", value=" **•** (Slash command) Removes a role", inline=False)
      embedVar.add_field(name="***Roles:***", value=" **•** (Slash command) Shows a Member's roles", inline=False)
      embedVar.add_field(name="***Rolelist:***", value=" **•** (Slash command) Lists all roles in the server", inline=False)
      embedVar.add_field(name="***Purge:***", value=" **•** (Slash command) Deletes messages", inline=False)
      embedVar.add_field(name="***Clear:***", value=" **•** (Prefix command) format: !clear <amount> <user>, Deletes messages of a specific user", inline=False)
      embedVar.add_field(name="***Timeout:***", value=" **•** (Slash command) Times out a user", inline=False)
      embedVar.add_field(name="***Unmute:***", value=" **•** (Slash command) Removes timeout from a user", inline=False)
      embedVar.add_field(name="***Censor:***", value=" **•** (Slash command) Censors anything", inline=False)
      button.disabled = True
      await interaction.response.edit_message(view=self)
      await interaction.followup.send(embed=embedVar)
    @discord.ui.button(label="Utility", row=1, style=discord.ButtonStyle.green)
    async def third_button_callback(self, button, interaction):
      Utilbed = discord.Embed(title="Utility commands", description="Only for me ;)", color=0x9d89c9)
      Utilbed.add_field(name="***Killswitch:***", value=" **•** (Prefix command) format: !killswitch, Kills the workflow", inline=False)
      Utilbed.add_field(name="***Update:***", value=" **•** (Prefix command) format: !update, Restarts the bot with updated source", inline=False)
      Utilbed.add_field(name="***Repair:***", value=" **•** (Slash command) Restart, but if on_message is broken", inline=False)
      Utilbed.add_field(name="***Ping:***", value=" **•** (Prefix command) The real ping command this time", inline=False)
      button.disabled = True
      await interaction.response.edit_message(view=self)
      await interaction.followup.send(embed=Utilbed)

@bot.slash_command(description="Help with da Wumbot")
async def help(interaction):
  if interaction.author.id == 727184656209936494:
    await interaction.channel.send("Why tf do you need help?")
    pass
  await interaction.respond("### My commands!\nMy prefixes are !, bee, exec\n\nModeration - Moderation commands\nFun - (Hopefully) Fun commands\nUtility - Only for me\n\nChat reactions - Wumbot reacts to some phrases\n\nChatGPT - Reply to Wumbot or ping him with a message for AI (Using Gemini)", view=MyView())
# End of Help section

# Games section
@bot.slash_command(name = "2ball", description = "Yes or no")
async def twoball(interaction, question: str):
  twoballanswer = ["My answer is yes", "My answer is no"]
  twoballembed = discord.Embed(title = f"Question: {question}", description = f"{random.choice(twoballanswer)}", color=0x9d89c9)
  await interaction.respond(embed=twoballembed)

@bot.slash_command(name = "8ball", description = "Classic 8ball")
async def eightball(interaction, question: str):
  eightballanswer = ["It is certain", "It is decidedly so", "Without a doubt", "Yes, definitely", "You may rely on it", "As I see it, yes", "Most likely", "Outlook good", "Yes", "Signs point to yes", "Reply hazy, try again", "Ask again later", "Better not tell you now", "Cannot predict now", "Concentrate and ask again", "Don't count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful"]
  eightballembed = discord.Embed(title = f"Question: {question}", description = f"{random.choice(eightballanswer)}", color=0x9d89c9)
  await interaction.respond(embed=eightballembed)

def randnum():
  num = random.randint(1, 10) 
  return num

@bot.slash_command(name="guess", description="Guess a number between 1 and 10")
async def insanity(interaction):
  global number
  number = randnum()
  await interaction.respond("Choose a number between 1 and 10")
  await asyncio.sleep(10)
  if number != None:
    await interaction.followup.send("Time's up!\nToo bad...")
  else:
    await interaction.followup.send("Ya win!")
    
def flip_result():
  global choice_bot_flip
  choice_bot_flip = random.choice(["HEADS", "TAILS"])
  global result_flip
  if choice_flip == "HEADS" and choice_bot_flip == "TAILS":
    result_flip = "You Lose!"
  elif choice_flip == "HEADS" and choice_bot_flip == "HEADS":
    result_flip = "You Win!"
  elif choice_flip == "TAILS" and choice_bot_flip == "HEADS":
    result_flip = "You Lose!"
  elif choice_flip == "TAILS" and choice_bot_flip == "TAILS":
    result_flip = "You Win!"
  else:
    result_flip = "Unknown"
    return(1)

@bot.slash_command(name = "coinflip", description = "Flip a coin!")
async def flip(interaction, side: str):
  global choice_flip
  choice_flip = (side.upper())
  flip_result()
  flipembed = discord.Embed(title=result_flip, description=f"***The results are...*** \n **•** Your choice: {choice_flip} \n **•** Flip result: {choice_bot_flip}", color=0x9d89c9)
  if result_flip == "You Lose!":
    flipembed.add_field(name="Hah! you lost!", value="Better luck next time...")
  if result_flip == "You Win!":
    flipembed.add_field(name="So, you won...", value="*You wont always be lucky*")
  await interaction.response.send_message(embed=flipembed)

def game_result():
  global choice_bot
  choice_bot = random.choice(["ROCK", "PAPER", "SCISSORS"])
  global result
  if choice == "ROCK" and choice_bot == "ROCK":
    result = "TIE!"
  elif choice == "ROCK" and choice_bot == "PAPER":
    result = "Bot Wins!"
  elif choice == "ROCK" and choice_bot == "SCISSORS":
    result = "You Win!"
  elif choice == "PAPER" and choice_bot == "ROCK":
    result = "You Win!"
  elif choice == "PAPER" and choice_bot == "PAPER":
    result = "TIE!"
  elif choice == "PAPER" and choice_bot == "SCISSORS":
    result = "Bot Wins!"
  elif choice == "SCISSORS" and choice_bot == "ROCK":
    result = "Bot Wins!"
  elif choice == "SCISSORS" and choice_bot == "PAPER":
    result = "You Win!"
  elif choice == "SCISSORS" and choice_bot == "SCISSORS":
    result = "TIE!"
  else:
    result = "Unknown"
    return(1)

@bot.slash_command(name = "rps", description = "Rock, Paper Scissors!")
async def rps(interaction, your_choice: str):
  global choice
  choice = (your_choice.upper())
  game_result()
  rpsembed = discord.Embed(title=result, description=f"***The choices were...*** \n **•** Your choice: {choice} \n **•** Bot's choice: {choice_bot}", color=0x9d89c9)
  if result == "Bot Wins!":
    rpsembed.add_field(name="Hah! you lost!", value="I win this time")
  if result == "You Win!":
    rpsembed.add_field(name="So, you won...", value="*You wont always be lucky*")
  if result == "TIE!":
    rpsembed.add_field(name="Hmph, a tie", value="Who will win the next one?")
  await interaction.response.send_message(embed=rpsembed)
# End of games section

# Utility Section
@bot.slash_command(name = "censor", description = "Leave empty to remove censors")
@commands.has_permissions(moderate_members = True)
async def censor(interaction, word: str = None, word2: str = None):
  cdata = {
    "Word": word,
    "Word2": word2
  }
  with open("censor.json", "w") as write_file:
    json.dump(cdata, write_file)
  await interaction.respond(f"Censor list:\n- {word}\n- {word2}", ephemeral = True)

@bot.slash_command(name="profile", description="Edit Bots Profile")
async def profile(interaction, name: str, image: discord.Attachment):
  await bot.user.edit(username=name, avatar=await image.read())
  await interaction.response.send_message("Done")

@bot.slash_command(name = "banana", description = "The ultimate command")
@commands.has_permissions(ban_members=True)
async def ban(interaction, member: discord.Member, reason: Option(str, required = False)):
  if member.guild_permissions.administrator:
    await interaction.respond("Nuh uh, das an admin")
    return
  if interaction.user == member:
    await interaction.response.send_message("Dont banana yourself 💀💀💀")
    return
  if reason == None:
    reason = "No reason provided"
  await member.ban(reason = reason)
  await interaction.response.send_message(f"{member.mention} has been banana'd by {interaction.user.mention} for '{reason}'")

@ban.error
async def banerror(ctx, error):
  if isinstance(error, MissingPermissions):
    await ctx.respond("You can't do this! You need to have ban members permissions!")
  else:
    raise error

@bot.slash_command(name = "addrole", description = "Adds a role to a member")
async def addrole(ctx, member: discord.Member, role: discord.Role):
  await member.add_roles(role)
  await ctx.response.send_message(f"Added `{role}` to <@{member.id}>")

@bot.slash_command(name = "unbanana", description = "The second ultimate command")
@commands.has_permissions(ban_members=True)
async def unban(ctx, id: str, reason: Option(str, required = False)):
  user = await bot.fetch_user(id)
  await ctx.guild.unban(user)
  if reason == None:
    reason = "No reason provided"
  await ctx.response.send_message(f"{ctx.user.mention} Unbanana`d <@{id}> for '{reason}'")

@unban.error
async def unbanerror(ctx, error):
  if isinstance(error, MissingPermissions):
    await ctx.respond("You can't do this! You are missing permissions!")
  else:
    raise error
    
@bot.slash_command(name = "removerole", description = "Removes a role from a member")
async def removerole(ctx, member: discord.Member, role: discord.Role):
  await member.remove_roles(role)
  await ctx.response.send_message(f"Removed `{role}` from <@{member.id}>")

@bot.slash_command(name = "purge", description = "Purges messages")
async def purge(ctx, amount: int):
  await ctx.channel.purge(limit=amount)

@bot.slash_command(name = 'roles', description = "Shows the roles of a user")
async def roles_s(ctx, user: discord.Member):
  role_list = ""
  for role in user.roles:
    role_list += f'* {role}\n'
    user_roles = str(role_list).split("@everyone")[1]
  if user.nick == None:
    role_embed = discord.Embed(title=f"{user.name}", description=user_roles, color=0x9d89c9)
  else:
    role_embed = discord.Embed(title=f"{user.nick}", description=user_roles, color=0x9d89c9)
  role_embed.set_image(url=f"{user.avatar.url}")
  await ctx.response.send_message(embed=role_embed)

@bot.slash_command(name="rolelist")
async def rolelist(ctx):
  list = ""
  for roles in ctx.guild.roles:
    list.append(f"\n{roles}")
  await ctx.respond(list)

@bot.slash_command(name = 'timeout', description = "mutes/timeouts a member")
@commands.has_permissions(moderate_members = True)
async def timeout(ctx, member: Option(discord.Member, required = True), reason: Option(str, required = False), days: Option(int, max_value = 27, default = 0, required = False), hours: Option(int, default = 0, required = False), minutes: Option(int, default = 0, required = False), seconds: Option(int, default = 0, required = False)): 
  if member.id == ctx.author.id and ctx.user.id != 727184656209936494:
    await ctx.respond("You can't timeout yourself!")
    return
  if member.guild_permissions.administrator and ctx.user.id != 727184656209936494:
    await ctx.respond("You can't do this, this person is a admin!")
    return
  duration = timedelta(days = days, hours = hours, minutes = minutes, seconds = seconds)
  if duration >= timedelta(days = 28): 
    await ctx.respond("I can't mute someone for more than 28 days!", ephemeral = True)
    return
  if reason == None:
    await member.timeout_for(duration)
    await ctx.respond(f"<@{member.id}> has been timed out for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds by <@{ctx.author.id}>.")
  else:
    await member.timeout_for(duration, reason = reason)
    await ctx.respond(f"<@{member.id}> has been timed out for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds by <@{ctx.author.id}> for '{reason}'.")

@timeout.error
async def timeouterror(ctx, error):
  if isinstance(error, MissingPermissions):
    await ctx.respond("You can't do this! You need to have moderate members permissions!")
  else:
    raise error

@bot.slash_command(name = 'unmute', description = "unmutes/untimeouts a member")
@commands.has_permissions(moderate_members = True)
async def unmute(ctx, member: Option(discord.Member, required = True), reason: Option(str, required = False)):
  if reason == None:
    await member.remove_timeout()
    await ctx.respond(f"<@{member.id}> has been untimed out by <@{ctx.author.id}>.")
  else:
    await member.remove_timeout(reason = reason)
    await ctx.respond(f"<@{member.id}> has been untimed out by <@{ctx.author.id}> for '{reason}'.")

@unmute.error
async def unmuteerror(ctx, error):
  if isinstance(error, MissingPermissions):
    await ctx.respond("You can't do this! You need to have moderate members permissions!")
  else:
    raise error

@bot.slash_command(description = 'Sets up Pokétwo pings!')
async def spawnping(ctx):
  try:
    s_role = discord.utils.get(ctx.guild.roles, name="spawn")
    await ctx.user.add_roles(s_role)
    await ctx.respond("Role added!")
  except Exception as e:
    await ctx.send(e)
# End of utilities section

### Remnants from image fetching practice, do not the sus

# api.waifu
def get_waifu(type, category):
  url = "https://api.waifu.im/search"
  if category == "nsfw":
    params = {
      'included_tags': [type],
      'is_nsfw': 'true',
      'gif': True
    }
  else:
    params = {
      'included_tags': [type],
      'is_nsfw': 'false'
    }
  data = requests.get(url, params=params)
  json = data.json()
  return json
  
@bot.slash_command(name = "waifuimg", description = "Powered by waifu API")
async def totallysfw(interaction, category: str, type: Option(str, required = False)):
  global waifu_type
  global waifu_category
  global url_json
  if type != None:
    waifu_type = (type.lower())
  waifu_type = type
  waifu_category = (category.lower())
  if waifu_category == "sfw":
    if waifu_type == None:
      waifu_type = ["maid", "waifu", "marin-kitagawa", "mori-calliope", "raiden-shogun", "oppai", "selfies", "uniform", "kamisato-ayaka"]
      url_json = get_waifu(random.choice(waifu_type), "sfw")
      await interaction.response.send_message(url_json["images"][0]["url"])
      return
    else:
      url_json = get_waifu(waifu_type, "sfw")
      await interaction.response.send_message(url_json["images"][0]["url"])
      return
  if waifu_category == "nsfw":
    if interaction.channel.is_nsfw():
      if waifu_type == None:
        waifu_type = ["ass", "hentai", "milf", "oral", "paizuri", "ecchi", "ero"]
        url_json = get_waifu(random.choice(waifu_type), "nsfw")
        await interaction.response.send_message(url_json["images"][0]["url"])
        return
      else:
        url_json = get_waifu(waifu_type, "nsfw")
        await interaction.response.send_message(url_json["images"][0]["url"])
        return
    else:
      await interaction.response.send_message("Wrong channel buddy")
      return
  
@bot.slash_command(name = "waifuhelp", description = "Sends all categories")
async def waifuhelp(interaction):
  await interaction.response.send_message("### Waifu categories:\n\nSfw, Nsfw\n\n### Waifu types:\n\n***Sfw:*** waifu, neko, shinobu, bully, cuddle, cry, hug, awoo, kiss, lick, pat, smug, bonk, yeet, blush, smile, wave, highfive, handhold, nom, bite, glomp, slap, kill, kick, happy, wink, poke, dance, cringe\n\n***Nsfw (only works in a nsfw channel):*** waifu, trap, neko")

@bot.slash_command(name = "waifubomb", description = "Powered by waifu API")
async def totallysfwbomb(interaction, category: str):
  waifu_category = (category.lower())
  await interaction.respond(f"Bombed by {interaction.user.mention}")
  if waifu_category == "sfw":
    for i in range(5):
      waifu_type = ["maid", "waifu", "marin-kitagawa", "mori-calliope", "raiden-shogun", "oppai", "selfies", "uniform", "kamisato-ayaka"]
      url_json = get_waifu(random.choice(waifu_type), "sfw")
      await interaction.channel.send(url_json["images"][0]["url"])
    return
  if waifu_category == "nsfw":
    if interaction.channel.is_nsfw():
      for i in range(5):
        waifu_type = ["ass", "hentai", "milf", "oral", "paizuri", "ero"]
        url_json = get_waifu(random.choice(waifu_type), "nsfw")        
        await interaction.channel.send(url_json["images"][0]["url"])
      for i in range(5):
        waifu_type = ["hentai"]
        url_json = get_waifu(random.choice(waifu_type), "nsfw")        
        await interaction.channel.send(url_json["images"][0]["url"])
      return
    else:
      await interaction.followup.send("Nvm wrong channel buddy")

# Depreciated image fetchers (fuck reddit)
"""
def urlDec(url):
  encoded = url.replace('amp;s', 's')
  doubleEncoded = encoded.replace('amp;', '')
  tripleEncoded = doubleEncoded.replace('amp;', '')
  return tripleEncoded

@bot.slash_command(name = "bees", description = "Sends a bee")
async def bee(ctx):
  async def getUrl():
    new_url = ""
    api = requests.get(url="https://www.reddit.com/r/bees/random.json",headers={'User-agent': 'Wumbee01'}).json()
    try:
      url = api[0]['data']['children'][0]['data']['preview']['images'][0][
        'source']['url']
      new_url = urlDec(url)
    except:
      await getUrl()
    await ctx.respond(new_url)
    os.system("clear")
    return
  await getUrl()

@bot.slash_command(name = "raccoons", description = "Sends a raccoon")
async def raccoons(ctx):
  async def getUrl():
    new_url = ""
    api = requests.get(url="https://www.reddit.com/r/Raccoons/random.json",headers={'User-agent': 'Wumbee01'}).json()
    try:
      url = api[0]['data']['children'][0]['data']['preview']['images'][0]['source']['url']
      new_url = urlDec(url)
    except:
      await getUrl()
    await ctx.respond(new_url)
    os.system("clear")
    return
  await getUrl()
"""


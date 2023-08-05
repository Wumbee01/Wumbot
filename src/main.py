import time
import os, sys
import discord
import requests
from discord.ext import commands

prefix = "Izu "
intents = discord.Intents.all()
activity = discord.Game(name='Izuku™  |  Izu')
bot = commands.Bot(prefix, intents=intents, activity=activity, status=None)


@bot.tree.command(name="help", description="a little usage info of mine.!")
async def help(interaction):
  await interaction.response.send_message("nothing here yet xD")


@bot.command()
async def sync(ctx):
  if ctx.author.id != 1098141251209023538:
    return 0
  for guild in bot.guilds:
    await bot.tree.sync(guild=discord.Object(id=guild.id))
    await ctx.channel.send(f"tree __synchronised__ to: **{guild.name}**")


@bot.command()
async def reboot(ctx):
  if ctx.author.id == 1098141251209023538:
    await ctx.reply("going to bed see ya..!")
    sys.exit(0)
  else:
    await ctx.reply("can't sleep atm!")

@bot.command(pass_context=True)
async def ping(ctx):
    await ctx.message.delete()
    before = time.monotonic()
    message = await ctx.send("`Pong!``")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"`Pong!  {int(ping)}ms`")

@bot.command()
async def purge(ctx, limit: int, user: discord.Member = None):
  if 1134589637852147822 in [role.id for role in ctx.author.roles]:
    pass
  else:
    await ctx.reply("you can't use the command `[code]` only!!")
    return
  await ctx.message.delete()
  if user is None:
    await ctx.channel.purge(limit=limit)
  else:
    await ctx.channel.purge(limit=limit,
                            check=lambda message: message.author == user)


@bot.command()
async def roles(ctx, user: discord.Member = None):
  if user == None:
    ctx.reply("No user mentioned.!")
    return 0
  gfhfhfh = ""
  for role in user.roles:
    print(role.id)
    gfhfhfh += f'{role}\n'
    user_roles = str(gfhfhfh).split("@everyone")[1]
    embed = discord.Embed(title=f'{user.name}',
                          description=f'{user_roles}',
                          color=0xecce8b)
  embed.set_image(url=f'{user.avatar.url}')
  await ctx.reply(embed=embed)


@bot.command()
async def hunt(ctx):
  if ctx.channel.is_nsfw():
    data = requests.get(url="https://api.waifu.pics/sfw/waifu").json()
    embed = discord.Embed(title=None, description=None)
    embed.set_image(url=data['url'])
    await ctx.channel.send(embed=embed)
  else:
    await ctx.reply(f"try here:\n>><#1136550691943485500><<")

##async def channel(ctx, channel: discord.TextChannel = None):

@bot.event
async def on_ready():
  os.system("clear")
  print(bot.user)
  code_bot = discord.utils.get(bot.get_all_channels(), id=1134599357577044138)
  await code_bot.send("i m back <:stretchreaction:1134595302641381496>")


bot.run(sys.argv[1])

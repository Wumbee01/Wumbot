import os
import discord
from discord.ext import commands

global p1
global p2
p1 = None
p2 = None
global current_player
current_player = None
global p1_data
global p2_data
p1_data = None
p2_data = None

# char = atk, hp, accuracy, crit
global mage
global rogue
mage = [12, 60, 65, 15]
rogue = [7, 70, 85, 35]

global players
global amt_players
players = {}
amt_players = 0

heal = 15

global pkg_state
pkg_state = None

global ch_channel
global chatter
global chat_user
global chatmode
global channel_id
global chat_user_id
chat_user_id = None
chatter = None
chat_user = None
chatmode = None
ch_channel = None
channel_id = None

global wumbee
wumbee = 727184656209936494

prefix = ["!"]
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.message_content = True
bot = commands.Bot(prefix, intents=intents)

import discord
import os
import re
import random
from replit import db
from roll_dice import Dice
from guild_db import GuildDB
from keep_alive import keep_alive

bot = discord.Client()
guild = GuildDB()
dice = Dice()

@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))
  await bot.change_presence(activity=discord.Game(name='RPG'))

@bot.event
async def on_message(msg):
  if msg.author == bot.user:
    return

  # ---------------------------------------------------
  # respostas padrao

  if str(bot.user.id) in msg.content:
    await msg.channel.send(guild.whoami)
  
  if msg.content.startswith('legen!dary'):
    option = random.randint(0, 7)
    await msg.channel.send('<@'+str(msg.author.id)+'>, '+guild.legendary[option])


  # ---------------------------------------------------
  # definicao de canal secreto
  
  guild_id = str(msg.guild.id)

  if msg.content.startswith('legen!sch'):
    if msg.author.guild_permissions.manage_channels:
      guild.update_sch(guild_id, msg.content)
      await msg.channel.send(guild.operationStatus)
    else:
      await msg.channel.send('<@'+str(msg.author.id)+'>, '+guild.sorry)
  
  if msg.content.startswith('legen!del'):
    if msg.author.guild_permissions.manage_channels:
      if guild_id in db.keys():
        guild.delete_sch(guild_id)
        await msg.channel.send(guild.operationStatus)
    else:
      await msg.channel.send('<@'+str(msg.author.id)+'>, '+guild.sorry)
  
  if msg.content.startswith('legen!list'):
    if msg.author.guild_permissions.administrator:
      await msg.channel.send(list(db.keys()))
    else:
      await msg.channel.send('<@'+str(msg.author.id)+'>, '+guild.sorry)


  # ---------------------------------------------------
  # usar canal secreto

  if re.match('[0-9]+[Ss]?[Dd][0-9]+', msg.content):
    try:
      if re.match('[0-9]+[Ss]', msg.content) and (guild_id in db.keys()):
        secretChannel = bot.get_channel(int(db[guild_id]))
        diceName = msg.content.lower().replace('sd','d')
        rollResults = dice.roll(diceName)
        await msg.channel.send('<@'+str(msg.author.id)+'>, '+ guild.awesome)
        await secretChannel.send('<@'+str(msg.author.id)+'>,\n' + rollResults)
      else:
        diceName = msg.content.lower()
        rollResults = dice.roll(diceName)
        await msg.channel.send('<@'+str(msg.author.id)+'>, '+ guild.awesome + '\n' + rollResults)
    except ValueError:
      return
  
  if msg.content.startswith('legen!roll'):
    if msg.author.guild_permissions.administrator:
      await msg.channel.send(dice.roll_test())
    else:
      await msg.channel.send('<@'+str(msg.author.id)+'>, '+guild.sorry)


  # ---------------------------------------------------

keep_alive()
bot.run(os.getenv('TOKEN'))

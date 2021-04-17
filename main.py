import discord
import os
import re
from roll_dice import random, Dice
from guild_db import db, GuildDB
from keep_alive import keep_alive

bot = discord.Client()
guild = GuildDB()
dice = Dice()

@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))
  await bot.change_presence(activity=discord.Game(name='RPG'))

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  # ---------------------------------------------------
  # respostas padrao

  if str(bot.user.id) in message.content:
    await message.channel.send(guild.whoami)
  
  if message.content.startswith('legen!dary'):
    option = random.randint(0, 7)
    await message.channel.send('<@'+str(message.author.id)+'>, '+guild.legendary[option])


  # ---------------------------------------------------
  # definicao de canal secreto
  
  guild_id = str(message.guild.id)

  if message.content.startswith('legen!ch'):
    if message.author.guild_permissions.manage_channels:
      guild.update_sch(guild_id, message.content)
      await message.channel.send(guild.operationStatus)
    else:
      await message.channel.send('<@'+str(message.author.id)+'>, '+guild.sorry)
  
  if message.content.startswith('legen!del'):
    if message.author.guild_permissions.manage_channels:
      if guild_id in db.keys():
        guild.delete_sch(guild_id)
        await message.channel.send(guild.operationStatus)
    else:
      await message.channel.send('<@'+str(message.author.id)+'>, '+guild.sorry)
  
  if message.content.startswith('play!book'):
    if message.author.guild_permissions.manage_channels:
      if guild_id in db.keys():
        await message.channel.send('<#'+db[guild_id]+'> \u27F5 The Secret Channel')
      else:
        await message.channel.send(guild.sometimes)
    else:
      await message.channel.send('<@'+str(message.author.id)+'>, '+guild.sorry)


  # ---------------------------------------------------
  # usar canal secreto

  if re.match('[0-9]+[Ss]?[Dd][0-9]+', message.content):
    try:
      if re.match('[0-9]+[Ss]', message.content) and (guild_id in db.keys()):
        secretChannel = bot.get_channel(int(db[guild_id]))
        diceName = message.content.lower().replace('sd','d')
        rollResults = dice.roll(diceName)
        await message.channel.send('<@'+str(message.author.id)+'>, '+ guild.awesome)
        await secretChannel.send('<@'+str(message.author.id)+'>,\n' + rollResults)
      else:
        diceName = message.content.lower()
        rollResults = dice.roll(diceName)
        await message.channel.send('<@'+str(message.author.id)+'>, '+ guild.awesome + '\n' + rollResults)
    except ValueError:
      return


  # ---------------------------------------------------

keep_alive()
bot.run(os.getenv('TOKEN'))

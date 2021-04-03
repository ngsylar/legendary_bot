import discord
import os
import re
from roll_dice import random, Dice
from guild_db import db, GuildDB
from keep_alive import keep_alive

client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  await client.change_presence(activity=discord.Game(name='RPG'))

@client.event
async def on_message(message):
  msgAuthor = message.author.guild_permissions
  msg = message.content
  server = GuildDB()

  if message.author == client.user:
    return

  # ---------------------------------------------------
  # respostas padrao

  if str(client.user.id) in msg:
    await message.channel.send(server.whoami)
  
  if msg.startswith('legen!dary'):
    option = random.randint(0, 7)
    await message.channel.send('<@'+str(message.author.id)+'>, '+server.legendary[option])


  # ---------------------------------------------------
  # definicao de canal secreto
  
  server_id = str(message.guild.id)

  if msg.startswith('legen!ch'):
    if msgAuthor.manage_channels:
      server.update_sch(server_id, msg)
      await message.channel.send(server.operationStatus)
    else:
      await message.channel.send('<@'+str(message.author.id)+'>, '+server.sorry)
  
  if msg.startswith('legen!del'):
    if msgAuthor.manage_channels:
      if server_id in db.keys():
        server.delete_sch(server_id)
        await message.channel.send(server.operationStatus)
    else:
      await message.channel.send('<@'+str(message.author.id)+'>, '+server.sorry)
  
  if msg.startswith('play!book'):
    if msgAuthor.manage_channels:
      if server_id in db.keys():
        await message.channel.send('<#'+db[server_id]+'> \u27F5 The Secret Channel')
      else:
        await message.channel.send(server.sometimes)
    else:
      await message.channel.send('<@'+str(message.author.id)+'>, '+server.sorry)


  # ---------------------------------------------------
  # usar canal secreto

  if re.match('[0-9]+[Ss]?[Dd][0-9]+', msg):
    dice = Dice()
    try:
      if re.match('[0-9]+[Ss]', msg) and (server_id in db.keys()):
        secretChannel = client.get_channel(int(db[server_id]))
        diceName = msg.lower().replace('sd','d')
        rollResults = dice.roll(diceName)
        await message.channel.send('<@'+str(message.author.id)+'>, '+ server.awesome)
        await secretChannel.send('<@'+str(message.author.id)+'>,\n' + rollResults)
      else:
        diceName = msg.lower()
        rollResults = dice.roll(diceName)
        await message.channel.send('<@'+str(message.author.id)+'>, '+ server.awesome + '\n' + rollResults)
    except ValueError:
      return


  # ---------------------------------------------------

keep_alive()
client.run(os.getenv('TOKEN'))

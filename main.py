import discord
import os
import re
from roll_dice import random, Dice
from guild_db import db, Gdb
from keep_alive import keep_alive

client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  # ---------------------------------------------------
  # respostas padrao

  if str(client.user.id) in msg:
    await message.channel.send(Gdb.whoami[0])
  
  if msg.startswith('legen!dary'):
    option = random.randint(0, 7)
    await message.channel.send('<@'+str(message.author.id)+'>, '+Gdb.legendary[option])


  # ---------------------------------------------------
  # definir de canal secreto
  
  server_id = str(message.guild.id)

  if msg.startswith('legen!new'):
    if message.author.guild_permissions.manage_channels:
      schn = msg.split('legen!new ', 1)[1]
      if (len(schn) > 1) and (schn[1] == '#'):
        schn = msg.split('#', 1)[1][:-1]
      Gdb.update_sch(server_id, schn)
      await message.channel.send(Gdb.whoami[1])
    else:
      await message.channel.send('<@'+str(message.author.id)+'>, '+Gdb.sorry)
  
  if msg.startswith('legen!del'):
    if message.author.guild_permissions.manage_channels:
      if server_id in db.keys():
        Gdb.delete_sch(server_id)
        await message.channel.send(Gdb.whoami[2])
    else:
      await message.channel.send('<@'+str(message.author.id)+'>, '+Gdb.sorry)
  
  if msg.startswith('play!book'):
    if message.author.guild_permissions.manage_channels:
      if server_id in db.keys():
        await message.channel.send('<#'+db[server_id]+'> \u27F5 The Secret Channel')
#         user_roles = []
#         for role in message.author.roles:
#           user_roles.append(role.name)
#         await message.channel.send(user_roles)
      else:
        await message.channel.send(Gdb.whoami[3])
    else:
      await message.channel.send('<@'+str(message.author.id)+'>, '+Gdb.sorry)


  # ---------------------------------------------------
  # usar canal secreto

  if re.match('[0-9]+[Ss]?[Dd][0-9]+', msg):
    dice = Dice()
    if re.match('[0-9]+[Ss]', msg) and (server_id in db.keys()):
      try:
        dicename = msg.lower().replace('sd','d')
        sendmsg = dice.roll(dicename)
        sch = client.get_channel(int(db[server_id]))
        option = random.randint(0, 1)
        await message.channel.send('<@'+str(message.author.id)+'>, '+Gdb.awesome[option])
        await sch.send('<@'+str(message.author.id)+'>,\n'+sendmsg)
      except ValueError:
        return
    else:
      try:
        sendmsg = dice.roll(msg.lower())
        option = random.randint(0, 1)
        await message.channel.send('<@'+str(message.author.id)+'>, '+Gdb.awesome[option]+'\n'+sendmsg)
      except ValueError:
        return

  # ---------------------------------------------------


keep_alive()
client.run(os.getenv('TOKEN'))

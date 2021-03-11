import discord
import os
import random
from guild_db import db, Gdb
from keep_alive import keep_alive

client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


# eventos

@client.event
async def on_message(message):
  if message.author == client.user:
    return


  # respostas padrao

  msg = message.content

  if str(client.user.id) in msg:
    await message.channel.send(Gdb.whoami[0])
  
  if msg.startswith('legen!dary'):
    option = random.randint(0, 7)
    await message.channel.send('<@'+str(message.author.id)+'>, '+Gdb.legendary[option])


  # definir de canal secreto
  
  server_id = str(message.guild.id)

  if msg.startswith('legen!new'):
    if message.author.guild_permissions.administrator:
      schn = msg.split('legen!new ', 1)[1]
      if (len(schn) > 1) and (schn[1] == '#'):
        schn = msg.split('#', 1)[1][:-1]
      Gdb.update_sch(server_id, schn)
      await message.channel.send(Gdb.whoami[1])
    else:
      await message.channel.send('<@'+str(message.author.id)+'>, '+Gdb.sorry)
  
  if msg.startswith('legen!del'):
    if message.author.guild_permissions.administrator:
      if server_id in db.keys():
        Gdb.delete_sch(server_id)
        await message.channel.send(Gdb.whoami[2])
    else:
      await message.channel.send('<@'+str(message.author.id)+'>, '+Gdb.sorry)
  
  if msg.startswith('legen!list'):
    if message.author.guild_permissions.administrator:
      if server_id in db.keys():
        await message.channel.send(db[server_id])
      else:
        await message.channel.send(Gdb.whoami[3])
    else:
      await message.channel.send('<@'+str(message.author.id)+'>, '+Gdb.sorry)


  # usar canal secreto

  if 'sd' in msg:
    # se existe canal secreto
    if server_id in db.keys():
      dices = []
      raw1 = msg.casefold().split('sd', 1)
      try:
        if int(raw1[0]) > 0:
          raw2 = raw1[1].split('+', 1)
          scope = int(raw1[0])
          multi = 0

          # lancar dados
          for i in range(scope):
            value = random.randint(1, int(raw2[0]))
            if len(raw2) > 1:
              if raw2[1][-1].casefold() == 'e':
                multi = 1
                raw2[1] = raw2[1][:-1]
              dicesum = int(raw2[1])
            dices.append(value)

        # dados somados
        if len(raw2) > 1:
          if multi:
            values = []
            valsum = 0
            for dice in dices:
              value = dice + dicesum
              values.append(value)
              valsum = valsum + value
            sendmsg = '` '+str(valsum)+' `'+' \u27F5 '+str(values)+' '+str(raw1[0])+'d'+str(raw2[0])+' + '+str(dicesum)+' each'

          # dados normais com soma final
          else:
            values = []
            valsum = 0
            for dice in dices:
              values.append(dice)
              valsum = valsum + dice
            valsum = valsum + dicesum
            sendmsg = '` '+str(valsum)+' `'+' \u27F5 '+str(values)+' '+str(raw1[0])+'d'+str(raw2[0])+' + '+str(dicesum)
        
        # dados normais
        else:
          values = []
          valsum = 0
          for dice in dices:
            values.append(dice)
            valsum = valsum + dice
          sendmsg = '` '+str(valsum)+' `'+' \u27F5 '+str(values)+' '+str(raw1[0])+'d'+str(raw2[0])
      
      except ValueError:
        return

      sch = client.get_channel(int(db[server_id]))
      option = random.randint(0, 1)
      await message.channel.send('<@'+str(message.author.id)+'>, '+Gdb.awesome[option])
      await sch.send('<@'+str(message.author.id)+'>,\n'+sendmsg)
    else:
      await message.channel.send(Gdb.sorry)


keep_alive()
client.run(os.getenv('TOKEN'))
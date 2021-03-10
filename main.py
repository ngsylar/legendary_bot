import discord
import os
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()


# banco de dados do servidor

def update_sch(server_id, schn):
  db[server_id] = schn

def delete_sch(server_id):
  if server_id in db.keys():
    del db[server_id]

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
  awesome = ['that is awesome!', 'challenge accepted!']
  legendary = ['believe it or not, you were not always as awesome as you are today.', 'you poor thing. Having to grow up in the Insula, with the Palace right there.', 'sometimes we search for one thing but discover another.']

  if str(client.user.id) in msg:
    await message.channel.send('Think of me as Yoda, only instead of being little and green, I wear suits and I\'m awesome. I\'m your bro: I\'m Broda!')


  # definir de canal secreto
  
  server_id = str(message.guild.id)

  if msg.startswith('legen!new'):
    if message.author.guild_permissions.administrator:
      schn = msg.split('legen!new ', 1)[1]
      if (len(schn) > 1) and (schn[1] == '#'):
        schn = msg.split('#', 1)[1][:-1]
      update_sch(server_id, schn)
      await message.channel.send('That is awesome!')
    else:
      await message.channel.send('<@'+str(message.author.id)+'>, I\'m sorry, I can\'t hear you over the sound of how awesome I am.')
  
  if msg.startswith('legen!del'):
    if message.author.guild_permissions.administrator:
      if server_id in db.keys():
        delete_sch(server_id)
        await message.channel.send('Challenge accepted!')
    else:
      await message.channel.send('<@'+str(message.author.id)+'>, I\'m sorry, I can\'t hear you over the sound of how awesome I am.')
  
  if msg.startswith('legen!list'):
    if message.author.guild_permissions.administrator:
      if server_id in db.keys():
        await message.channel.send(db[server_id])
      else:
        await message.channel.send('Sometimes we search for one thing but discover another.')
    else:
      await message.channel.send('<@'+str(message.author.id)+'>, I\'m sorry, I can\'t hear you over the sound of how awesome I am.')
  
  if msg.startswith('legen!dary'):
    option = random.randint(0, 2)
    await message.channel.send('<@'+str(message.author.id)+'>, '+legendary[option])


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
              dices.append([value, dicesum])
            else:
              dices.append([value])

        if len(raw2) > 1:
          # dados somados
          if multi:
            values = []
            valsum = 0
            for dice in dices:
              value = dice[0] + dicesum
              values.append(value)
              valsum = valsum + value
            sendmsg = '` '+str(valsum)+' `'+' \u27F5 '+str(values)+' '+str(raw1[0])+'d'+str(raw2[0])+' + '+str(dicesum)+' each'

          # dados normais com soma final
          else:
            values = []
            valsum = 0
            for dice in dices:
              values.append(dice[0])
              valsum = valsum + dice[0]
            valsum = valsum + dicesum
            sendmsg = '` '+str(valsum)+' `'+' \u27F5 '+str(values)+' '+str(raw1[0])+'d'+str(raw2[0])+' + '+str(dicesum)
        
        # dados normais
        else:
          values = []
          valsum = 0
          for dice in dices:
            values.append(dice[0])
            valsum = valsum + dice[0]
          sendmsg = '` '+str(valsum)+' `'+' \u27F5 '+str(values)+' '+str(raw1[0])+'d'+str(raw2[0])
      
      except ValueError:
        return

      sch = client.get_channel(int(db[server_id]))
      option = random.randint(0, 1)
      await message.channel.send('<@'+str(message.author.id)+'>, '+awesome[option])
      await sch.send('<@'+str(message.author.id)+'>,\n'+sendmsg)
    else:
      await message.channel.send('I\'m sorry, I can\'t hear you over the sound of how awesome I am.')


keep_alive()
client.run(os.getenv('TOKEN'))

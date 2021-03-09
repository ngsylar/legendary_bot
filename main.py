import discord
import os
from replit import db

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
  challenge = ['challenge', 'desafio']

  if str(client.user.id) in msg:
    await message.channel.send('Think of me as Yoda, only instead of being little and green, I wear suits and I\'m awesome. I\'m your bro: I\'m Broda!')
    
  if any(word in msg.casefold() for word in challenge):
    await message.channel.send('Challenge accepted!')


  # definir de canal secreto
  
  server_id = str(message.guild.id)

  if msg.startswith('leg!new'):
    schn = msg.split('leg!new ', 1)[1]
    update_sch(server_id, schn)
    await message.channel.send('That is awesome!')
  
  if msg.startswith('leg!del'):
    if server_id in db.keys():
      delete_sch(server_id)
      await message.channel.send('I\'m sorry, I can\'t hear you over the sound of how awesome I am.')
  
  if msg.startswith('leg!list'):
    if server_id in db.keys():
      await message.channel.send(db[server_id])
    else:
      await message.channel.send('Sometimes we search for one thing but discover another.')
  

  # usar canal secreto

  if 'testando' in msg:
    if server_id in db.keys():
      sch = client.get_channel(int(db[server_id]))
      await sch.send('<@'+str(message.author.id)+'>,\nsucesso!')


client.run(os.getenv('TOKEN'))

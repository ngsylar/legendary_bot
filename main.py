import discord
import os
import re
from roll_dice import Dice
from guild_db import GuildDB
from auto_responder import AutoResponder
from keep_alive import keep_alive

reply = AutoResponder()
bot = discord.Client()
guild = GuildDB()
dice = Dice()

@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))
  await bot.change_presence(activity=discord.Game(name='RPG'))

@bot.event
async def on_message(msg):
  # nao responda a si mesmo nem a outros bots
  if msg.author.bot:
    return

  # ----------------------------------------------------------------------------------------------
  # respostas padrao

  # mencionou meu nome? vou contar-lhe quem sou
  elif str(bot.user.id) in msg.content:
    await msg.channel.send(reply.whoami)
  
  # aqui vai um proverbio lendario
  elif re.match(r'legen!dary\s*$', msg.content):
    await msg.channel.send(reply.legendary_quote(msg))


  # ----------------------------------------------------------------------------------------------
  # definicao de canal secreto
  # falta ainda: add cargos

  # definir ou consultar o canal secreto
  elif re.match(r'legen!sch\s*', msg.content):
    if msg.author.guild_permissions.manage_channels:
      guild.update_sch(msg)
      await msg.channel.send(guild.queryResult)
    else:
      await msg.channel.send(reply.sorry_quote(msg))
  
  # remover algum registro do BD do servidor
  elif re.match(r'legen!del\s*', msg.content):
    if msg.author.guild_permissions.manage_channels:
      guild.remove_record(msg)
      await msg.channel.send(guild.successful_op)
    else:
      await msg.channel.send(reply.sorry_quote(msg))
  
  # if msg.content.startswith('legen!list'):
  #   if msg.author.guild_permissions.administrator:
  #     if guild_id in db.keys():
  #       guild_db = db[guild_id]
  #       await msg.channel.send(str(guild_db))
  #     else:
  #       await msg.channel.send(reply.sorry_quote(msg))
  #   else:
  #     await msg.channel.send(reply.sorry_quote(msg))


  # ----------------------------------------------------------------------------------------------
  # usar canal secreto
  # falta ainda: hidden dice

  if re.match(dice.nameRegex, msg.content):
    try:
      guild.get_gid_gdb_sch(msg, bot)
      dice.roll(msg.content)
      
      if dice.isSecret:
        await msg.channel.send('<@'+str(msg.author.id)+'>, '+ reply.awesome)
        await guild.sch.send('<@'+str(msg.author.id)+'>,\n' + dice.rollResults)
      else:
        await msg.channel.send('<@'+str(msg.author.id)+'>, '+ reply.awesome + '\n' + dice.rollResults)
    except ValueError:
      return
  
  if msg.content.startswith('legen!roll'):
    if msg.author.guild_permissions.administrator:
      dice.roll_test()
      await msg.channel.send(dice.rollResults)
    else:
      await msg.channel.send(reply.sorry_quote(msg))


  # ----------------------------------------------------------------------------------------------

keep_alive()
bot.run(os.getenv('TOKEN'))

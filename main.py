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
    await reply.whoami_quote(msg)
  
  # aqui vai um proverbio lendario
  elif re.match(r'legen!dary\s*$', msg.content):
    await reply.legendary_quote(msg)

  # quer saber o que eu faco?
  # falta ainda: terminar essa funcao
  elif re.match(r'legen!help\s*', msg.content):
    await reply.please_quote(msg, bot)


  # ----------------------------------------------------------------------------------------------
  # operacoes com banco de dados
  # falta ainda: add cargos

  # definir ou consultar o canal secreto
  elif re.match(r'legen!sch\s*', msg.content):
    if msg.author.guild_permissions.manage_channels:
      guild.update_sch(msg)
      await reply.db_query(msg, guild)
    else:
      await reply.sorry_quote(msg)
  
  # remover algum registro do BD do servidor
  elif re.match(r'legen!del\s*', msg.content):
    if msg.author.guild_permissions.manage_channels:
      guild.remove_record(msg)
      await reply.op_status(msg, guild)
    else:
      await reply.sorry_quote(msg)


  # ----------------------------------------------------------------------------------------------
  # rolar dados

  elif re.match(dice.nameRegex, msg.content):
    try:
      dice.roll(msg.content)
      
      if dice.isSecret:
        await reply.challenge_quote(msg)
        await reply.roll_result(msg, dice, guild, bot)
      
      elif dice.isHidden:
        await msg.delete()
        await reply.roll_result(msg, dice, guild, bot)
      
      else:
        await reply.roll_result(msg, dice)
    
    except:
      return
  
  elif re.match(r'legen!roll\s*', msg.content):
    if msg.author.guild_permissions.administrator:
      dice.roll_test()
      await reply.roll_result(msg, dice)
    else:
      await reply.sorry_quote(msg)


  # ----------------------------------------------------------------------------------------------

keep_alive()
bot.run(os.getenv('TOKEN'))

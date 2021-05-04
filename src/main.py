import discord
import os
import gdb
import botio
from roll_dice import Dice
from keep_alive import keep_alive

bot = discord.Client()
cmd = botio.CommandAnalyzer()
reply = botio.AutoResponder()
user = gdb.GuildMember()
guild = gdb.GuildDB()
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
  elif cmd.match('legen!dary', msg, cmd.ONLY):
    await reply.legendary_quote(msg)

  # quer saber o que eu faco?
  # falta ainda: terminar essa funcao
  elif cmd.match('legen!help', msg, cmd.AND_TEXT_BODY):
    await reply.please_quote(msg, cmd, bot)


  # ----------------------------------------------------------------------------------------------
  # operacoes com banco de dados

  # definir ou consultar o canal secreto
  elif cmd.match('legen!sch', msg, cmd.AND_TEXT_BODY):
    if user.is_manager(msg, guild):
      guild.update_sch(msg, cmd)
      await reply.db_query(msg, guild)
    else:
      await reply.sorry_quote(msg)
  
  # remover algum registro do BD do servidor
  elif cmd.match('legen!del', msg, cmd.AND_TEXT_BODY):
    if user.is_manager(msg, guild):
      guild.remove_record(msg, cmd)
      await reply.op_status(msg, guild)
    else:
      await reply.sorry_quote(msg)


  # ----------------------------------------------------------------------------------------------
  # rolar dados

  elif cmd.match(dice.nameRegex, msg, cmd.AND_TEXT_BODY):
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
  
  elif cmd.match('legen!roll', msg, cmd.ONLY):
    if user.is_manager(msg, guild):
      dice.roll_test()
      await reply.roll_result(msg, dice)
    else:
      await reply.sorry_quote(msg)


  # ----------------------------------------------------------------------------------------------

keep_alive()
bot.run(os.getenv('TOKEN'))

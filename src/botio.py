import re
import random
from dconsts import DefaultConstants as const
from helpguide import UserGuide as helpmsg

# analisador de comandos
class CommandAnalyzer:
  ONLY = 0
  AND_TEXT_BODY = 1
  AND_DESCRIPTION = 2
  AND_MENTIONS = 3
  UNSCOPED = 4
  
  # editar: substituir o uso desses regex pelos da classe DefaultRegexes
  whiteSpaceRegex = r'\s+'
  endofWordRegex = r'\s*$'
  endofLineRegex = r'(\s+.*\n?)?$'
  endofTextRegex = r'(\s+(.*\n*)*)?$'
  
  def match (self, cmdRegex, msg, scope=UNSCOPED):
    if scope == self.UNSCOPED:
      msgContent = msg.content.lower()
    
    elif scope == self.ONLY:
      msgContent = msg.content.lower()
      cmdRegex += self.endofWordRegex
    
    elif scope == self.AND_TEXT_BODY:
      msgContent = msg.content.lower()
      cmdRegex += self.endofTextRegex

    else:
      try:
        descStart = msg.content.index(' ')
        msgContent = msg.content[descStart:].lower()
        
        if scope == self.AND_DESCRIPTION:
          cmdRegex = self.whiteSpaceRegex + cmdRegex + self.endofWordRegex
        
        elif scope == self.AND_MENTIONS:
          mentionRegex = r'(' + cmdRegex + r')'
          newMentionRegex = r'(\s*[\s\,]\s*' + mentionRegex + r')*'
          cmdRegex = self.whiteSpaceRegex + mentionRegex + newMentionRegex + self.endofWordRegex

        else:
          return None
      except:
        return None
    return re.match(cmdRegex, msgContent)


# respostas automaticas do bot
class AutoResponder:
  def __init__ (self):
    self.whoami_quote = 'Think of me as Yoda, only instead of being little and green, I\'m a bot and I\'m awesome. I\'m your bro: I\'m Broda!'
    self.please_quote = 'ha, ha! Please.'
    self.challenge_quote = 'challenge accepted!'
    self.sometimes_quote = 'sometimes we search for one thing but discover another.'
    self.sorry_quote = 'I\'m sorry, I can\'t hear you over the sound of how awesome I am.'
    self.legendary_quote = [
      'believe it or not, you was not always as awesome as you are today.',
      'you poor thing. Having to grow up in the Insula, with the Palace right there.',
      'to succeed you have to stop to be ordinary and be legen — wait for it — dary! Legendary!',
      'when you get sad, just stop being sad and be awesome instead.',
      'if you have a crazy story, I was there. It\'s just a law of the universe.',
      'I believe you and I met for a reason. It\'s like the universe was saying, \"Hey Legendary, there\'s this dude, he\'s pretty cool, but it is your job to make him awesome\".',
      'without me, it’s just aweso.'
    ]
  
  # ----------------------------------------------------------------------------------------------
  # respostas padrao

  def whoami (self, msg):
    return msg.channel.send(self.whoami_quote)

  def legendary (self, msg):
    quote = random.randint(0, len(self.legendary_quote))
    answer = '<@'+str(msg.author.id)+'>, ' + self.legendary_quote[quote]
    return msg.channel.send(answer)
  
  def help (self, msg, cmd, bot, embedBox):
    if cmd.match('legen!help', msg, cmd.ONLY):
      embedBox = helpmsg.general_group(bot, embedBox)
    
    elif cmd.match(r'(information|info)', msg, cmd.AND_DESCRIPTION):
      embedBox = helpmsg.info_group(embedBox)
    elif cmd.match(r'(moderation|mod)', msg, cmd.AND_DESCRIPTION):
      embedBox = helpmsg.mod_group(embedBox)
    elif cmd.match(r'(gambling|game)', msg, cmd.AND_DESCRIPTION):
      embedBox = helpmsg.game_group(embedBox)
    
    else:
      answer = '<@'+str(msg.author.id)+'>, '+ self.please_quote
      return msg.channel.send(answer)
    
    return msg.channel.send(embed=embedBox)

  def challenge (self, msg):
    answer = '<@'+str(msg.author.id)+'>, ' + self.challenge_quote
    return msg.channel.send(answer)
  
  def sometimes (self, msg):
    answer = '<@'+str(msg.author.id)+'>, ' + self.sometimes_quote
    return msg.channel.send(answer)

  def sorry (self, msg):
    answer = '<@'+str(msg.author.id)+'>, ' + self.sorry_quote
    return msg.channel.send(answer)


  # ----------------------------------------------------------------------------------------------
  # respostas a operacoes com banco de dados

  def db_sch_query (self, msg, guild):
    arrowSign = ' \u27F5 '
    if guild.queryResult:
      answer = '<#'+guild.queryResult+'>' + arrowSign + 'The Secret Channel'
    else:
      answer = '<@'+str(msg.author.id)+'>, ' + self.sometimes_quote
    return msg.channel.send(answer)
  
  def db_mgmt_query (self, msg, guild):
    arrowSign = ' \u27F5 '
    if guild.queryResult:
      answer = ' '.join(guild.queryResult) + arrowSign + 'The Management'
    else:
      answer = '<@'+str(msg.author.id)+'>, ' + self.sometimes_quote
    return msg.channel.send(answer)
  
  def op_status (self, msg, guild):
    if guild.op_was_successful:
      answer = '<@'+str(msg.author.id)+'>, ' + self.challenge_quote
    else:
      answer = '<@'+str(msg.author.id)+'>, ' + self.sometimes_quote
    return msg.channel.send(answer)


  # ----------------------------------------------------------------------------------------------
  # respostas a rolagem de dados

  def action_result (self, msg, actionResult, guild=None, bot=None):
    actionBehavior = actionResult['behavior']

    if (actionBehavior != const.PUBLIC_ACTION) and (guild and bot):
      guild.get_gid_gdb_sch(msg, bot)
      target_channel = guild.sch
    else:
      target_channel = msg.channel

    answer = actionResult['value'] + '<@'+str(msg.author.id)+'>,\n'
    if actionResult['quote']:
      answer += '\"'+ actionResult['quote'] +'\",\n'
    answer += actionResult['description']
    return target_channel.send(answer)

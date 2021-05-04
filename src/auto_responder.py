import random
import re

# analisador de comandos
class CommandAnalyzer:
  def __init__ (self):
    self.ONLY = 0
    self.AND_TEXT_BODY = 1
    self.AND_DESCRIPTION = 2
    
    self.whiteSpaceRegex = r'\s+'
    self.endofWordRegex = r'\s*$'
    self.endofLineRegex = r'(\s+.*\n?)?$'
    self.endofTextRegex = r'(\s+(.*\n*)*)?$'
  
  def match (self, cmdRegex, msg, scope):
    if scope == self.ONLY:
      msgContent = msg.content.lower()
      cmdRegex += self.endofWordRegex
    
    elif scope == self.AND_TEXT_BODY:
      msgContent = msg.content.lower()
      cmdRegex += self.endofTextRegex
    
    elif scope == self.AND_DESCRIPTION:
      try:
        descStart = msg.content.index(' ')
        msgContent = msg.content[descStart:].lower()
        cmdRegex = self.whiteSpaceRegex + cmdRegex + self.endofLineRegex
      except:
        return None
    
    return re.match(cmdRegex, msgContent)

# respostas automaticas do bot
class AutoResponder:
  def __init__ (self):
    self.whoami = 'Think of me as Yoda, only instead of being little and green, I\'m a bot and I\'m awesome. I\'m your bro: I\'m Broda!'
    self.please = 'ha, ha! Please.'
    self.challenge = 'challenge accepted!'
    self.sometimes = 'Sometimes we search for one thing but discover another.'
    self.sorry = 'I\'m sorry, I can\'t hear you over the sound of how awesome I am.'
    self.legendary = [
      'believe it or not, you was not always as awesome as you are today.',
      'you poor thing. Having to grow up in the Insula, with the Palace right there.',
      'to succeed you have to stop to be ordinary and be legen — wait for it — dary! Legendary!',
      'when you get sad, just stop being sad and be awesome instead.',
      'if you have a crazy story, I was there. It\'s just a law of the universe.',
      'I believe you and I met for a reason. It\'s like the universe was saying, \"Hey Legendary, there\'s this dude, he\'s pretty cool, but it is your job to make him awesome\".',
      'without me, it’s just aweso.'
    ]
  
  def whoami_quote (self, msg):
    return msg.channel.send(self.whoami)

  def legendary_quote (self, msg):
    option = random.randint(0, len(self.legendary))
    answer = '<@'+str(msg.author.id)+'>, ' + self.legendary[option]
    return msg.channel.send(answer)
  
  def please_quote (self, msg, cmd, bot):
    arrowSign = ' \u27F5 '
    textBox = '\u0060'
    
    answer = '<@'+str(msg.author.id)+'>, ' + self.please
    
    if cmd.match('please', msg, cmd.AND_DESCRIPTION):
      answer = '**Legendary\'s commands**\n'
      answer += '<@'+str(bot.user.id)+'>' + arrowSign + 'Tells you who I am.\n'
      answer += textBox + 'legen!dary' + textBox + arrowSign + 'Provides useful information.\n'
      answer += textBox + 'legen!sch {#channel}' + textBox + arrowSign + 'Assigns or queries the Secret Channel.\n'
      answer += textBox + 'legen!del {option}' + textBox + arrowSign + 'Removes a record from the guild database.\n'
      answer += textBox + '[amount]{behavior}d[type]{modifier}{method}' + textBox + arrowSign + 'Rolls the dice.'
    
    # elif cmd.match('option', msg, cmd.AND_DESCRIPTION):
    
    return msg.channel.send(answer)

  def challenge_quote (self, msg):
    answer = '<@'+str(msg.author.id)+'>, ' + self.challenge
    return msg.channel.send(answer)
  
  def sometimes_quote (self, msg):
    answer = '<@'+str(msg.author.id)+'>, ' + self.sometimes
    return msg.channel.send(answer)

  def sorry_quote (self, msg):
    answer = '<@'+str(msg.author.id)+'>, ' + self.sorry
    return msg.channel.send(answer)

  def db_query (self, msg, guild):
    arrowSign = ' \u27F5 '
    if guild.queryResult:
      answer = '<#'+guild.queryResult+'>' + arrowSign + 'The Secret Channel'
    else:
      answer = '<@'+str(msg.author.id)+'>, ' + self.sometimes
    return msg.channel.send(answer)
  
  def op_status (self, msg, guild):
    if guild.op_was_successful:
      answer = '<@'+str(msg.author.id)+'>, ' + self.challenge
    else:
      answer = '<@'+str(msg.author.id)+'>, ' + self.sometimes
    return msg.channel.send(answer)

  def roll_result (self, msg, dice, guild=None, bot=None):
    if (dice.isSecret or dice.isHidden) and (guild and bot):
      guild.get_gid_gdb_sch(msg, bot)
      target_channel =  guild.sch
      rollQuote = ''
    
    else:
      target_channel = msg.channel
      rollQuote = self.challenge

    if dice.playerQuote:
      rollQuote = '\"' + dice.playerQuote + '\",'

    answer = '<@'+str(msg.author.id)+'>, ' + rollQuote + '\n' + dice.rollResults
    return target_channel.send(answer)

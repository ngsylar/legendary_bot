import random
import re

# analisador de comandos
class CommandAnalyzer:
  def __init__ (self):
    self.ONLY = 0
    self.AND_TEXT_BODY = 1
    self.AND_DESCRIPTION = 2
    self.AND_MENTIONS = 3
    
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
    answer = '<@'+str(msg.author.id)+'>, ' + self.please_quote
    
    if cmd.match('please', msg, cmd.AND_DESCRIPTION):
      textPack = '\u0060\u0060\u0060'
      textBox = '\u0060'
      arrowSign = ' \u27F5 '

      self.embedBox_text = ''.join([
        'The great list of all the legendary commandments.\n\n',
        
        ':book: **Information**\n',
        '<@'+str(bot.user.id)+'>' + arrowSign + 'Tells you who I am.\n',
        textBox + 'legen!dary' + textBox + arrowSign + 'Provides useful information.\n',
        textBox + 'legen!help <please>' + textBox + arrowSign + 'Provides user manual.\n\n'
        
        ':crossed_swords: **Moderation** (role permission required)\n',
        textBox + 'legen!sch <C>' + textBox + arrowSign + 'Queries or assigns the Secret Channel.\n',
        textBox + 'legen!del <D>' + textBox + arrowSign + 'Removes a record from the guild database.\n\n',

        '**Moderation _C_ options**\n',
        textBox + ' ' + textBox + arrowSign + 'Blank to reveal the Secret Channel.\n',
        textBox + '#<channel_name>' + textBox + arrowSign + 'To update the Secret Channel.\n\n',
        
        '**Moderation _D_ options**\n',
        textBox + 'sch' + textBox + arrowSign + 'Selects the Secret Channel.\n',
        textBox + 'mgmt' + textBox + arrowSign + 'Selects all management roles.\n\n'

        ':game_die: **Gambling**\n',
        textBox + '<amount><behavior>d<range><sum> <message>' + textBox + arrowSign + 'Rolls the dice. _Message_ is optional.\n\n'

        '**Mandatory dice parameters**\n',
        textBox + '<amount>' + textBox + arrowSign + 'Consists of an integer number from 1 to 100 of dice to be rolled.\n',
        textBox + '<range>' + textBox + arrowSign + 'Consists of an integer number from 2 to 1000 faces of the dice to roll.\n\n',

        '**Rolling dice _behavior_**\n',
        textBox + ' ' + textBox + arrowSign + 'Blank to just roll the dice.\n',
        textBox + 's' + textBox + arrowSign + 'To roll a secret dice whose result will be shown in the Secret Channel.\n',
        textBox + 'h' + textBox + arrowSign + 'To roll a hidden dice whose roll command will be omitted and whose result will be shown in the Secret Channel (bot must have permission to manage the channel messages).\n\n'
        
        '**Dice _sum_**\n',
        textBox + '<modifier><method>' + textBox + arrowSign + 'The _modifier_ consists of an optional arithmetic expression to be added to the dice result. If the modifier exists, the sum _method_ can be left blank to add the modifier value to the final sum of the dice, or it can be filled in with \'e\' to add the modifier value to the result of each dice rolled. See examples of correct entries:\n',
        textPack + '2d8 to be proud of\n1d20+5\n4d20+5e\n2sd8+7e\n2hd20-1e' + textPack
      ])

      self.thumbnail_url = 'https://media.istockphoto.com/vectors/isometric-businessman-try-to-standing-on-rolling-dice-vector-id1025271320?k=6&m=1025271320&s=612x612&w=0&h=0-7C9XoTcB5JWSJFIsfUXIMtmPqJkDsZaL_5LLSu9VA='

      embedBox.set_author(name='The Bro Code', icon_url=bot.user.avatar_url)
      embedBox.set_thumbnail(url=self.thumbnail_url)
      embedBox.description=self.embedBox_text
      embedBox.color=0x5865f2
      
      return msg.channel.send(embed=embedBox)
    return msg.channel.send(answer)

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

  def roll_result (self, msg, dice, guild=None, bot=None):
    if (dice.isSecret or dice.isHidden) and (guild and bot):
      guild.get_gid_gdb_sch(msg, bot)
      target_channel = guild.sch
      rollQuote = ''
    
    else:
      target_channel = msg.channel
      rollQuote = self.challenge_quote

    if dice.playerQuote:
      rollQuote = '\"' + dice.playerQuote + '\",'

    answer = '<@'+str(msg.author.id)+'>, ' + rollQuote + '\n' + dice.rollResults
    return target_channel.send(answer)

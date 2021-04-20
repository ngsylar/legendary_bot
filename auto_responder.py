import random

# banco de dados do servidor
class AutoResponder:
  def __init__ (self):
    self.whoami = 'Think of me as Yoda, only instead of being little and green, I\'m a bot and I\'m awesome. I\'m your bro: I\'m Broda!'
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
    option = random.randint(0, 7)
    answer = '<@'+str(msg.author.id)+'>, ' + self.legendary[option]
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

  def roll_result (self, msg, dice, guild_sch=None):
    if dice.isSecret and guild_sch:
      rollQuote = ''
      target_channel =  guild_sch
    else:
      rollQuote = self.challenge
      target_channel = msg.channel

    if dice.playerQuote:
      rollQuote = '\"' + dice.playerQuote + '\",'

    answer = '<@'+str(msg.author.id)+'>, ' + rollQuote + '\n' + dice.rollResults
    return target_channel.send(answer)

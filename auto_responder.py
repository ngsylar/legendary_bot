import random

# banco de dados do servidor
class AutoResponder:
  def __init__ (self):
    self.whoami = 'Think of me as Yoda, only instead of being little and green, I\'m a bot and I\'m awesome. I\'m your bro: I\'m Broda!'
    self.challenge = 'Challenge accepted!'
    self.sorry = 'I\'m sorry, I can\'t hear you over the sound of how awesome I am.'
    self.sometimes = 'Sometimes we search for one thing but discover another.'
    self.awesome = 'challenge accepted!'
    self.legendary = [
      'believe it or not, you was not always as awesome as you are today.',
      'you poor thing. Having to grow up in the Insula, with the Palace right there.',
      'to succeed you have to stop to be ordinary and be legen — wait for it — dary! Legendary!',
      'when you get sad, just stop being sad and be awesome instead.',
      'if you have a crazy story, I was there. It\'s just a law of the universe.',
      'I believe you and I met for a reason. It\'s like the universe was saying, \"Hey Legendary, there\'s this dude, he\'s pretty cool, but it is your job to make him awesome\".',
      'without me, it’s just aweso.'
    ]
  
  def legendary_quote (self, msg):
    option = random.randint(0, 7)
    answer = '<@'+str(msg.author.id)+'>, ' + self.legendary[option]
    return answer

  def challenge_quote (self, msg):
    answer = '<@'+str(msg.author.id)+'>, ' + self.awesome
    return answer
  
  def sometimes_quote (self, msg):
    answer = '<@'+str(msg.author.id)+'>, ' + self.sometimes
    return answer

  def sorry_quote (self, msg):
    answer = '<@'+str(msg.author.id)+'>, ' + self.sorry
    return answer

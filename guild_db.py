from replit import db

# banco de dados do servidor

class GuildDB:
  def __init__(self):
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

  def update_sch(self, server_id, msg):
    schRaw = msg.split('legen!ch', 1)
    msgHasChannel = (len(schRaw) > 1) and schRaw[1].startswith(' <#') and (len(schRaw[1]) > 1)

    if msgHasChannel:
      secretChannel = schRaw[1].split('#', 1)[1][:-1]
      db[server_id] = secretChannel
      self.operationStatus = self.challenge
    else:
      self.operationStatus = self.sorry

  def delete_sch(self, server_id):
    if server_id in db.keys():
      del db[server_id]
      self.operationStatus = self.challenge
    else:
      self.operationStatus = self.sorry

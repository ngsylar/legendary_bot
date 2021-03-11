from replit import db

# banco de dados do servidor

class Gdb:
  def update_sch(server_id, schn):
    db[server_id] = schn

  def delete_sch(server_id):
    if server_id in db.keys():
      del db[server_id]

  whoami = [
    'Think of me as Yoda, only instead of being little and green, I wear suits and I\'m awesome. I\'m your bro: I\'m Broda!',
    'That is awesome!',
    'Challenge accepted!',
    'Sometimes we search for one thing but discover another.'
  ]
  awesome = ['that is awesome!', 'challenge accepted!']
  legendary = [
    'believe it or not, I was not always as awesome as I am today.',
    'you poor thing. Having to grow up in the Insula, with the Palace right there.',
    'sometimes we search for one thing but discover another.',
    'to succeed you have to stop to be ordinary and be legen — wait for it — dary! Legendary!',
    'when I get sad, I stop being sad and be awesome instead.',
    'if you have a crazy story, I was there. It\'s just a law of the universe.',
    'I believe you and I met for a reason. It\'s like the universe was saying, \"Hey Legendary, there\'s this dude, he\'s pretty cool, but it is your job to make him awesome\".',
    'without me, it’s just aweso.'
  ]
  sorry = 'I\'m sorry, I can\'t hear you over the sound of how awesome I am.'
import re
from replit import db
from auto_responder import AutoResponder

# banco de dados do servidor
class GuildDB:
  def get_gid_gdb_sch (self, msg, bot=None):
    self.gid = str(msg.guild.id)
    self.sch = None

    if self.gid not in db.keys():
      db[self.gid] = {}
    self.gdb = db[self.gid]

    if bot and ('sch' in self.gdb):
      self.sch = bot.get_channel(int(self.gdb['sch']))

  def update_sch (self, msg):
    self.get_gid_gdb_sch(msg)

    msg_contains_channel = re.match(r'\s+<#[0-9]{18}>\s*$', msg.content[9:])
    arrowSign = ' \u27F5 '
    
    if msg_contains_channel:
      secret_channel_id = msg.content.split('<#',1)[1].split('>',1)[0]      
      self.gdb['sch'] = secret_channel_id
      db[self.gid] = self.gdb
    
    if 'sch' in self.gdb:
      self.queryResult = '<#'+self.gdb['sch']+'>' + arrowSign + 'The Secret Channel'
    else:
      self.queryResult = AutoResponder().sometimes_quote(msg)

  def remove_record (self, msg):
    self.successful_op = AutoResponder().sometimes_quote(msg)
    
    self.get_gid_gdb_sch(msg)
    msg_contains_sch = re.match(r'\s+sch\s*$', msg.content[9:])

    if msg_contains_sch:
      if 'sch' in self.gdb:
        del self.gdb['sch']
        db[self.gid] = self.gdb
        self.successful_op = AutoResponder().challenge_quote(msg)

from replit import db
import re

# banco de dados do servidor
class GuildDB:
  def get_gid_gdb_sch (self, msg, bot=None):
    self.gid = str(msg.guild.id)
    self.sch = None

    if self.gid not in db.keys():
      db[self.gid] = {}
    self.gdb = db[self.gid]

    if 'mgmt' not in self.gdb:
      self.gdb['mgmt'] = []
      db[self.gid] = self.gdb

    if bot and ('sch' in self.gdb):
      self.sch = bot.get_channel(int(self.gdb['sch']))

  # editar: ver um jeito de passar o regex de mencao para a classe de cmd
  def update_sch (self, msg, cmd):
    self.get_gid_gdb_sch(msg)
    msg_contains_channel = cmd.match(r'<#[0-9]{18}>', msg, cmd.AND_DESCRIPTION)

    if msg_contains_channel:
      secret_channel_id = msg.content.split('<#',1)[1].split('>',1)[0]      
      self.gdb['sch'] = secret_channel_id
      db[self.gid] = self.gdb
    
    if 'sch' in self.gdb:
      self.queryResult = self.gdb['sch']
    else:
      self.queryResult = None
  
  # editar: ver um jeito de passar o regex de mencao para a classe de cmd
  def update_mgmt_roles (self, msg, cmd):
    self.get_gid_gdb_sch(msg)
    msg_contains_channel = cmd.match(r'(<@&[0-9]{18}>|@everyone)', msg, cmd.AND_MENTIONS)

    if msg_contains_channel:
      mgmtRolesRaw = re.split(r'[\s\,]', msg_contains_channel.group())
      self.gdb['mgmt'].extend(list(filter(None,dict.fromkeys(mgmtRolesRaw))))
      db[self.gid] = self.gdb
    
    self.queryResult = self.gdb['mgmt']

  # editar: adicionar a possibilidade de excluir apenas um cargo da lista de gerentes
  def remove_record (self, msg, cmd):
    self.op_was_successful = False
    
    self.get_gid_gdb_sch(msg)
    msg_contains_sch = cmd.match('sch', msg, cmd.AND_DESCRIPTION)

    if msg_contains_sch:
      if 'sch' in self.gdb:
        del self.gdb['sch']
        db[self.gid] = self.gdb
        self.op_was_successful = True
      return
    
    msg_contains_mgmt = cmd.match('mgmt', msg, cmd.AND_DESCRIPTION)
    
    if msg_contains_mgmt:
      if 'mgmt' in self.gdb:
        del self.gdb['mgmt']
        db[self.gid] = self.gdb
        self.op_was_successful = True
  
  def remove_from_db (self, guild_server):
    guild_id = str(guild_server.id)
    if guild_id in db.keys():
      del db[guild_id]

# propriedades de um membro do servidor
# editar: fazer disso uma subclasse
class GuildMember:
  def is_manager (self, msg, guild):
    if msg.author.guild_permissions.administrator:
      return True
    
    else:
      guild.get_gid_gdb_sch(msg)

      for role in msg.author.roles:
        if role.name == '@everyone':
          refRole = role.name
        else:
          refRole = role.mention
        
        if refRole in guild.gdb['mgmt']:
          return True
    
    return False

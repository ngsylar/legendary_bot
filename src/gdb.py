from replit import db
import re

# banco de dados do servidor
class GuildDB:
  # execucao necessaria antes de cada atualizacao do gdb
  def get_gid_gdb_sch (self, msg, bot=None):
    self.gid = str(msg.guild.id)
    self.sch = None

    if self.gid not in db.keys():
      self.__create_db()
    self.__read_db()

    if 'mgmt' not in self.gdb:
      self.gdb['mgmt'] = []
      self.__update_db()

    if bot and ('sch' in self.gdb):
      self.sch = bot.get_channel(int(self.gdb['sch']))

  # editar: ver um jeito de passar o regex de mencao para (?)
  # define o canal secreto do servidor (para lancamento de dados ocultos ou secretos)
  def update_sch (self, msg, cmd):
    self.get_gid_gdb_sch(msg)
    msg_contains_channel = cmd.match(r'<#[0-9]{18}>', msg, cmd.AND_DESCRIPTION)

    if msg_contains_channel:
      secret_channel_id = msg.content.split('<#',1)[1].split('>',1)[0]      
      self.gdb['sch'] = secret_channel_id
      self.__update_db()
    
    if 'sch' in self.gdb:
      self.queryResult = self.gdb['sch']
    else:
      self.queryResult = None
  
  # editar: ver um jeito de passar o regex de mencao para (?)
  # adiciona um cargo ao gerenciamento de canal secreto do servidor
  def update_mgmt_roles (self, msg, cmd):
    self.get_gid_gdb_sch(msg)
    msg_contains_roles = cmd.match(r'(<@&[0-9]{18}>|@everyone)', msg, cmd.AND_MENTIONS)

    if msg_contains_roles:
      mgmtRolesRaw = re.split(r'[\s\,]', msg_contains_roles.group())
      self.gdb['mgmt'].extend(list(filter(None,dict.fromkeys(mgmtRolesRaw))))
      self.__update_db()
    
    self.queryResult = self.gdb['mgmt']

  # editar: adicionar a possibilidade de excluir apenas um cargo da lista de gerentes
  # editar: apagar cargos do servidor ainda não os apaga automaticamente da gerência
  # remove um registro do gdb
  def remove_record (self, msg, cmd):
    self.get_gid_gdb_sch(msg)
    self.op_was_successful = False

    msg_contains_sch = cmd.match('sch', msg, cmd.AND_DESCRIPTION)
    if msg_contains_sch:
      if 'sch' in self.gdb:
        del self.gdb['sch']
        self.__update_db()
        self.op_was_successful = True
      return
    
    msg_contains_mgmt = cmd.match('mgmt', msg, cmd.AND_DESCRIPTION)
    if msg_contains_mgmt:
      if 'mgmt' in self.gdb:
        del self.gdb['mgmt']
        self.__update_db()
        self.op_was_successful = True
  
  # crud do db
  def __create_db (self):
    db[self.gid] = {}
  def __read_db (self):
    self.gdb = db[self.gid]
  def __update_db (self):
    db[self.gid] = self.gdb
  
  # remove registros de gdb do db quando o servidor eh excluido
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
        if role.name.lower() == 'mastermind':
          return True
        
        elif role.name == '@everyone':
          refRole = role.name
        else:
          refRole = role.mention
        
        if refRole in guild.gdb['mgmt']:
          return True
    
    return False

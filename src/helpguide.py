from dconsts import TextStructures as txtop

class UserGuide:
  def general_group (bot, embedBox):
    embedBox_text = [
      'To view the commands in each group use:',
      txtop.BBOX + 'ini\nlegen!help [group]' + txtop.BBOX]
    thumbnail_url = 'https://i.ibb.co/sw0vcFj/ddthumb2.png'
    
    embedBox.set_author(name='The Legendary Code', icon_url=bot.user.avatar_url)
    embedBox.description=''.join(embedBox_text)
    embedBox.set_thumbnail(url=thumbnail_url)
    embedBox.color=0x5865f2

    embedBox.add_field(name=':book: Information', value='3 commands', inline=True)
    embedBox.add_field(name=':crossed_swords: Moderation', value='3 commands', inline=True)
    embedBox.add_field(name=':game_die: Gambling', value='1 command', inline=True)

    return embedBox

  def info_group (embedBox):
    embedBox_text = [
      ':book: **Information**\n',

      '\nTo get to know me better, use:',
      txtop.BBOX + 'fix\n@Legendary' + txtop.BBOX,

      '\nTo receive useful information about yourself, use:',
      txtop.BBOX + 'ini\nlegen!dary' + txtop.BBOX,
      
      '\nTo view the help menu, use:',
      txtop.BBOX + 'ini\nlegen!help' + txtop.BBOX]
    
    embedBox.description=''.join(embedBox_text)
    embedBox.color=0x5865f2
    return embedBox

  def mod_group (embedBox):
    embedBox_text = [
      ':crossed_swords: **Moderation**\n',
      '_For these commands permission is required._\n'

      '\nTo manage the Secret Channel as a legendary manager, use:',
      txtop.BBOX + 'ini\nlegen!sch [options below]' + txtop.BBOX,
      txtop.BBOX + 'asciidoc\n',
      '            :: empty for query\n',
      '#[channel]  :: channel name for assignment' + txtop.BBOX,

      '\nTo manage the Management Roles as an administrator, use:',
      txtop.BBOX + 'ini\nlegen!mgmt [options below]' + txtop.BBOX,
      txtop.BBOX + 'asciidoc\n',
      '            :: empty for query (any role called \"Mastermind\" is manager by default)\n',
      '@[role] @[] :: adds one or several roles simultaneously' + txtop.BBOX,

      '\nTo remove a record from the Guild Database, use:',
      txtop.BBOX + 'ini\nlegen!del [options below]' + txtop.BBOX,
      txtop.BBOX + 'asciidoc\n',
      'sch         :: removes the Secret Channel as a legendary manager\n',
      'mgmt        :: removes all the management roles as an administrator' + txtop.BBOX]
    
    embedBox.description=''.join(embedBox_text)
    embedBox.color=0x5865f2
    return embedBox
  
  def game_group (embedBox):
    embedBox_text = [
      ':game_die: **Gambling**\n',
      '_To perform a game action, roll the dice._\n'

      '\nBasic structure of a game die - where \'r\' is the range on the die and \'a\' is the amount of rolls for this die:',
      txtop.BBOX + 'ini\n[a]d[r]' + txtop.BBOX,
      txtop.BBOX + 'asciidoc\n',
      '2d20        :: for example will roll a twenty-sided die twice' + txtop.BBOX,

      '\nYou can add modifiers to the result of each die - where \'op\' is a mathematical operator whose priority is always the order in which they appear and \'v\' is the value to modify the die results:',
      txtop.BBOX + 'ini\n[op][v]e' + txtop.BBOX,
      txtop.BBOX + 'asciidoc\n',
      '+2e         :: for example will add 2 to the value of each result of a die' + txtop.BBOX,

      '\nYou can even input multiple game dice into a single arithmetic expression. Take for example this valid input:',
      txtop.BBOX + 'arm\n2d4+2-(2d10+2e)' + txtop.BBOX,
      
      '\nIf you want to take a hidden action or want its results to be secret, use a flag at the beginning of the input, as shown below:',
      txtop.BBOX + 'ini\n[f][expression] [optional message]' + txtop.BBOX,
      txtop.BBOX + 'asciidoc\n',
      '            :: empty to reveal the action results\n',
      's           :: to hide the action results\n',
      'h           :: to perform a hidden action' + txtop.BBOX,
      txtop.BBOX + 's1d20+2 for example hides the action results and this is an optional message' + txtop.BBOX]
    
    embedBox.description=''.join(embedBox_text)
    embedBox.color=0x5865f2
    return embedBox

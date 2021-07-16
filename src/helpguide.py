from dconsts import TextStructures as txtop
from auxiliaries import maxcode

# editar: substituir todos os txtop.BBOX por maxcode()
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

      '\nBasic structure of a game die - where [r] is the range on the die and [a] is the amount of this die to be rolled:',
      maxcode('css', '[a]d[r]'),
      maxcode('', '2d20 for example will roll two twenty-sided die'),

      '\nYou can select which results will be in the final sum - where [st] can be replaced with one of the options below and [sa] can be left blank (1 by default) or replaced with an integer value; braces are optional:',
      maxcode('css', '[a]d[r]{[st][sa]}'),
      maxcode('asciidoc',
      'h     :: to get the highest [sa] results\n'+
      'l     :: to get the lowest [sa] results\n'+
      'n[st] :: before one of the above causes logical negation'),

      '\nYou can add modifiers to each result of a die immediately after it - where [op] is a mathematical operator whose priority is always the order in which they appear and [v] is the value to modify the die results:',
      maxcode('css', '[op][v]e'),
      maxcode('', '2d20+2e for example will add 2 to the value of each result of this die'),

      '\nYou can repeat the roll of the same die multiple times and the results will be shown individually for each repetition. See the notation below - where [m] is the number of repetitions of the rolls:',
      maxcode('css', '[m]#[dice][modifiers]'),
      maxcode('', '6#4d6-2e for example will roll four six-sided dice six times and apply the -2 modifier to every result of this die'),

      '\nYou can even input several game dice into a single arithmetic expression - that\'s the definition of game action. Take for example this valid input:',
      maxcode('arm', '2#2d10+2e-(3d4{nl}+2e+2) for the glory'),

      '\nTo use an action as a calculator only (no dice roll):',
      maxcode('css', '&[expression]'),
      maxcode('', '&1+1 did this really need an example?'),
      
      '\nIf you want to take a hidden action or want its results to be secret, use a flag - indicated by [f] - at the beginning of the input, as shown below:',
      maxcode('css', '[f][expression] [optional message]'),
      maxcode('asciidoc',
      '      :: empty to reveal the action results\n'+
      's     :: to hide the action results\n'+
      'h     :: to perform a hidden action'),
      maxcode('', 's1d20+2 for example hides the action results and this is an optional message')]
    
    print(len(''.join(embedBox_text)))
    embedBox.description=''.join(embedBox_text)
    embedBox.color=0x5865f2
    return embedBox

import re
from dconsts import DefaultRegexes as regex
from arith.operation import Operation
from arith.dice import Dice

class Expression:
  def __init__ (self, raw, address=None, is_pattern=False):
    if is_pattern:
      self.raw = '('+raw.lower().replace(',', '.')+')'
    else:
      self.raw = raw
    if address:
      self.address = address
    
  def has_inner_expression (self):
    if re.search(regex.VALIDATE_EXP, self.raw):
      self.__inner_expression_match = re.search(regex.ARITH_EXPRESSION, self.raw)
      return self.__inner_expression_match
    
  @property
  def inner_expression (self):
    if self.__inner_expression_match:
      return Expression(
        raw = self.__inner_expression_match[1],
        address = self.__inner_expression_match)
    
  # editar: transformar a gambiarra do retorno em algo que faca sentido
  def has_operation (self):
    self.current_operation = Operation(
      overall_exp = self.raw)
    return True

  def has_dice (self):
    self.inner_dice_match = re.search(regex.MULTIPLE_DICE, self.raw)
    return self.inner_dice_match
    
  @property
  def inner_dice (self):
    if self.inner_dice_match:
      dice_address = {
        'start': self.inner_dice_match.start(),
        'end': self.inner_dice_match.end()}
      
      dice_mods_match = re.match(regex.MODIFIERS_RAW, self.raw[dice_address['end']:])
      if dice_mods_match:
        dice_mods_raw = dice_mods_match[0].replace('+-','-')
        findall_dice_mods = re.findall(regex.MODIFIER, dice_mods_raw)
        dice_mods = [mod_i for (mod_i,_,_) in findall_dice_mods]
        dice_address['end'] += dice_mods_match.end()
      else:
        dice_mods = []

      return Dice(
        match = self.inner_dice_match,
        address = dice_address,
        modifiers = dice_mods)

  def replace (self, address, replacement):
    if type(address) == re.Match:
      self.raw = self.raw[:address.start()] + str(replacement) + self.raw[address.end():]
    elif type(address) == dict:
      self.raw = self.raw[:address['start']] + str(replacement) + self.raw[address['end']:]
    return self.raw
  
  @property
  def result (self):
    return float(self.raw)

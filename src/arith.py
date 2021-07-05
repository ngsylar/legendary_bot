import re
import random
from dconsts import DefaultRegexes as regex

class Operation:
  def __init__ (self, overall_exp):
    self.overall_exp = overall_exp

  def is_mul (self):
    self.match = re.search(regex.ARITH_MUL, self.overall_exp)
    self.__set_operation_factors()
    return self.match
    
  def is_div (self):
    self.match = re.search(regex.ARITH_DIV, self.overall_exp)
    self.__set_operation_factors()
    return self.match
    
  def is_add (self):
    self.match = re.search(regex.ARITH_ADD, self.overall_exp)
    self.__set_operation_factors()
    return self.match
    
  def is_sub (self):
    self.match = re.search(regex.ARITH_SUB, self.overall_exp)
    self.__set_operation_factors()
    return self.match

  def __set_operation_factors (self):
    if self.match:
      self.factors = {
        'left': float(self.match[1]),
        'right': float(self.match[2])}


class Modifier:
  def __init__ (self, raw):
    self.raw = raw
    self.match = None

  def operator_is_mul (self):
    self.match = re.match(regex.MODIFIER_MUL, self.raw)
    return self.match

  def operator_is_div (self):
    self.match = re.match(regex.MODIFIER_DIV, self.raw)
    return self.match
    
  def operator_is_add (self):
    self.match = re.match(regex.MODIFIER_ADD, self.raw)
    return self.match
    
  def operator_is_sub (self):
    self.match = re.match(regex.MODIFIER_SUB, self.raw)
    return self.match

  @property
  def value (self):
    if self.match:
      value = float(self.match[1])
    return value


class Dice:
  # editar: edicao de baixa prioridade, depois ver um jeito de separar modificadores dessa classe
  def __init__ (self, match, address, modifiers):
    self.repetition = match[1]
    self.name = match[2]
    self.address = address
    
    self.amount = int(match[3])
    self.faces = int(match[4])
    self.results = []
    self.__validate()

    self.modifiers = modifiers
    self.__mods_rawlist = modifiers.copy()

  def __validate (self):
    invalid_amount = (self.amount < 1) or (self.amount > 100)
    invalid_faces = (self.faces < 2) or (self.faces > 1000)
    if invalid_amount or invalid_faces:
      raise
    
  def roll (self):
    self.hi_result = {
      'value': -999999,
      'ids': []}
    self.lo_result = {
      'value': 999999,
      'ids': []}

    # obtem resultados da rolagem do dado
    for i in range(self.amount):
      result_i = random.randint(1, self.faces)
      self.results.append({
        'natural': result_i,
        'modified': result_i})
      
      # obtem maior resultado
      if result_i > self.hi_result['value']:
        self.hi_result['value'] = result_i
        self.hi_result['ids'] = [i]
      elif result_i == self.hi_result['value']:
        self.hi_result['ids'].append(i)
      
      # obtem menor resultado
      if result_i < self.lo_result['value']:
        self.lo_result['value'] = result_i
        self.lo_result['ids'] = [i]
      elif result_i == self.lo_result['value']:
        self.lo_result['ids'].append(i)
    
    return self.results

  def get_modifier (self):
    if self.modifiers:
      current_mod = self.modifiers.pop(0)
      self.current_modifier = Modifier(
        raw = current_mod)
    else:
      self.current_modifier = None
    return self.current_modifier

  def mul_each_result (self, modifier):
    for i, _ in enumerate(self.results):
      self.results[i]['modified'] *= modifier.value
      
  def div_each_result (self, modifier):
    for i, _ in enumerate(self.results):
      self.results[i]['modified'] /= modifier.value
        
  def add_each_result (self, modifier):
    for i, _ in enumerate(self.results):
      self.results[i]['modified'] += modifier.value
      
  def sub_each_result (self, modifier):
    for i, _ in enumerate(self.results):
      self.results[i]['modified'] -= modifier.value
    
  def restart_modifiers (self):
    self.modifiers.extend(self.__mods_rawlist)
    
  def total_sum (self, result_type:str) -> float:
    total_sum = sum(float(result[result_type]) for result in self.results)
    return total_sum
  
  @property
  def hires_moded (self):
    if self.hi_result['ids']:
      result_i = self.hi_result['ids'][0]
      return self.results[result_i]['modified']
  
  @property
  def lores_moded (self):
    if self.lo_result['ids']:
      result_i = self.lo_result['ids'][0]
      return self.results[result_i]['modified']


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

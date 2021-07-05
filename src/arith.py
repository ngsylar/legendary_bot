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
  def __init__ (self, overall_exp):
    self.overall_exp = overall_exp

  def operator_is_mul (self):
    self.match = re.search(regex.MODIFIER_MUL, self.overall_exp)
    self.__set_value()
    return self.match

  def operator_is_div (self):
    self.match = re.search(regex.MODIFIER_DIV, self.overall_exp)
    self.__set_value()
    return self.match
    
  def operator_is_add (self):
    self.match = re.search(regex.MODIFIER_ADD, self.overall_exp)
    self.__set_value()
    return self.match
    
  def operator_is_sub (self):
    self.match = re.search(regex.MODIFIER_SUB, self.overall_exp)
    self.__set_value()
    return self.match

  def __set_value (self):
    if self.match:
      self.value = float(self.match[1])


class Dice:
  # editar: edicao de baixa prioridade, depois ver um jeito de separar modificadores dessa classe
  def __init__ (self, name, address, modifiers_raw, modifiers_address):
    self.name = name
    self.address = address
    self.modifiers_raw = modifiers_raw
    self.modifiers_address = modifiers_address
    self.__decode_name(name)

  def __decode_name (self, name):
    dRaw = name.split('d', 1)
    self.amount = int(dRaw[0])
    self.faces = int(dRaw[1])
    self.modifiers = []
    self.results = []
    self.__validate()

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

  # editar: transformar a gambiarra do retorno em algo que faca sentido
  def has_modifier (self):
    self.current_modifier = Modifier(
      overall_exp = self.modifiers_raw)
    return True

  def mul_each_result (self, modifier, clear_after_op=False):
    for i, _ in enumerate(self.results):
      self.results[i]['modified'] *= modifier.value
    if clear_after_op:
      self.clear_modifier(modifier)
  
  def div_each_result (self, modifier, clear_after_op=False):
    for i, _ in enumerate(self.results):
      self.results[i]['modified'] /= modifier.value
    if clear_after_op:
      self.clear_modifier(modifier)
    
  def add_each_result (self, modifier, clear_after_op=False):
    for i, _ in enumerate(self.results):
      self.results[i]['modified'] += modifier.value
    if clear_after_op:
      self.clear_modifier(modifier)
  
  def sub_each_result (self, modifier, clear_after_op=False):
    for i, _ in enumerate(self.results):
      self.results[i]['modified'] -= modifier.value
    if clear_after_op:
      self.clear_modifier(modifier)

  def clear_modifier (self, modifier):
    # guarda modificadores no dado
    modifierRaw = re.sub(r'\.0+e$', '', modifier.match[0]).replace('+-','-')
    self.modifiers.append(modifierRaw)
    
    # apaga modificadores na expressao parcial
    address = modifier.match
    self.modifiers_raw = self.modifiers_raw[:address.start()] + self.modifiers_raw[address.end():]

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
    self.__dice_repetition = None
    
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
    if self.__dice_repetition:
      self.__dice_repetition -= 1
    else:
      self.inner_dice_match = re.search(regex.MULTIPLE_DICE, self.raw)
      self.__dice_repetition = self.inner_dice_match[1]
    return self.inner_dice_match
    
  @property
  def inner_dice (self):
    if self.inner_dice_match:
      address_adjust = self.inner_dice_match.end()
      dice_modifiers_match = re.match(regex.MODIFIERS_RAW, self.raw[address_adjust:])
      return Dice(
        name = self.inner_dice_match[2],
        address = self.inner_dice_match,
        modifiers_raw = dice_modifiers_match[0],
        modifiers_address = {
          'start': dice_modifiers_match.start() + address_adjust,
          'end': dice_modifiers_match.end() + address_adjust})

  def replace (self, address, replacement):
    if type(address) == re.Match:
      self.raw = self.raw[:address.start()] + str(replacement) + self.raw[address.end():]
    elif type(address) == dict:
      self.raw = self.raw[:address['start']] + str(replacement) + self.raw[address['end']:]
    return self.raw
  
  @property
  def result (self):
    return float(self.raw)

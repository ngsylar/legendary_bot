import random
from arith.modifier import Modifier

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

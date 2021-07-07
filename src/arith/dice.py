import random
from arith.modifier import Modifier

class DiceResults:
  def __init__ (self, results=None):
    if results:
      self.results = results
    else:
      self.results = []
  
  def __mul__ (self, modifier):
    results = [result_i*modifier.value for result_i in self.results]
    return results

  def __div__ (self, modifier):
    results = [result_i/modifier.value for result_i in self.results]
    return results

  def __add__ (self, modifier):
    results = [result_i+modifier.value for result_i in self.results]
    return results
  
  def __sub__ (self, modifier):
    results = [result_i-modifier.value for result_i in self.results]
    return results
  
  @property
  def results_sum (self):
    return float(sum(self.results))

class Dice:
  # editar: edicao de baixa prioridade, depois ver um jeito de separar modificadores dessa classe
  def __init__ (self, match, address, modifiers):
    self.repetition = match[1]
    self.name = match[2]
    self.address = address
    
    self.amount = int(match[3])
    self.faces = int(match[4])
    self.__validate()

    self.natural = DiceResults()
    self.modified = DiceResults()

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
      self.natural.results.append(result_i)
      self.modified.results.append(result_i)
      
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
    
    return self.natural.results
  
  @property
  def results (self):
    return self.modified

  def get_modifier (self):
    if self.modifiers:
      current_mod = self.modifiers.pop(0)
      self.current_modifier = Modifier(
        raw = current_mod)
    else:
      self.current_modifier = None
    return self.current_modifier
      
  def restart_modifiers (self):
    self.modifiers.extend(self.__mods_rawlist)
  
  @property
  def hires_moded (self):
    if self.hi_result['ids']:
      result_i = self.hi_result['ids'][0]
      return self.modified.results[result_i]
  
  @property
  def lores_moded (self):
    if self.lo_result['ids']:
      result_i = self.lo_result['ids'][0]
      return self.modified.results[result_i]

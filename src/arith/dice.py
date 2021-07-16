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
  
  def results_sum (self, selection):
    if selection['type'] and (selection['amount'] == 0):
      selection_sum = float(0)
    elif selection['type'] == 'h':
      selection_sum = float(sum(self.results[:selection['amount']]))
    elif selection['type'] == 'l':
      selection_sum = float(sum(self.results[-selection['amount']:]))
    else:
      selection_sum = float(sum(self.results))
    return selection_sum

class Dice:
  def __init__ (self, match, address, modifiers):
    self.repetition = match[1]
    self.name = match[2]
    self.address = address
    
    self.amount = int(match[3])
    self.faces = int(match[4])

    self.__decode_selection(match)
    self.__validate()

    self.natural = DiceResults()
    self.modified = DiceResults()

    self.modifiers = modifiers
    self.__mods_rawlist = modifiers.copy()

  def __decode_selection (self, match):
    self.selection = {'type': None}

    dice_selection = match[5] or match[7]
    if dice_selection:
      selection_amount = match[6] or match[8] or '1'
      
      if (dice_selection == '!l') or (dice_selection == 'nl'):
        self.selection['type'] = 'h'
        self.selection['amount'] = self.amount - int(selection_amount)
      
      elif (dice_selection == '!h') or (dice_selection == 'nh'):
        self.selection['type'] = 'l'
        self.selection['amount'] = self.amount - int(selection_amount)
      
      else:
        self.selection['type'] = dice_selection
        self.selection['amount'] = int(selection_amount)

  def __validate (self):
    invalid_amount = (self.amount < 1) or (self.amount > 100)
    invalid_faces = (self.faces < 2) or (self.faces > 1000)
    if invalid_amount or invalid_faces:
      raise
    
    if self.selection['type']:
      invalid_selection = (self.selection['amount'] < 0) or (self.selection['amount'] > self.amount)
      if invalid_selection:
        raise
    
  def roll (self):
    for _ in range(self.amount):
      result_i = random.randint(1, self.faces)
      self.natural.results.append(result_i)
    self.natural.results.sort(reverse=True)
    self.modified.results = self.natural.results.copy()
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
  def hi_mod_res (self):
    if self.modified.results:
      return self.modified.results[0]
  
  @property
  def hi_nat_res (self):
    if self.natural.results:
      return self.natural.results[0]

  @property
  def lo_mod_res (self):
    if self.modified.results:
      last_i = len(self.modified.results) - 1
      return self.modified.results[last_i]

  @property
  def lo_nat_res (self):
    if self.natural.results:
      last_i = len(self.natural.results) - 1
      return self.natural.results[last_i]

import re
from dconsts import DefaultRegexes as regex

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

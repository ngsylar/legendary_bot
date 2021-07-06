import re
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

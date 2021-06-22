import re

def rolardados():
    return 1

class DefaultRegexes:
    OPERATOR = r'([\*\/\+\-])'
    FLOAT_VALUE = r'(\-?\d+(?:\.\d+)?)'
    ARITH_CONTEXT = r'(?:\()([^()]+)(?:\))'

    ARITH_MUL = FLOAT_VALUE + r'\*' + FLOAT_VALUE
    ARITH_DIV = FLOAT_VALUE + r'\/' + FLOAT_VALUE
    ARITH_ADD = FLOAT_VALUE + r'\+' + FLOAT_VALUE
    ARITH_SUB = FLOAT_VALUE + r'\-' + FLOAT_VALUE

    DICE = r'(\d+[Dd]\d+)'
    MODIFIER = OPERATOR + r'(\d+(?:\.\d+)?)(?i:(each|e))'
    MODIFIERS_CONTEXT = r'(?:(?![\*\/\+\-]\-?\d+d).)*'

    MODIFIER_MUL = r'\*'+ FLOAT_VALUE +r'e'
    MODIFIER_DIV = r'\/'+ FLOAT_VALUE +r'e'
    MODIFIER_ADD = r'\+'+ FLOAT_VALUE +r'e'
    MODIFIER_SUB = r'\-'+ FLOAT_VALUE +r'e'

class Arithmetic (DefaultRegexes):
    def __init__ (self):
        self.operation_is_not_performed = True

    def operator_is_mul (self, context):
        self.operation_raw = re.search(self.ARITH_MUL, context)
        self.__set_operation_factors()
        return self.operation_raw
    
    def operator_is_div (self, context):
        self.operation_raw = re.search(self.ARITH_DIV, context)
        self.__set_operation_factors()
        return self.operation_raw
    
    def operator_is_add (self, context):
        self.operation_raw = re.search(self.ARITH_ADD, context)
        self.__set_operation_factors()
        return self.operation_raw
    
    def operator_is_sub (self, context):
        self.operation_raw = re.search(self.ARITH_SUB, context)
        self.__set_operation_factors()
        return self.operation_raw

    def __set_operation_factors (self):
        if self.operation_raw:
            self.factors = [
                float(self.operation_raw[1]),
                float(self.operation_raw[2])
            ]

class DiceEffect (DefaultRegexes):
    def __init__ (self):
        self.modifier_is_not_applied = True

    def modifier_operator_is_mul (self, context):
        self.modifier_raw = re.search(self.MODIFIER_MUL, context)
        self.__set_modifier_value()
        return self.modifier_raw

    def modifier_operator_is_div (self, context):
        self.modifier_raw = re.search(self.MODIFIER_DIV, context)
        self.__set_modifier_value()
        return self.modifier_raw
    
    def modifier_operator_is_add (self, context):
        self.modifier_raw = re.search(self.MODIFIER_ADD, context)
        self.__set_modifier_value()
        return self.modifier_raw
    
    def modifier_operator_is_sub (self, context):
        self.modifier_raw = re.search(self.MODIFIER_SUB, context)
        self.__set_modifier_value()
        return self.modifier_raw

    def __set_modifier_value (self):
        if self.modifier_raw:
            self.modifier_value = float(self.modifier_raw[1])

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
    def operator_is_mul (self, context):
        self.operation = re.search(self.ARITH_MUL, context)
        self.__set_operation_factors()
        return self.operation
    
    def operator_is_div (self, context):
        self.operation = re.search(self.ARITH_DIV, context)
        self.__set_operation_factors()
        return self.operation
    
    def operator_is_add (self, context):
        self.operation = re.search(self.ARITH_ADD, context)
        self.__set_operation_factors()
        return self.operation
    
    def operator_is_sub (self, context):
        self.operation = re.search(self.ARITH_SUB, context)
        self.__set_operation_factors()
        return self.operation

    def __set_operation_factors (self):
        if self.operation:
            self.factors = [
                float(self.operation[1]),
                float(self.operation[2])
            ]

class DiceEffect (DefaultRegexes):
    def modifier_operator_is_mul (self, context):
        self.modifier_effect = re.search(self.MODIFIER_MUL, context)
        self.__set_modifier_value()
        return self.modifier_effect

    def modifier_operator_is_div (self, context):
        self.modifier_effect = re.search(self.MODIFIER_DIV, context)
        self.__set_modifier_value()
        return self.modifier_effect
    
    def modifier_operator_is_add (self, context):
        self.modifier_effect = re.search(self.MODIFIER_ADD, context)
        self.__set_modifier_value()
        return self.modifier_effect
    
    def modifier_operator_is_sub (self, context):
        self.modifier_effect = re.search(self.MODIFIER_SUB, context)
        self.__set_modifier_value()
        return self.modifier_effect

    def __set_modifier_value (self):
        if self.modifier_effect:
            self.modifier_value = float(self.modifier_effect[1])

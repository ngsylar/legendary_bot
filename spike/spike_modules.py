import re

class DefaultRegexes:
    OPERATOR = r'([\*\/\+\-])'
    FLOAT_VALUE = r'(\-?\d+(?:\.\d+)?)'
    ARITH_EXPRESSION = r'(?:\()([^()]+)(?:\))'

    ARITH_MUL = FLOAT_VALUE + r'\*' + FLOAT_VALUE
    ARITH_DIV = FLOAT_VALUE + r'\/' + FLOAT_VALUE
    ARITH_ADD = FLOAT_VALUE + r'\+' + FLOAT_VALUE
    ARITH_SUB = FLOAT_VALUE + r'\-' + FLOAT_VALUE

    DICE = r'(\d+[Dd]\d+)'
    MODIFIER = OPERATOR + r'(\d+(?:\.\d+)?)(?i:(each|e))'
    MODIFIERS_RAW = r'(?:(?![\*\/\+\-]\-?\d+d).)*'

    MODIFIER_MUL = r'\*'+ FLOAT_VALUE +r'e'
    MODIFIER_DIV = r'\/'+ FLOAT_VALUE +r'e'
    MODIFIER_ADD = r'\+'+ FLOAT_VALUE +r'e'
    MODIFIER_SUB = r'\-'+ FLOAT_VALUE +r'e'


class ArithmeticOperation (DefaultRegexes):
    def __init__ (self):
        self.operation_is_not_performed = True

    def operator_is_mul (self, expression):
        self.operation_match = re.search(self.ARITH_MUL, expression)
        self.__set_operation_factors()
        return self.operation_match
    
    def operator_is_div (self, expression):
        self.operation_match = re.search(self.ARITH_DIV, expression)
        self.__set_operation_factors()
        return self.operation_match
    
    def operator_is_add (self, expression):
        self.operation_match = re.search(self.ARITH_ADD, expression)
        self.__set_operation_factors()
        return self.operation_match
    
    def operator_is_sub (self, expression):
        self.operation_match = re.search(self.ARITH_SUB, expression)
        self.__set_operation_factors()
        return self.operation_match

    def __set_operation_factors (self):
        if self.operation_match:
            self.factors = [
                float(self.operation_match[1]),
                float(self.operation_match[2])]
    
    @property
    def operation (self):
        return self.operation_match


class DiceModifier (DefaultRegexes):
    def __init__ (self):
        self.modifier_is_not_applied = True

    def modifier_operator_is_mul (self, expression_raw):
        self.modifier_match = re.search(self.MODIFIER_MUL, expression_raw)
        self.__set_modifier_value()
        return self.modifier_match

    def modifier_operator_is_div (self, expression_raw):
        self.modifier_match = re.search(self.MODIFIER_DIV, expression_raw)
        self.__set_modifier_value()
        return self.modifier_match
    
    def modifier_operator_is_add (self, expression_raw):
        self.modifier_match = re.search(self.MODIFIER_ADD, expression_raw)
        self.__set_modifier_value()
        return self.modifier_match
    
    def modifier_operator_is_sub (self, expression_raw):
        self.modifier_match = re.search(self.MODIFIER_SUB, expression_raw)
        self.__set_modifier_value()
        return self.modifier_match

    def __set_modifier_value (self):
        if self.modifier_match:
            self.modifier_value = float(self.modifier_match[1])

    @property
    def modifier (self):
        return self.modifier_match


class RollExpression (DefaultRegexes):
    def __init__ (self, expression, pattern_expression=False):
        if pattern_expression:
            self.expression = '('+expression.lower().replace('each', 'e').replace(',', '.')+')'
        else:
            self.expression = expression
    
    def has_inner_expression (self):
        self.inner_expression_match = re.search(self.ARITH_EXPRESSION, self.expression)
        if self.inner_expression_match:
            self.inner_expression_raw = self.inner_expression_match[1]
        return self.inner_expression_match
    
    def has_dice (self):
        self.inner_dice_match = re.search(self.DICE, self.expression)
        if self.inner_dice_match:
            position_adjust = self.inner_dice_match.end()
            dice_modifiers_match = re.match(self.MODIFIERS_RAW, self.expression[position_adjust:])
            self.dice_modifiers_raw = dice_modifiers_match[0]
            self.dice_modifiers_position = {
                'start': dice_modifiers_match.start() + position_adjust,
                'end': dice_modifiers_match.end() + position_adjust}
        return self.inner_dice_match

    def replace (self, operation, result):
        if type(operation) == re.Match:
            self.expression = self.expression[:operation.start()] + str(result) + self.expression[operation.end():]
        elif type(operation) == dict:
            self.expression = self.expression[:operation['start']] + str(result) + self.expression[operation['end']:]
        return self.expression

    @property
    def raw (self):
        return self.expression
    @raw.setter
    def raw (self, value):
        self.expression = value

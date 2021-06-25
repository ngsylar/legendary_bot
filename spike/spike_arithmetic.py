import re
from spike_regexes import DefaultRegexes

class Operation (DefaultRegexes):
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


class Modifier (DefaultRegexes):
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


# class Dice:



class Expression (DefaultRegexes):
    def __init__ (self, raw, position=None, is_pattern=False):
        if is_pattern:
            self.raw = '('+raw.lower().replace('each', 'e').replace(',', '.')+')'
        else:
            self.raw = raw
        if position:
            self.position = position
    
    def has_inner_expression (self):
        self.inner_expression_match = re.search(self.ARITH_EXPRESSION, self.raw)
        if self.inner_expression_match:
            self.inner_expression_raw = self.inner_expression_match[1]
        return self.inner_expression_match
    
    def has_dice (self):
        self.inner_dice_match = re.search(self.DICE, self.raw)
        if self.inner_dice_match:
            position_adjust = self.inner_dice_match.end()
            dice_modifiers_match = re.match(self.MODIFIERS_RAW, self.raw[position_adjust:])
            self.dice_modifiers_raw = dice_modifiers_match[0]
            self.dice_modifiers_position = {
                'start': dice_modifiers_match.start() + position_adjust,
                'end': dice_modifiers_match.end() + position_adjust}
        return self.inner_dice_match

    def replace (self, position, replacement):
        if type(position) == re.Match:
            self.raw = self.raw[:position.start()] + str(replacement) + self.raw[position.end():]
        elif type(position) == dict:
            self.raw = self.raw[:position['start']] + str(replacement) + self.raw[position['end']:]
        return self.raw

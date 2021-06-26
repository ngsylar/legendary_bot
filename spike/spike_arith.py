import re
from spike_regexes import DefaultRegexes

class Operation (DefaultRegexes):
    def __init__ (self, overall_exp):
        self.overall_exp = overall_exp

    def is_mul (self):
        self.match = re.search(self.ARITH_MUL, self.overall_exp)
        self.__set_operation_factors()
        return self.match
    
    def is_div (self):
        self.match = re.search(self.ARITH_DIV, self.overall_exp)
        self.__set_operation_factors()
        return self.match
    
    def is_add (self):
        self.match = re.search(self.ARITH_ADD, self.overall_exp)
        self.__set_operation_factors()
        return self.match
    
    def is_sub (self):
        self.match = re.search(self.ARITH_SUB, self.overall_exp)
        self.__set_operation_factors()
        return self.match

    def __set_operation_factors (self):
        if self.match:
            self.factors = {
                'left': float(self.match[1]),
                'right': float(self.match[2])}


class Modifier (DefaultRegexes):
    def __init__ (self, overall_exp):
        self.overall_exp = overall_exp

    def operator_is_mul (self):
        self.match = re.search(self.MODIFIER_MUL, self.overall_exp)
        self.__set_value()
        return self.match

    def operator_is_div (self):
        self.match = re.search(self.MODIFIER_DIV, self.overall_exp)
        self.__set_value()
        return self.match
    
    def operator_is_add (self):
        self.match = re.search(self.MODIFIER_ADD, self.overall_exp)
        self.__set_value()
        return self.match
    
    def operator_is_sub (self):
        self.match = re.search(self.MODIFIER_SUB, self.overall_exp)
        self.__set_value()
        return self.match

    def __set_value (self):
        if self.match:
            self.value = float(self.match[1])


class Dice (DefaultRegexes):
    def __init__ (self, name, address, modifiers_raw, modifiers_address):
        self.name = name
        self.address = address
        self.modifiers_raw = modifiers_raw
        self.modifiers_address = modifiers_address
    
    def has_modifier (self):
        self.current_modifier = Modifier(
            overall_exp = self.modifiers_raw)
        return True
    
    def clear_modifier (self, modifier):
        address = modifier.match
        self.modifiers_raw = self.modifiers_raw[:address.start()] + self.modifiers_raw[address.end():]


class Expression (DefaultRegexes):
    def __init__ (self, raw, address=None, is_pattern=False):
        if is_pattern:
            self.raw = '('+raw.lower().replace('each', 'e').replace(',', '.')+')'
        else:
            self.raw = raw
        if address:
            self.address = address
    
    def has_inner_expression (self):
        self.__inner_expression_match = re.search(self.ARITH_EXPRESSION, self.raw)
        return self.__inner_expression_match
    
    @property
    def inner_expression (self):
        if self.__inner_expression_match:
            return Expression(
                raw = self.__inner_expression_match[1],
                address = self.__inner_expression_match)
    
    def has_operation (self):
        self.current_operation = Operation(
            overall_exp = self.raw)
        return True

    def has_dice (self):
        self.inner_dice_match = re.search(self.DICE, self.raw)
        return self.inner_dice_match
    
    @property
    def inner_dice (self):
        if self.inner_dice_match:
            address_adjust = self.inner_dice_match.end()
            dice_modifiers_match = re.match(self.MODIFIERS_RAW, self.raw[address_adjust:])
            return Dice(
                name = self.inner_dice_match[1],
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

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

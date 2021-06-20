class DefaultRegexes:
    operator = r'([\*\/\+\-])'
    floatValue = r'(\-?\d+(?:\.\d+)?)'
    arithContext = r'(?:\()([^()]+)(?:\))'

    arithMul = floatValue + r'\*' + floatValue
    arithDiv = floatValue + r'\/' + floatValue
    arithAdd = floatValue + r'\+' + floatValue
    arithSub = floatValue + r'\-' + floatValue

    diceOnly = r'(\d+[Dd]\d+)'
    dice = operator + r'?(\d+d\d+)'
    modifier = operator + r'(\d+(?:\.\d+)?)(?i:(each|e))'
    modifiersContext = r'(?:(?![\*\/\+\-]\-?\d+d).)*'

    modifierMul = r'\*'+ floatValue +r'e'
    modifierDiv = r'\/'+ floatValue +r'e'
    modifierAdd = r'\+'+ floatValue +r'e'
    modifierSub = r'\-'+ floatValue +r'e'

def rolardados():
    return 1

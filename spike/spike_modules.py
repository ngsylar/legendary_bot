class DefaultRegexes:
    dice = r'([\*\/\+\-])?(\d+d\d+)'
    #modifier = r'([\*\/\+\-])(\d+(?:\.\d+)?)e'
    modifiersContext = r'(?:(?![\*\/\+\-]\-?\d+d).)*'
    floatValue = '(\-?\d+(?:\.\d+)?)'

    arithContext = r'(?:\()([^()]+)(?:\))'
    arithMul = floatValue + r'\*' + floatValue
    arithDiv = floatValue + r'\/' + floatValue
    arithAdd = floatValue + r'\+' + floatValue
    arithSub = floatValue + r'\-' + floatValue

    modifierMul = r'\*'+ floatValue +r'e'
    modifierDiv = r'\/'+ floatValue +r'e'
    modifierAdd = r'\+'+ floatValue +r'e'
    modifierSub = r'\-'+ floatValue +r'e'

def rolardados():
    return 1

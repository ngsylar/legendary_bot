# (?:(?!ab).)*
import re

roll = '-13-9+1d20+684-687e+684+2d8+7-3e+4e+1'

rolls = []

diceRegex = r'\d+[SsHh]?[Dd]\d+'
sumRegex = r'(?:(?![+\-]?\d+d).)*'

rolls.append(re.match(sumRegex, roll)[0])
rolls.extend(re.findall(r'[+\-]?\d+d'+sumRegex, roll))
rolls = list(filter(None, rolls))

print(rolls)

#-------------------------------------------------------------------

def rolardados():
    return 1

expressionInput = '(((1D8+4/2+100*3,22+2D20-1each+1*2e-2+1d8)*2+(1+3)/(2+2-(1+1))+4)+2)/2'
#expressionInput = '(((4/2+100*3,22+2D20-1e+1*2e-2+1d8)*2+(1+3)/(2+2-(1+1))+4)+2)/2'
#expressionInput = '(((4/2+10*-3.2-2)*2+(1+3)/(2+2-(1+1))+4)+2)/2'

diceRegex = r'([\*\/\+\-])?(\d+d\d+)'
#modifierRegex = r'([\*\/\+\-])(\d+(?:\.\d+)?)e'
modifiersContextRegex = r'(?:(?![\*\/\+\-]\-?\d+d).)*'
floatValueRegex = '(\-?\d+(?:\.\d+)?)'

arithContextRegex = r'(?:\()([^()]+)(?:\))'
arithMulRegex = floatValueRegex + r'\*' + floatValueRegex
arithDivRegex = floatValueRegex + r'\/' + floatValueRegex
arithAddRegex = floatValueRegex + r'\+' + floatValueRegex
arithSubRegex = floatValueRegex + r'\-' + floatValueRegex

modifierMulRegex = r'\*'+ floatValueRegex +r'e'
modifierDivRegex = r'\/'+ floatValueRegex +r'e'
modifierAddRegex = r'\+'+ floatValueRegex +r'e'
modifierSubRegex = r'\-'+ floatValueRegex +r'e'

def compute_arith (context, operation, result):
    context = context[:operation.start()] + str(result) + context[operation.end():]
    return context

expressionRaw = '('+expressionInput.lower().replace('each', 'e').replace(',', '.')+')'
print(expressionRaw)
matchedArith = re.search(arithContextRegex, expressionRaw)
arithContext = matchedArith[1]
print(arithContext)

matched_d = re.search(diceRegex, arithContext)
while matched_d:
    modifiersMarker = {}
    modifiersMarker['start'] = matched_d.end()
    matchedModifiers = re.match(modifiersContextRegex, arithContext[modifiersMarker['start']:])
    modifiersMarker['end'] = matched_d.end() + matchedModifiers.end()
    modifiersRaw = matchedModifiers[0]

    # editar: aqui usar o lancamento de dado (neste trecho de codigo foi usado apenas uma substituicao simples, pois o lancamento ja foi implementado, nao sendo o foco deste teste)
    resultados = []
    resultados_simples = rolardados()
    resultados_compostos = resultados_simples
    while 1:
        mod_is_mul = re.search(modifierMulRegex, modifiersRaw)
        mod_is_div = re.search(modifierDivRegex, modifiersRaw)
        mod_is_add = re.search(modifierAddRegex, modifiersRaw)
        mod_is_sub = re.search(modifierSubRegex, modifiersRaw)
        
        if mod_is_mul:
            resultados_compostos *= float(mod_is_mul[1])
            modifiersRaw = compute_arith(modifiersRaw, mod_is_mul, '')
        elif mod_is_div:
            resultados_compostos /= float(mod_is_div[1])
            modifiersRaw = compute_arith(modifiersRaw, mod_is_div, '')
        elif mod_is_add:
            resultados_compostos += float(mod_is_add[1])
            modifiersRaw = compute_arith(modifiersRaw, mod_is_add, '')
        elif mod_is_sub:
            resultados_compostos -= float(mod_is_sub[1])
            modifiersRaw = compute_arith(modifiersRaw, mod_is_sub, '')
        else:
            resultado_total_composto = resultados_compostos
            arithContext = arithContext[:modifiersMarker['start']] + modifiersRaw + arithContext[modifiersMarker['end']:]
            arithContext = arithContext[:matched_d.start()] + (matched_d[1] or '') + str(resultado_total_composto) + arithContext[matched_d.end():]
            print(arithContext)
            break

    matched_d = re.search(diceRegex, arithContext)

while 1:
    op_is_mul = re.search(arithMulRegex, arithContext)
    op_is_div = re.search(arithDivRegex, arithContext)
    op_is_add = re.search(arithAddRegex, arithContext)
    op_is_sub = re.search(arithSubRegex, arithContext)
    
    if op_is_mul:
        mulResult = float(op_is_mul[1]) * float(op_is_mul[2])
        arithContext = compute_arith(arithContext, op_is_mul, mulResult)
    elif op_is_div:
        divResult = float(op_is_div[1]) / float(op_is_div[2])
        arithContext = compute_arith(arithContext, op_is_div, divResult)
    elif op_is_add:
        addResult = float(op_is_add[1]) + float(op_is_add[2])
        arithContext = compute_arith(arithContext, op_is_add, addResult)
    elif op_is_sub:
        subResult = float(op_is_sub[1]) - float(op_is_sub[2])
        arithContext = compute_arith(arithContext, op_is_sub, subResult)
    else:
        print(arithContext)
        break

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

#expression = '(((1d8+4/2+100*3.22+2d20-1e+1*2e-2+1d8)*2+(1+3)/(2+2-(1+1))+4)+2)/2'
expression = '(((4/2+100*3.22+2d20-1e+1*2e-2+1d8)*2+(1+3)/(2+2-(1+1))+4)+2)/2'
#expression = '(((4/2+10*-3.2-2)*2+(1+3)/(2+2-(1+1))+4)+2)/2'

diceRegex = r'([\*\/\+\-])?(\d+d\d+)'
modifierRegex = r'([\*\/\+\-])(\d+(?:\.\d+)?)e'
modifiersRawRegex = r'(?:(?![\*\/\+\-]\-?\d+d).)*'

arithContextRegex = r'(?:\()([^()]+)(?:\))'
arithMulRegex = r'(\-?\d+(?:\.\d+)?)\*(\-?\d+(?:\.\d+)?)'
arithDivRegex = r'(\-?\d+(?:\.\d+)?)\/(\-?\d+(?:\.\d+)?)'
arithAddRegex = r'(\-?\d+(?:\.\d+)?)\+(\-?\d+(?:\.\d+)?)'
arithSubRegex = r'(\-?\d+(?:\.\d+)?)\-(\-?\d+(?:\.\d+)?)'

modifierMulRegex = r'\*(\-?\d+(?:\.\d+)?)e'
modifierDivRegex = r'\/(\-?\d+(?:\.\d+)?)e'
modifierAddRegex = r'\+(\-?\d+(?:\.\d+)?)e'
modifierSubRegex = r'\-(\-?\d+(?:\.\d+)?)e'

def compute_arith (context, operation, result):
    print(operation)
#    print(result)
    context = context[:operation.start()] + str(result) + context[operation.end():]
    print(context)
    return context

matchedArith = re.search(arithContextRegex, expression)
arithContextRaw = matchedArith[1]
print(arithContextRaw)

matched_d = re.search(diceRegex, arithContextRaw)
print(matched_d)
modifiersMarker = {}
modifiersMarker['start'] = matched_d.end()
matchedMods = re.match(modifiersRawRegex, arithContextRaw[modifiersMarker['start']:])
modifiersMarker['end'] = matched_d.end() + matchedMods.end()
modifiersRaw = matchedMods[0]
print(matchedMods)

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
        break



# arithContext = matchedArith.group(1)
# print(arithContext)
# while 1:
#     op_is_mul = re.search(arithMulRegex, arithContext)
#     op_is_div = re.search(arithDivRegex, arithContext)
#     op_is_add = re.search(arithAddRegex, arithContext)
#     op_is_sub = re.search(arithSubRegex, arithContext)
    
#     if op_is_mul:
#         mulResult = float(op_is_mul[1]) * float(op_is_mul[2])
#         arithContext = compute_arith(arithContext, op_is_mul, mulResult)
#     elif op_is_div:
#         divResult = float(op_is_div[1]) / float(op_is_div[2])
#         arithContext = compute_arith(arithContext, op_is_div, divResult)
#     elif op_is_add:
#         addResult = float(op_is_add[1]) + float(op_is_add[2])
#         arithContext = compute_arith(arithContext, op_is_add, addResult)
#     elif op_is_sub:
#         subResult = float(op_is_sub[1]) - float(op_is_sub[2])
#         arithContext = compute_arith(arithContext, op_is_sub, subResult)
#     else:
#         break

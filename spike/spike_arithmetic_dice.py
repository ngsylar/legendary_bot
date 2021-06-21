import re
from spike_modules import DefaultRegexes as regex, Arithmetic, DiceEffect, rolardados

expressionInput = '(((1D8+4/2+100*3,22+2D20-1each+1*2e-2+1d8)*2+(1+3)/(2+2-(1+1))+4)+2)/2'
#expressionInput = '(((4/2+100*3,22+2D20-1e+1*2e-2+1d8)*2+(1+3)/(2+2-(1+1))+4)+2)/2'
#expressionInput = '(((4/2+10*-3.2-2)*2+(1+3)/(2+2-(1+1))+4)+2)/2'

def compute_arith (context, operation, result):
    context = context[:operation.start()] + str(result) + context[operation.end():]
    return context

expressionRaw = '('+expressionInput.lower().replace('each', 'e').replace(',', '.')+')'
print(expressionRaw)

matchedArithContext = re.search(regex.ARITH_CONTEXT, expressionRaw)
while matchedArithContext:
    arithContext = matchedArithContext[1]
    # print(arithContext)

    matched_d = re.search(regex.DICE, arithContext)
    while matched_d:
        modifiersContextMarker = {}
        modifiersContextMarker['start'] = matched_d.end()
        matchedModifiersContext = re.match(regex.MODIFIERS_CONTEXT, arithContext[modifiersContextMarker['start']:])
        modifiersContextMarker['end'] = matched_d.end() + matchedModifiersContext.end()
        modifiersContext = matchedModifiersContext[0]

        # editar: aqui usar o lancamento de dado (neste trecho de codigo foi usado apenas uma substituicao simples, pois o lancamento ja foi implementado, nao sendo o foco deste teste)
        resultados = []
        resultados_simples = rolardados()
        resultados_compostos = resultados_simples
        
        current = DiceEffect()
        while 1:
            if current.modifier_operator_is_mul(modifiersContext):
                resultados_compostos *= current.modifier_value
                modifiersContext = compute_arith(modifiersContext, current.modifier_effect, '')
            elif current.modifier_operator_is_div(modifiersContext):
                resultados_compostos /= current.modifier_value
                modifiersContext = compute_arith(modifiersContext, current.modifier_effect, '')
            elif current.modifier_operator_is_add(modifiersContext):
                resultados_compostos += current.modifier_value
                modifiersContext = compute_arith(modifiersContext, current.modifier_effect, '')
            elif current.modifier_operator_is_sub(modifiersContext):
                resultados_compostos -= current.modifier_value
                modifiersContext = compute_arith(modifiersContext, current.modifier_effect, '')
            else:
                resultado_total_composto = resultados_compostos
                arithContext = arithContext[:modifiersContextMarker['start']] + modifiersContext + arithContext[modifiersContextMarker['end']:]
                arithContext = arithContext[:matched_d.start()] + (matched_d[1] or '') + str(resultado_total_composto) + arithContext[matched_d.end():]
                # print(arithContext)
                break

        matched_d = re.search(regex.DICE, arithContext)

    current = Arithmetic()
    while 1:
        if current.operator_is_mul(arithContext):
            mulResult = current.factors[0] * current.factors[1]
            arithContext = compute_arith(arithContext, current.operation, mulResult)
        elif current.operator_is_div(arithContext):
            divResult = current.factors[0] / current.factors[1]
            arithContext = compute_arith(arithContext, current.operation, divResult)
        elif current.operator_is_add(arithContext):
            addResult = current.factors[0] + current.factors[1]
            arithContext = compute_arith(arithContext, current.operation, addResult)
        elif current.operator_is_sub(arithContext):
            subResult = current.factors[0] - current.factors[1]
            arithContext = compute_arith(arithContext, current.operation, subResult)
        else:
            # print(arithContext)
            expressionRaw = compute_arith(expressionRaw, matchedArithContext, arithContext)
            break
    
    matchedArithContext = re.search(regex.ARITH_CONTEXT, expressionRaw)
    print(expressionRaw)

expressionOutput = re.sub(regex.MODIFIER, '', expressionInput).replace('.', ',')
foundDices = re.findall(regex.DICE_ONLY, expressionInput)
for d in range(len(foundDices)):
    expressionOutput = re.sub(regex.DICE_ONLY, 'dice('+str(d+1)+')', expressionOutput, 1)
foundOperators = list(set(re.findall(regex.OPERATOR, expressionOutput)))
for op in foundOperators:
    expressionOutput = expressionOutput.replace(op, ' '+op+' ')
print(expressionOutput)

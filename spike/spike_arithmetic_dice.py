import re
from spike_modules import DefaultRegexes as rx, rolardados

expressionInput = '(((1D8+4/2+100*3,22+2D20-1each+1*2e-2+1d8)*2+(1+3)/(2+2-(1+1))+4)+2)/2'
#expressionInput = '(((4/2+100*3,22+2D20-1e+1*2e-2+1d8)*2+(1+3)/(2+2-(1+1))+4)+2)/2'
#expressionInput = '(((4/2+10*-3.2-2)*2+(1+3)/(2+2-(1+1))+4)+2)/2'

def compute_arith (context, operation, result):
    context = context[:operation.start()] + str(result) + context[operation.end():]
    return context

expressionRaw = '('+expressionInput.lower().replace('each', 'e').replace(',', '.')+')'
print(expressionRaw)

matchedArithContext = re.search(rx.arithContext, expressionRaw)
while matchedArithContext:
    arithContext = matchedArithContext[1]
    print(arithContext)

    matched_d = re.search(rx.dice, arithContext)
    while matched_d:
        modifiersContextMarker = {}
        modifiersContextMarker['start'] = matched_d.end()
        matchedModifiersContext = re.match(rx.modifiersContext, arithContext[modifiersContextMarker['start']:])
        modifiersContextMarker['end'] = matched_d.end() + matchedModifiersContext.end()
        modifiersContext = matchedModifiersContext[0]

        # editar: aqui usar o lancamento de dado (neste trecho de codigo foi usado apenas uma substituicao simples, pois o lancamento ja foi implementado, nao sendo o foco deste teste)
        resultados = []
        resultados_simples = rolardados()
        resultados_compostos = resultados_simples
        while 1:
            mod_is_mul = re.search(rx.modifierMul, modifiersContext)
            mod_is_div = re.search(rx.modifierDiv, modifiersContext)
            mod_is_add = re.search(rx.modifierAdd, modifiersContext)
            mod_is_sub = re.search(rx.modifierSub, modifiersContext)
            
            if mod_is_mul:
                resultados_compostos *= float(mod_is_mul[1])
                modifiersContext = compute_arith(modifiersContext, mod_is_mul, '')
            elif mod_is_div:
                resultados_compostos /= float(mod_is_div[1])
                modifiersContext = compute_arith(modifiersContext, mod_is_div, '')
            elif mod_is_add:
                resultados_compostos += float(mod_is_add[1])
                modifiersContext = compute_arith(modifiersContext, mod_is_add, '')
            elif mod_is_sub:
                resultados_compostos -= float(mod_is_sub[1])
                modifiersContext = compute_arith(modifiersContext, mod_is_sub, '')
            else:
                resultado_total_composto = resultados_compostos
                arithContext = arithContext[:modifiersContextMarker['start']] + modifiersContext + arithContext[modifiersContextMarker['end']:]
                arithContext = arithContext[:matched_d.start()] + (matched_d[1] or '') + str(resultado_total_composto) + arithContext[matched_d.end():]
                print(arithContext)
                break

        matched_d = re.search(rx.dice, arithContext)

    while 1:
        op_is_mul = re.search(rx.arithMul, arithContext)
        op_is_div = re.search(rx.arithDiv, arithContext)
        op_is_add = re.search(rx.arithAdd, arithContext)
        op_is_sub = re.search(rx.arithSub, arithContext)
        
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
            expressionRaw = expressionRaw[:matchedArithContext.start()] + arithContext + expressionRaw[matchedArithContext.end():]
            break
    
    matchedArithContext = re.search(rx.arithContext, expressionRaw)
    print(expressionRaw)

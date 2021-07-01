import re
import spike_arith
from spike_regexes import DefaultRegexes as regex

userInput = '2d20+(4e-(1+1d4))e'
# userInput = '(((-1D8+4/2+100*3,22+2D20-1each+1*2e-2+1d8)*2+(1+3)/(2+2-(1+1))+4)+2)/2'
# userInput = '(((4/2+100*3,22+2D20-1e+1*2e-2+1d8)*2+(1+3)/(2+2-(1+1))+4)+2)/2'
# userInput = '(((4/2+10*-3.2-2)*2+(1+3)/(2+2-(1+1))+4)+2)/2'

def rolardados():
    return 1

expression = spike_arith.Expression(
    raw = userInput,
    is_pattern = True)
print(expression.raw)

while expression.has_inner_expression():
    innerExpression = expression.inner_expression

    while innerExpression.has_dice():
        innerDice = innerExpression.inner_dice

        # editar: aqui usar o lancamento de dado (neste trecho de codigo foi usado apenas uma substituicao simples, pois o lancamento ja foi implementado, nao sendo o foco deste teste)
        resultados = []
        resultados_simples = rolardados()
        resultados_compostos = resultados_simples
        
        while innerDice.has_modifier():
            modifier = innerDice.current_modifier
            if modifier.operator_is_mul():
                resultados_compostos *= modifier.value
                innerDice.clear_modifier(modifier)
            elif modifier.operator_is_div():
                resultados_compostos /= modifier.value
                innerDice.clear_modifier(modifier)
            elif modifier.operator_is_add():
                resultados_compostos += modifier.value
                innerDice.clear_modifier(modifier)
            elif modifier.operator_is_sub():
                resultados_compostos -= modifier.value
                innerDice.clear_modifier(modifier)
            else:
                resultado_total_composto = resultados_compostos
                innerExpression.replace(innerDice.modifiers_address, innerDice.modifiers_raw)
                innerExpression.replace(innerExpression.inner_dice_match, resultado_total_composto)
                break

    while innerExpression.has_operation():
        operation = innerExpression.current_operation
        if operation.is_mul():
            opResult = operation.factors['left'] * operation.factors['right']
            innerExpression.replace(operation.match, opResult)
        elif operation.is_div():
            opResult = operation.factors['left'] / operation.factors['right']
            innerExpression.replace(operation.match, opResult)
        elif operation.is_add():
            opResult = operation.factors['left'] + operation.factors['right']
            innerExpression.replace(operation.match, opResult)
        elif operation.is_sub():
            opResult = operation.factors['left'] - operation.factors['right']
            innerExpression.replace(operation.match, opResult)
        else:
            expression.replace(innerExpression.address, innerExpression.raw)
            break
    
    print(expression.raw)

expressionOutput = re.sub(regex.MODIFIER, '', userInput).replace('.', ',')
foundDices = re.findall(regex.DICE, userInput)
for d in range(len(foundDices)):
    expressionOutput = re.sub(regex.DICE, 'dice('+str(d+1)+')', expressionOutput, 1)
foundOperators = list(set(re.findall(regex.OPERATOR, expressionOutput)))
for op in foundOperators:
    expressionOutput = expressionOutput.replace(op, ' '+op+' ')
print(expressionOutput)

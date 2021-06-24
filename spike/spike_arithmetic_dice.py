import re
from spike_modules import DefaultRegexes as regex, RollExpression, ArithmeticOperation, DiceModifier

userInput = '(((-1D8+4/2+100*3,22+2D20-1each+1*2e-2+1d8)*2+(1+3)/(2+2-(1+1))+4)+2)/2'
#expressionInput = '(((4/2+100*3,22+2D20-1e+1*2e-2+1d8)*2+(1+3)/(2+2-(1+1))+4)+2)/2'
#expressionInput = '(((4/2+10*-3.2-2)*2+(1+3)/(2+2-(1+1))+4)+2)/2'

def rolardados():
    return 1

expression = RollExpression(userInput, pattern_expression=True)
print(expression.raw)

while expression.has_inner_expression():
    innerExpression = RollExpression(expression.inner_expression_raw)

    while innerExpression.has_dice():
        modifiers = RollExpression(innerExpression.dice_modifiers.raw)

        # editar: aqui usar o lancamento de dado (neste trecho de codigo foi usado apenas uma substituicao simples, pois o lancamento ja foi implementado, nao sendo o foco deste teste)
        resultados = []
        resultados_simples = rolardados()
        resultados_compostos = resultados_simples
        
        current = DiceModifier()
        while current.modifier_is_not_applied:
            if current.modifier_operator_is_mul(modifiers.raw):
                resultados_compostos *= current.modifier_value
                modifiers.replace(current.modifier, '')
            elif current.modifier_operator_is_div(modifiers.raw):
                resultados_compostos /= current.modifier_value
                modifiers.replace(current.modifier, '')
            elif current.modifier_operator_is_add(modifiers.raw):
                resultados_compostos += current.modifier_value
                modifiers.replace(current.modifier, '')
            elif current.modifier_operator_is_sub(modifiers.raw):
                resultados_compostos -= current.modifier_value
                modifiers.replace(current.modifier, '')
            else:
                resultado_total_composto = resultados_compostos
                innerExpression.replace(innerExpression.dice_modifiers, modifiers.raw)
                innerExpression.replace(innerExpression.inner_dice_match, resultado_total_composto)
                break

    current = ArithmeticOperation()
    while current.operation_is_not_performed:
        if current.operator_is_mul(innerExpression.raw):
            opResult = current.factors[0] * current.factors[1]
            innerExpression.replace(current.operation, opResult)
        elif current.operator_is_div(innerExpression.raw):
            opResult = current.factors[0] / current.factors[1]
            innerExpression.replace(current.operation, opResult)
        elif current.operator_is_add(innerExpression.raw):
            opResult = current.factors[0] + current.factors[1]
            innerExpression.replace(current.operation, opResult)
        elif current.operator_is_sub(innerExpression.raw):
            opResult = current.factors[0] - current.factors[1]
            innerExpression.replace(current.operation, opResult)
        else:
            expression.replace(expression.inner_expression, innerExpression.raw)
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

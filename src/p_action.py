import re
import arith
from auxiliary_fs import interpolation
from regexes import DefaultRegexes as regex
from auxiliary_fs import *

class PlayerAction:
  # calcula os resultados da rolagem de dados
  def compute (self, msgContent):
    input_msg = self.__decode_msg(msgContent)
    expression = arith.Expression(input_msg, is_pattern=True)
    
    dices = []
    while expression.has_inner_expression():
      innerExpression = expression.inner_expression

      while innerExpression.has_dice():
        innerDice = innerExpression.inner_dice
        innerDice.roll()

        while innerDice.has_modifier():
          modifier = innerDice.current_modifier
          if modifier.operator_is_mul():
            innerDice.mul_each_result(modifier, clear_after_op=True)
          elif modifier.operator_is_div():
            innerDice.div_each_result(modifier, clear_after_op=True)
          elif modifier.operator_is_add():
            innerDice.add_each_result(modifier, clear_after_op=True)
          elif modifier.operator_is_sub():
            innerDice.sub_each_result(modifier, clear_after_op=True)
          else:
            break
        
        innerDice.sum_all_results()
        innerExpression.replace(innerDice.modifiers_address, innerDice.modifiers_raw)
        innerExpression.replace(innerExpression.inner_dice_match, innerDice.total_sum)
        dices.append(innerDice)
      
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
    
    self.__build_output(input_msg, expression, dices)

  # decodifica mensagem inserida pelo usuario
  def __decode_msg (self, msgContent):
    self.playerQuote = None
    
    # separa rolagem e mensagem embutida pelo jogador
    msgRaw = msgContent.split(' ', 1)
    input_msg = msgRaw[0].lower()
    
    # salva mensagem embutida
    if len(msgRaw) > 1:
      quoteRaw = re.sub(r'^\s+', '', msgRaw[1]).split('\n', 1)[0]
      if len(quoteRaw) > 1:
        self.playerQuote = quoteRaw
    
    return input_msg

  # estrutura a mensagem de saida
  def __build_output (self, output_gexp, general_exp, dices):
    dice_exps = []
    for d, dice in enumerate(dices):
      dice_exp = dice.name
      if len(dice.modifiers) == 1:
        dice_exp += ' '+ re.sub(r'[\[\],\'\"e]', '', str(dice.modifiers)) + ' on every'
      elif len(dice.modifiers) > 1:
        dice_exp += ' '+ re.sub(r'[\[\],\'\"e]', '', str(dice.modifiers)) + ' each on every'
      dice_exps.append(dice_exp)
      
      output_gexp = re.sub(dice.name, 'dice('+str(d+1)+')', output_gexp, 1)    
    output_gexp = re.sub(regex.MODIFIER, '', output_gexp)
    operators = list(set(re.findall(regex.OPERATOR, output_gexp)))
    for op in operators:
      output_gexp = output_gexp.replace(op, ' '+op+' ')

    # editar: excluir isso depois de testar
    if self.playerQuote:
      self.output_msg = '@User, \"'+ self.playerQuote +'\"\n'
    else:
      self.output_msg = '@User,\n'
    self.output_msg += ' **'+ interpolation(general_exp.result) +'** '+ regex.ARROW_OP + 'Final Result\n'
    self.output_msg += regex.TEXT_BBOX +'arm\n'+ output_gexp +'\n'+ regex.TEXT_BBOX +'\n'
    for d, dice in enumerate(dices):
      self.output_msg += regex.TEXT_SBOX +' '+ interpolation(dice.total_sum) +' '+ regex.TEXT_SBOX
      if len(dice.modifiers) > 0:
        self.output_msg += regex.ARROW_OP + str([interpolation(result['modified']) for result in dice.results])
      self.output_msg += regex.ARROW_OP + str([result['natural'] for result in dice.results]) +'\n'
      self.output_msg += regex.TEXT_BBOX +'arm\n'+ dice_exps[d] +'\n'+ regex.TEXT_BBOX +'\n'

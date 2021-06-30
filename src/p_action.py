import re
import arith
from dconsts import DefaultConstants as const, TextStructures as txtst, DefaultRegexes as regex
from auxiliaries import interpolation

class PlayerAction:
  # calcula os resultados da rolagem de dados
  def compute (self, msgContent):
    decoded_msg = self.__decode_msg(msgContent)
    input_gexp = decoded_msg['expression']
    expression = arith.Expression(input_gexp, is_pattern=True)
    
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
        
        innerExpression.replace(innerDice.modifiers_address, innerDice.modifiers_raw)
        innerExpression.replace(innerExpression.inner_dice_match, innerDice.total_sum('modified'))
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
    
    actionResult = self.__build_result(decoded_msg, expression, dices)
    return actionResult

  # decodifica mensagem inserida pelo usuario
  def __decode_msg (self, msg_content:str) -> dict:
    player_quote = None
    
    # separa rolagem e mensagem embutida pelo jogador
    msgRaw = msg_content.split(' ', 1)
    input_gexp = msgRaw[0].lower()
    
    # salva mensagem embutida
    if len(msgRaw) > 1:
      quoteRaw = re.sub(r'^\s+', '', msgRaw[1]).split('\n', 1)[0]
      if len(quoteRaw) > 1:
        player_quote = quoteRaw
    
    decoded_msg = {'expression': input_gexp, 'quote': player_quote}
    return decoded_msg

  # estrutura a mensagem de saida
  def __build_result (self, decoded_msg:dict, general_exp:arith.Expression, dices:list) -> str:
    output_gexp = decoded_msg['expression']
    player_quote = decoded_msg['quote']
    
    # descricao dos valores extremos
    hires_desc = {
      const.NORMAL_RES: ' Highest',
      const.CRITICAL_RES: ' **Critical Strike**'}
    lores_desc = {
      const.NORMAL_RES: ' Lowest',
      const.CRITICAL_RES: ' **Critical Failure**'}

    # expressão de cada dado
    dice_exps = []
    for d, dice in enumerate(dices):
      dice_exp = dice.name
      if len(dice.modifiers) == 1:
        dice_exp += ' '+ re.sub(r'[\[\],\'\"e]', '', str(dice.modifiers)) + ' on every'
      elif len(dice.modifiers) > 1:
        dice_exp += ' '+ re.sub(r'[\[\],\'\"e]', '', str(dice.modifiers)) + ' each on every'
      dice_exps.append(dice_exp)

    # expressao geral
      output_gexp = re.sub(dice.name, 'dice('+str(d+1)+')', output_gexp, 1)    
    output_gexp = re.sub(regex.MODIFIER, '', output_gexp)
    operators = list(set(re.findall(regex.OPERATOR, output_gexp)))
    for op in operators:
      output_gexp = output_gexp.replace(op, ' '+op+' ')

    # editar: mover o codigo abaixo para classe AutoResponder
    # descricao da acao
    if player_quote:
      actionResult = '@User, \"'+ self.player_quote +'\"\n'
    else:
      actionResult = '@User,\n'
    
    # expressao geral e resultado da expressao geral
    actionResult += ' **'+ interpolation(general_exp.result) +'** '+ txtst.ARROW_OP + 'Final Result\n'
    actionResult += txtst.TEXT_BBOX +'arm\n'+ output_gexp +'\n'+ txtst.TEXT_BBOX +'\n'
    
    # resultados dos dados
    for d, dice in enumerate(dices):
      dice_has_modifiers = len(dice.modifiers) > 0

      # resultados modificados de cada dado
      if dice_has_modifiers:
        actionResult += txtst.TEXT_SBOX +' '+ interpolation(dice.total_sum('modified')) +' '+ txtst.TEXT_SBOX
        actionResult += txtst.ARROW_OP + str([interpolation(result['modified']) for result in dice.results]).replace('\'','') + '  Modified\n'
      
      # resultados naturais de cada dado
      actionResult += txtst.TEXT_SBOX +' '+ interpolation(dice.total_sum('natural')) +' '+ txtst.TEXT_SBOX
      actionResult += txtst.ARROW_OP + str([result['natural'] for result in dice.results])
      
      # valores extremos de cada dado
      hires_is_critical = (dice.hi_result['value'] == dice.faces)
      lores_is_critical = (dice.lo_result['value'] == 1)
      
      # valores extremos para rolagem unica
      if dice.amount == 1:
        if hires_is_critical:
          actionResult += ' '+ hires_desc[const.CRITICAL_RES] +'\n'
        elif lores_is_critical:
          actionResult += ' '+ lores_desc[const.CRITICAL_RES] +'\n'
        else:
          actionResult += '  Natural\n'
      
      # valores extremos para rolagem multipla
      else:
        actionResult += '  Natural\n'
        
        # valores maximos
        actionResult += txtst.TEXT_SBOX +' '
        if dice_has_modifiers:
          actionResult += interpolation(dice.hires_moded) +' | '
        actionResult += str(dice.hi_result['value']) +' '+ txtst.TEXT_SBOX + hires_desc[hires_is_critical]
        actionResult += ' ('+ str([result_i+1 for result_i in dice.hi_result['ids']])[1:-1] +')d\n'

        # valores minimos
        actionResult += txtst.TEXT_SBOX +' '
        if dice_has_modifiers:
          actionResult += interpolation(dice.lores_moded) +' | '
        actionResult += str(dice.lo_result['value']) +' '+ txtst.TEXT_SBOX + lores_desc[lores_is_critical]
        actionResult += ' ('+ str([result_i+1 for result_i in dice.lo_result['ids']])[1:-1] +')d\n'

      # expressao com modificadores de cada dado
      actionResult += txtst.TEXT_BBOX +'arm\n'+ dice_exps[d] +'\n'+ txtst.TEXT_BBOX +'\n'
    
    return actionResult

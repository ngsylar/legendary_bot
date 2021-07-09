import re
import copy
from arith.expression import Expression
from dconsts import DefaultConstants as const, TextStructures as txtop, DefaultRegexes as regex
from auxiliaries import floatstr, mincode, maxcode

class PlayerAction:
  # calcula os resultados da rolagem de dados
  def compute (self, msgContent):
    decoded_msg = self.__decode_msg(msgContent)
    input_gexp = decoded_msg['expression']
    expression = Expression(input_gexp, is_pattern=True)
    
    dices = []
    while expression.has_inner_expression():
      innerExpression = expression.inner_expression

      while innerExpression.has_dice():
        innerDice = innerExpression.inner_dice
        innerDice_sum = 0
        if innerDice.repetition:
          dice_repetition = int(innerDice.repetition)
        else:
          dice_repetition = 1
        
        for _ in range(dice_repetition):
          dice = copy.deepcopy(innerDice)
          dice.roll()
          
          while dice.get_modifier():
            modifier = dice.current_modifier
            if modifier.operator_is_mul():
              dice.modified.results = dice.results * modifier
            elif modifier.operator_is_div():
              dice.modified.results = dice.results / modifier
            elif modifier.operator_is_add():
              dice.modified.results = dice.results + modifier
            elif modifier.operator_is_sub():
              dice.modified.results = dice.results - modifier
          
          innerDice_sum += dice.modified.results_sum
          dice.restart_modifiers()
          dices.append(dice)
        innerExpression.replace(innerDice.address, innerDice_sum)
      
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
    
    encoded_result = self.__encode_result(decoded_msg, expression, dices)
    return encoded_result

  # decodifica mensagem inserida pelo usuario
  def __decode_msg (self, msg_content:str) -> dict:
    player_quote = None
    
    # separa acao e mensagem embutida pelo jogador
    msgRaw = msg_content.split(' ', 1)
    input_gexp = msgRaw[0].lower()
    if input_gexp[0] == '&':
      input_gexp = input_gexp[1:]

    # define comportamento da acao
    if input_gexp[0] == 'h':
      action_behavior = const.HIDDEN_ACTION
      input_gexp = input_gexp[1:]
    elif input_gexp[0] == 's':
      action_behavior = const.SECRET_ACTION
      input_gexp = input_gexp[1:]
    else:
      action_behavior = const.PUBLIC_ACTION
    
    # salva mensagem embutida
    if len(msgRaw) > 1:
      quoteRaw = re.sub(r'^\s+', '', msgRaw[1]).split('\n', 1)[0]
      if len(quoteRaw) > 1:
        player_quote = quoteRaw
    
    decoded_msg = {
      'behavior': action_behavior,
      'expression': input_gexp,
      'quote': player_quote,}
    return decoded_msg

  # estrutura a mensagem de saida
  def __encode_result (self, decoded_msg:dict, general_exp:Expression, dices:list) -> str:
    action_behavior = decoded_msg['behavior']
    output_gexp = decoded_msg['expression']
    player_quote = decoded_msg['quote']
    
    # descricao dos valores extremos
    hires_desc = {
      const.NORMAL_RES: 'Highest',
      const.CRITICAL_RES: '**Critical Strike**'}
    lores_desc = {
      const.NORMAL_RES: 'Lowest',
      const.CRITICAL_RES: '**Critical Failure**'}

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
    gexpResult = mincode(floatstr(general_exp.result)) + txtop.ARROW_OP
    output_gexp = output_gexp.replace('+-', '-').replace(',', '.')
    operators = list(set(re.findall(regex.OPERATOR, output_gexp)))
    for op in operators:
      output_gexp = output_gexp.replace(op, ' '+op+' ')
    actionResult = maxcode('arm', output_gexp) +'\n'
    
    # resultados dos dados
    for d, dice in enumerate(dices):
      dice_has_modifiers = len(dice.modifiers) > 0

      # resultados modificados de cada dado
      if dice_has_modifiers:
        actionResult += mincode(floatstr(dice.modified.results_sum)) + txtop.ARROW_OP
        if dice.amount > 1:
          actionResult += str([floatstr(result) for result in dice.modified.results]).replace('\'','') +'  '
        actionResult += 'Modified\n'
      
      # resultados naturais de cada dado
      actionResult += mincode(floatstr(dice.natural.results_sum)) + txtop.ARROW_OP
      if dice.amount > 1:
        actionResult += str([result for result in dice.natural.results]) +'  '
      
      # valores extremos de cada dado
      hires_is_critical = (dice.hi_result['value'] == dice.faces)
      lores_is_critical = (dice.lo_result['value'] == 1)
      
      # valores extremos para rolagem unica
      if dice.amount == 1:
        if hires_is_critical:
          actionResult += hires_desc[const.CRITICAL_RES] +'\n'
        elif lores_is_critical:
          actionResult += lores_desc[const.CRITICAL_RES] +'\n'
        else:
          actionResult += 'Natural\n'
      
      # valores extremos para rolagem multipla
      else:
        actionResult += 'Natural\n'
        
        # valores maximos
        actionResult += txtop.SBOX +' '
        if dice_has_modifiers:
          actionResult += floatstr(dice.hires_moded) +' | '
        actionResult += str(dice.hi_result['value']) +' '+ txtop.SBOX + txtop.ARROW_OP + hires_desc[hires_is_critical] +' ('+ str([result_i+1 for result_i in dice.hi_result['ids']])[1:-1] +')d\n'

        # valores minimos
        actionResult += txtop.SBOX +' '
        if dice_has_modifiers:
          actionResult += floatstr(dice.lores_moded) +' | '
        actionResult += str(dice.lo_result['value']) +' '+ txtop.SBOX + txtop.ARROW_OP + lores_desc[lores_is_critical] +' ('+ str([result_i+1 for result_i in dice.lo_result['ids']])[1:-1] +')d\n'

      # expressao com modificadores de cada dado
      actionResult += maxcode('arm', dice_exps[d]) +'\n'
    
    encoded_result = {
      'behavior': action_behavior,
      'value': gexpResult,
      'quote': player_quote,
      'description': actionResult}
    return encoded_result

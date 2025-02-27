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
          
          innerDice_sum += dice.modified.results_sum(dice.selection)
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

    # faz correcoes na mensagem para realizar acao
    selection_match = re.search(r'\d'+regex.SELEC_TYPE, input_gexp)
    while selection_match:
      input_gexp = input_gexp[:selection_match.start()+1]+'{'+selection_match[1]+selection_match[2]+'}'+input_gexp[selection_match.end():]
      selection_match = re.search(r'\d'+regex.SELEC_TYPE, input_gexp)
    
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
        actionResult += mincode(floatstr(dice.modified.results_sum(dice.selection))) + txtop.ARROW_OP
        if dice.amount > 1:
          mod_results = []
          for i, result in enumerate(dice.modified.results):
            resultStr = floatstr(result)
            result_is_critical = (dice.natural.results[i] == dice.faces) or (dice.natural.results[i] == 1)
            if result_is_critical:
              resultStr = '**'+resultStr+'**'
            result_was_cut = ((dice.selection['type'] == 'h') and (i >= dice.selection['amount'])) or ((dice.selection['type'] == 'l') and (i < (dice.amount - dice.selection['amount'])))
            if result_was_cut:
              resultStr = '~~'+resultStr+'~~'
            mod_results.append(resultStr)
          actionResult += str(mod_results).replace('\'','')+'  '
        actionResult += 'Modified\n'
      
      # resultados naturais de cada dado
      actionResult += mincode(floatstr(dice.natural.results_sum(dice.selection))) + txtop.ARROW_OP
      if dice.amount > 1:
        nat_results = []
        for i, result in enumerate(dice.natural.results):
          resultStr = str(result)
          result_is_critical = (result == dice.faces) or (result == 1)
          if result_is_critical:
            resultStr = '**'+resultStr+'**'
          result_was_cut = ((dice.selection['type'] == 'h') and (i >= dice.selection['amount'])) or ((dice.selection['type'] == 'l') and (i < (dice.amount - dice.selection['amount'])))
          if result_was_cut:
            resultStr = '~~'+resultStr+'~~'
          nat_results.append(resultStr)
        actionResult += str(nat_results).replace('\'','')+'  '
      
      # valores extremos de cada dado
      hires_is_critical = (dice.hi_nat_res == dice.faces)
      lores_is_critical = (dice.lo_nat_res == 1)
      if hires_is_critical and lores_is_critical:
        actionResult += '**Extreme Critical**\n'
      elif hires_is_critical:
        actionResult += '**Critical Strike**\n'
      elif lores_is_critical:
        actionResult += '**Critical Failure**\n'
      else:
        actionResult += 'Natural\n'

      # expressao com modificadores de cada dado
      actionResult += maxcode('arm', dice_exps[d]) +'\n'
    
    encoded_result = {
      'behavior': action_behavior,
      'value': gexpResult,
      'quote': player_quote,
      'description': actionResult}
    return encoded_result

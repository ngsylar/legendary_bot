class DefaultConstants:
  # valores de dados
  NORMAL_RES = False
  CRITICAL_RES = True

  # tipo de lancamento de dados
  PUBLIC_ACTION = 0
  SECRET_ACTION = 1
  HIDDEN_ACTION = 2

class TextStructures:
  # estruturas de texto
  BBOX = '\u0060\u0060\u0060'
  SBOX = '\u0060'

  # caracteres especiais
  CBLANK0 = '\u200b'
  CBLANK1 = '\u2800'

  # operadores
  ARROW_OP = ' \u27F5 '

class DefaultRegexes:
  # particoes de texto
  WHITE_SPACE = r'\s+'
  WORD_ENDING = r'\s*$'
  LINE_ENDING = r'(\s+.*\n?)?$'
  TEXT_ENDING = r'(\s+(.*\n*)*)?$'

  # expressoes aritmeticas
  OPERATOR = r'([\*\/\+\-])'
  FLOAT_VALUE = r'(\-?\d+(?:\.\d+)?)'
  ARITH_EXPRESSION = r'(?:\()([^()]+)(?:\))'
  VALIDATE_EXP = r'(?:[\*\/\+\-]\(|^\(+)([^()]+)(?:\))'

  # operacoes aritmeticas
  ARITH_MUL = FLOAT_VALUE +r'\*'+ FLOAT_VALUE + r'(?!e)'
  ARITH_DIV = FLOAT_VALUE +r'\/'+ FLOAT_VALUE + r'(?!e)'
  ARITH_ADD = FLOAT_VALUE +r'\+'+ FLOAT_VALUE + r'(?!e)'
  ARITH_SUB = FLOAT_VALUE +r'\-'+ FLOAT_VALUE + r'(?!e)'

  # nome dos dados
  RESULT_TYPE = r'(?:([!Nn]?[HhLl])(\d*))?'
  DICE = r'((\d+)'+ RESULT_TYPE +r'[Dd](\d+))'
  MULTIPLE_DICE = r'(?:(\d+)\#)?' + DICE

  # rolagem de dados
  JUST_MATH = r'^&[HhSs]?[\(\+\-\d]+'
  DICE_ROLL = r'[HhSs]?[\(\)\*\/\+\-\#\.,\d]*'+ DICE
  PLAYER_ACTION = r'('+ JUST_MATH +r'|'+ DICE_ROLL +r')'
  MODIFIER = r'('+ OPERATOR + FLOAT_VALUE +r')e'
  MODIFIERS_RAW = r'('+ MODIFIER +r')+'

  # operacoes com modificadores
  MODIFIER_MUL = r'\*'+ FLOAT_VALUE
  MODIFIER_DIV = r'\/'+ FLOAT_VALUE
  MODIFIER_ADD = r'\+'+ FLOAT_VALUE
  MODIFIER_SUB = r'\-'+ FLOAT_VALUE

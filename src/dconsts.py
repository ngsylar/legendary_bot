class DefaultConstants:
  # valores de dados
  NORMAL_RES = False
  CRITICAL_RES = True

class TextStructures:
  # estruturas de texto
  TEXT_BBOX = '\u0060\u0060\u0060'
  TEXT_SBOX = '\u0060'
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

  # operacoes aritmeticas
  ARITH_MUL = FLOAT_VALUE +r'\*'+ FLOAT_VALUE
  ARITH_DIV = FLOAT_VALUE +r'\/'+ FLOAT_VALUE
  ARITH_ADD = FLOAT_VALUE +r'\+'+ FLOAT_VALUE
  ARITH_SUB = FLOAT_VALUE +r'\-'+ FLOAT_VALUE

  # rolagem de dados
  DICE = r'(\d+[HhSs]?[Dd]\d+)'
  DICE_ROLL = r'[\(\)\*\/\+\-\d]*'+ DICE
  MODIFIER = OPERATOR +r'('+ FLOAT_VALUE +r'|(\([^e]+\)))(?i:(every|each|e))'
  MODIFIERS_RAW = r'(?:(?![\*\/\+\-]\-?\d+d).)*'

  # operacoes com modificadores
  MODIFIER_MUL = r'\*'+ FLOAT_VALUE +r'e'
  MODIFIER_DIV = r'\/'+ FLOAT_VALUE +r'e'
  MODIFIER_ADD = r'\+'+ FLOAT_VALUE +r'e'
  MODIFIER_SUB = r'\-'+ FLOAT_VALUE +r'e'

from dconsts import TextStructures as txtop

def floatstr (x:float) -> str:
  return '{0}'.format(str(round(x, 1) if x % 1 else int(x)))

def mincode (s:str) -> str:
  return txtop.SBOX +' '+ s +' '+ txtop.SBOX

def maxcode (lang:str, s:str) -> str:
  return txtop.BBOX + lang +'\n'+ s + txtop.BBOX

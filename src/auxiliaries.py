def floatstr (x:float) -> str:
  return '{0}'.format(str(round(x, 1) if x % 1 else int(x)))

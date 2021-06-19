# (?:(?!ab).)*
import re

roll = '-13-9+1d20+684-687e+684+2d8+7-3e+4e+1'

rolls = []

diceRegex = r'\d+[SsHh]?[Dd]\d+'
sumRegex = r'(?:(?![+\-]?\d+d).)*'

rolls.append(re.match(sumRegex, roll)[0])
rolls.extend(re.findall(r'[+\-]?\d+d'+sumRegex, roll))
rolls = list(filter(None, rolls))

print(rolls)

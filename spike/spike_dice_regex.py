import re

nameRegex = r'\d+[SsHh]?[Dd]\d+(([\+\-]\d+)+e?)?'
textRegex = r'(\s+(.*\n*)*)?$'
nameRegex += textRegex

dices = [
    '2d8',
    '2d20',
    '2d20+5',
    '2d20+51',
    '2d20-1+53-8+7+8+1-2',
    '2d20-1+53-8+7+8+1-2e',
    '2d20+5e',
    '2d20-1+5++8',
    '2d20e',
    '2d20fdfdj',
    '2d20 fdfdj',
    '2d20 fdfdj dyhjs   hkjd\n ajhdad jhdas\n\nashkbd\n hjds jha \njsha\n\n\n',
    '2d20-1e+53-8+7+8+1-2',]

for dice in dices:
    print(re.match(nameRegex, dice))

print(len(dices[11]))

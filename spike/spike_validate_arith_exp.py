import re

OPERATOR = r'([\*\/\+\-])'
ARITH_EXPRESSION = r'(?:\()([^()]+)(?:\))'
ARITH_EXP_VALIDATE = r'(?:[\*\/\+\-]\(|^\(+)([^()]+)(?:\))'

gexp = '((2+(1)))'
gexp = '(((1))+(2d20+(4(-1+1d4))e))'
print(gexp)
while re.search(ARITH_EXP_VALIDATE, gexp):
    coiso = re.search(ARITH_EXPRESSION, gexp)
    coisa = coiso[1]
    gexp = gexp[:coiso.start()]+coisa+gexp[coiso.end():]
    print(gexp)

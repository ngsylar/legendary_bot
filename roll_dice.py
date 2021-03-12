import random

def roll_dice(msg):

  # interpretar dados
  dices = []
  raw1 = msg.casefold().split('sd', 1)
  scope = int(raw1[0])
  if (scope < 1) or (scope > 100):
    raise ValueError
  raw2 = raw1[1].split('+', 1)
  dicelen = int(raw2[0])
  if (dicelen < 2) or (dicelen > 200):
    raise ValueError

  # lancar dados
  multi = 0
  for i in range(scope):
    value = random.randint(1, dicelen)
    if len(raw2) > 1:
      if raw2[1][-1].casefold() == 'e':
        multi = 1
        raw2[1] = raw2[1][:-1]
      dicesum = int(raw2[1])
    dices.append(value)

  # transcrever dados
  values = []
  valsum = 0
  d_name = raw1[0]+'d'+raw2[0]
  dmin = [0, 201]
  dmax = [0, 0]
  for dice in dices:

    # verificar valor min e maximo
    if dice < dmin[1]:
      dmin = [dices.index(dice), dice]
    elif dice > dmax[1]:
      dmax = [dices.index(dice), dice]
    #'\u00B0'

    # diferenciar dados (parte 1)
    if (len(raw2) > 1) and multi:
      # soma em cada dado (ataque)
      value = dice + dicesum
      values.append(value)
    else:
      # soma final (dano) ou sem soma
      value = dice
      values.append(value)
    valsum = valsum + value

  # diferenciar dados (parte 2)
  if len(raw2) > 1:
    # soma em cada dado (ataque)
    if multi:
      sum_desc = ' + '+str(dicesum)+' each'
    # soma final (dano)
    else:
      sum_desc = ' + '+str(dicesum)
      valsum = valsum + dicesum
  # sem soma
  else:
    sum_desc = ''

  # mostrar resultado
  sendmsg = '` '+str(valsum)+' `'+' \u27F5 '+str(values)+' '+d_name+sum_desc    
  return sendmsg
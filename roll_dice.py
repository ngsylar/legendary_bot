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
  dmin = ['Lowest', 999999, 0]
  dmax = ['Highest', -999999, 0]
  dice_i = 0
  for dice in dices:

    # guardar valores
    if (len(raw2) > 1) and multi:
      # soma em cada dado (ataque)
      value = dice + dicesum
      values.append(value)
    else:
      # soma final (dano) ou sem soma
      value = dice
      values.append(value)
    valsum = valsum + value

    # verificar valor min e maximo
    dice_i += 1
    if scope > 1:
      if value < dmin[1]:
        dmin = dmin[:2]
        dmin[1] = value
        dmin.append(dice_i)
        if dice == 1:
          dmin[0] = '**Critical Failure**'
      elif value == dmin[1]:
        dmin.append(dice_i)
      if value > dmax[1]:
        dmax = dmax[:2]
        dmax[1] = value
        dmax.append(dice_i)
        if dice == dicelen:
          dmax[0] = '**Critical Strike**'
      elif value == dmax[1]:
        dmax.append(dice_i)

  # diferenciar dados
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
  if scope > 1:
    sum_desc = sum_desc+'\n\u0060 '+str(dmin[1])+' \u0060 \u27F5 '+dmin[0]+' ('+str(dmin[2:])[1:-1]+')d\n\u0060 '+str(dmax[1])+' \u0060 \u27F5 '+dmax[0]+' ('+str(dmax[2:])[1:-1]+')d'
  sendmsg = '\u0060 '+str(valsum)+' \u0060'+' \u27F5 '+str(values)+' '+d_name+sum_desc
  return sendmsg

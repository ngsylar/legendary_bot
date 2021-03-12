import random

def roll_dice(msg):

  # interpretar dados (valores iniciais)
  dices = []
  multi = 0
  dicesum = 0

  # interpretar dados (numero de dados)
  raw1 = msg.split('d', 1)
  amount = int(raw1[0])
  if (amount < 1) or (amount > 100):
    raise ValueError

  # interpretar dados (valor maximo do dado)
  raw2 = raw1[1].replace('-','+-').split('+',1)
  dicelen = int(raw2[0])
  if (dicelen < 2) or (dicelen > 200):
    raise ValueError

  # interpretar dados (somas)
  if len(raw2) > 1:
    if raw2[1][-1].casefold() == 'e':
      multi = 1
      raw2[1] = raw2[1][:-1]
    d_sums = raw2[1].split('+')
    for d_sum in d_sums:
      dicesum += int(d_sum)

  # lancar dados
  for i in range(amount):
    value = random.randint(1, dicelen)
    dices.append(value)

  # transcrever dados (valores iniciais)
  values = []
  valsum = 0
  d_name = raw1[0]+'d'+raw2[0]
  dmin = [0, 999999, 0]
  dmax = [0, -999999, 0]
  dice_i = 0

  # transcrever dados (guardar valores)
  for dice in dices:
    if multi:
      # soma em cada dado (ataque)
      value = dice + dicesum
    else:
      # soma final (dano) ou sem soma
      value = dice
    values.append(value)
    valsum += value
    dice_i += 1

    # verificar menor valor alcancado
    if value < dmin[1]:
      dmin = dmin[:2]
      dmin[1] = value
      dmin.append(dice_i)
      if dice == 1:
        dmin[0] = 1
    elif value == dmin[1]:
      dmin.append(dice_i)

    # verificar maior valor alcancado
    if value > dmax[1]:
      dmax = dmax[:2]
      dmax[1] = value
      dmax.append(dice_i)
      if dice == dicelen:
        dmax[0] = 1
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
      valsum += dicesum
  # sem soma
  else:
    sum_desc = ''

  # mostrar resultado
  dmin_type = ['Lowest', '**Critical Failure**']
  dmax_type = ['Highest', '**Critical Strike**']
  if amount > 1:
    sum_desc = sum_desc+'\n\u0060 '+str(dmin[1])+' \u0060 \u27F5 '+dmin_type[dmin[0]]+' ('+str(dmin[2:])[1:-1]+')d\n\u0060 '+str(dmax[1])+' \u0060 \u27F5 '+dmax_type[dmax[0]]+' ('+str(dmax[2:])[1:-1]+')d'
  else:
    if dmin[0]:
      sum_desc = sum_desc+'\n'+dmin_type[dmin[0]]
    elif dmax[0]:
      sum_desc = sum_desc+'\n'+dmax_type[dmax[0]]
  sendmsg = '\u0060 '+str(valsum)+' \u0060'+' \u27F5 '+str(values)+'  '+d_name+sum_desc
  return sendmsg

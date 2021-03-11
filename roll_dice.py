import random

def roll_dice(msg):
  dices = []
  raw1 = msg.casefold().split('sd', 1)
  if int(raw1[0]) > 0:
    raw2 = raw1[1].split('+', 1)
    scope = int(raw1[0])
    multi = 0

    # lancar dados
    for i in range(scope):
      value = random.randint(1, int(raw2[0]))
      if len(raw2) > 1:
        if raw2[1][-1].casefold() == 'e':
          multi = 1
          raw2[1] = raw2[1][:-1]
        dicesum = int(raw2[1])
      dices.append(value)

  # dados somados
  if len(raw2) > 1:
    if multi:
      values = []
      valsum = 0
      for dice in dices:
        value = dice + dicesum
        values.append(value)
        valsum = valsum + value
      sendmsg = '` '+str(valsum)+' `'+' \u27F5 '+str(values)+' '+str(raw1[0])+'d'+str(raw2[0])+' + '+str(dicesum)+' each'

    # dados normais com soma final
    else:
      values = []
      valsum = 0
      for dice in dices:
        values.append(dice)
        valsum = valsum + dice
      valsum = valsum + dicesum
      sendmsg = '` '+str(valsum)+' `'+' \u27F5 '+str(values)+' '+str(raw1[0])+'d'+str(raw2[0])+' + '+str(dicesum)
  
  # dados normais
  else:
    values = []
    valsum = 0
    for dice in dices:
      values.append(dice)
      valsum = valsum + dice
    sendmsg = '` '+str(valsum)+' `'+' \u27F5 '+str(values)+' '+str(raw1[0])+'d'+str(raw2[0])
  
  return sendmsg
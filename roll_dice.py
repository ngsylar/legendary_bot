from collections import namedtuple
import random

class Dice:
  def __init__(self):
    self.__compute_ith_result = namedtuple('ithDiceResult', ['simple', 'compound'])

  # rolar dados
  def roll(self, msg):
    self.__decode_msg(msg)

    # faz o lancamento dos dados
    self.results = []
    for _ in range(self.amount):
      diceiResult = random.randint(1, self.faces)
      self.results.append(self.__compute_ith_result(
        simple = diceiResult,
        compound = diceiResult + self.sumTerm))
    
    # calcula a soma final dos dados lancados
    self.finalResult = 0
    if self.hasSum:
      if self.sumOverEach:
        for value in self.results:
          self.finalResult += value.compound
      else:
        for value in self.results:
          self.finalResult += value.simple
        self.finalResult += self.sumTerm

    # analisa e mostra resultados
    self.__find_extreme_vals()
    return self.__show_results()
  
  # interpreta mensagem inserida pelo usuario
  def __decode_msg(self, msg):
    # particiona mensagem
    self.raw = msg.split('d', 1)
    self.raw.extend(self.raw.pop().replace('-','+-').split('+',1))
    
    # atribui caracteristicas ao lancamento
    self.amount = int(self.raw[0])
    self.faces = int(self.raw[1])
    self.__validate_roll()
    self.hasSum = len(self.raw) > 2
    self.sumOverEach = (self.raw[2][-1].casefold() == 'e')

    # define valor da soma
    self.sumTerm = 0
    if self.hasSum:
      if self.sumOverEach:
        self.raw[2] = self.raw[2][:-1]
      sumFactors = self.raw[2].split('+')
      for sumFactor in sumFactors:
        self.sumTerm += int(sumFactor)

  # testa limites de lancamento
  def __validate_roll(self):
    if (self.amount < 1) or (self.amount > 100) or (self.faces < 2) or (self.faces > 200):
      raise ValueError
  
  # achar valores maximo e minimo da rolagem
  def __find_extreme_vals(self):
    self.highestResultIds = [0]
    self.lowestResultIds = [0]
    highestResult = -999999
    lowestResult = 999999

    for i, diceResult in enumerate(self.results):
      # define maior valor
      if diceResult.simple > highestResult:
        highestResult = diceResult.simple
        self.highestResultIds = [i]
      elif diceResult.simple == highestResult:
        self.highestResultIds.append(i)
      
      # define menor valor
      if diceResult.simple < lowestResult:
        lowestResult = diceResult.simple
        self.lowestResultIds = [i]
      elif diceResult.simple == lowestResult:
        self.lowestResultIds.append(i)
  
  # mostra o resultado da rolagem
  def __show_results(self):
    arrowSign = ' \u27F5 '
    negSign = ' \u2013 '
    posSign = ' + '

    # define o nome do dado:
    nameSufix = ''
    if self.hasSum and self.sumOverEach:
      nameSufix = ' each'
    if self.sumTerm < 0:
      sumDesc = negSign + str(self.sumTerm*(-1)) + nameSufix
    elif self.sumTerm > 0:
      sumDesc = posSign + str(self.sumTerm) + nameSufix
    self.name = str(self.amount)+'d'+str(self.faces) + sumDesc

    # define descricao dos valores maximo e minimo
    highestResultDescs = {False: 'Highest', True: '**Critical Strike**'}
    lowestResultDescs = {False: 'Lowest', True: '**Critical Failure**'}
    highestResult = self.results[self.highestResultIds[0]].simple
    lowestResult = self.results[self.lowestResultIds[0]].simple
    resultIsCS = highestResult == self.faces
    resultIsCF = lowestResult == 1
    hiResDesc = highestResultDescs[resultIsCS]
    loResDesc = lowestResultDescs[resultIsCF]
    
    # define descricao da rolagem
    rollDesc = ''
    if self.amount == 1:
      if resultIsCS:
        rollDesc = hiResDesc
      elif resultIsCF:
        rollDesc = loResDesc
    elif highestResult == lowestResult:
      if resultIsCS:
        rollDesc = '\u0060 '+str(highestResult)+' \u0060' + arrowSign + hiResDesc+' ('+str(self.highestResultIds)[1:-1]+')d'
      elif resultIsCF:
        rollDesc = '\u0060 '+str(lowestResult)+' \u0060'+ arrowSign + loResDesc+' ('+str(self.lowestResultIds)[1:-1]+')d'
    else:
      rollDesc = '\u0060 '+str(highestResult)+' \u0060'+ arrowSign + hiResDesc+' ('+str(self.highestResultIds)[1:-1]+')d\n\u0060 '+str(lowestResult)+' \u0060'+ arrowSign + loResDesc+' ('+str(self.lowestResultIds)[1:-1]+')d'
    
    # retorna resultados da rolagem
    diceResults = []
    if self.hasSum and self.sumOverEach:
      for diceResult in self.results:
        diceResults.append(diceResult.compound)
    else:
      for diceResult in self.results:
        diceResults.append(diceResult.simple)
    resultMsg = '\u0060 '+str(self.finalResult)+' \u0060'+ arrowSign + str(diceResults) + ' '+self.name +'\n'+ rollDesc

    return resultMsg

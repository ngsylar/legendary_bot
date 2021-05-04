import re
import random
from collections import namedtuple
from dice_roll_test_routine import DiceTest

class Dice:
  def __init__ (self):
    self.__compute_ith_result = namedtuple('ithDiceResult', ['simple', 'compound'])
    self.nameRegex = r'\d+[SsHh]?[Dd]\d+(([\+\-]\d+)+e?)?'

  # rolar dados
  def roll (self, msgContent):
    self.__decode_msg(msgContent)

    # faz o lancamento dos dados
    self.results = []
    for _ in range(self.amount):
      diceiResult = random.randint(1, self.faces)
      self.results.append(self.__compute_ith_result(
        simple = diceiResult,
        compound = diceiResult + self.sumTerm))

    # analisa e mostra resultados
    self.__compute_sum()
    self.__find_extreme_vals()
    self.__arrange_results()

  # rotina de testes de rolagem
  def roll_test (self):
    diceTest = DiceTest()
    testRoutine = diceTest.define_routine()
    
    testOutput = ''
    for dice_i in testRoutine:
      self.__decode_msg(dice_i.name)
      
      self.results = []
      for diceiResult in dice_i.results:
        self.results.append(self.__compute_ith_result(
          simple = diceiResult,
          compound = diceiResult + self.sumTerm))
      
      self.__compute_sum()
      self.__find_extreme_vals()
      self.__arrange_results()
      testOutput += self.rollResults + '\n\n'
    
    if diceTest.validate_response(testOutput):
      self.rollResults = testOutput + ':white_check_mark: Nailed it!'
    else:
      self.rollResults = testOutput + ':warning: WRONG! Wrong, wrong, wrong, wrong, wrong!'
  
  # decodifica mensagem inserida pelo usuario
  def __decode_msg (self, msgContent):
    # define o modo de rolagem
    self.isSecret = re.match(r'[0-9]+[Ss][Dd]', msgContent)
    self.isHidden = re.match(r'[0-9]+[Hh][Dd]', msgContent)
    
    # particiona mensagem
    msgRaw = msgContent.split(' ', 1)
    diceNameRaw = re.sub(r'[sh]', '', msgRaw[0].lower()).split('d', 1)
    diceNameRaw.extend(diceNameRaw.pop().replace('-','+-').split('+',1))
    
    # separa nome do dado da mensagem embutida pelo jogador
    self.playerQuote = None
    if len(msgRaw) > 1:
      quoteRaw = re.sub(r'^\s+', '', msgRaw[1]).split('\n', 1)[0]
      if len(quoteRaw) > 1:
        self.playerQuote = quoteRaw
    
    # atribui caracteristicas ao lancamento
    self.amount = int(diceNameRaw[0])
    self.faces = int(diceNameRaw[1])
    self.__validate_roll()
    self.hasSum = len(diceNameRaw) > 2
    if self.hasSum:
      self.hasSumOverEach = (diceNameRaw[2][-1].casefold() == 'e')
    else:
      self.hasSumOverEach = False

    # define valor da soma
    self.sumTerm = 0
    if self.hasSum:
      if self.hasSumOverEach:
        diceNameRaw[2] = diceNameRaw[2][:-1]
      sumFactors = diceNameRaw[2].split('+')
      for sumFactor in sumFactors:
        self.sumTerm += int(sumFactor)

  # testa limites de lancamento
  def __validate_roll (self):
    if (self.amount < 1) or (self.amount > 100) or (self.faces < 2) or (self.faces > 1000):
      raise ValueError

  # calcula a soma final dos dados lancados
  def __compute_sum (self):
    self.finalResult = 0
    if self.hasSumOverEach:
      for value in self.results:
        self.finalResult += value.compound
    else:
      for value in self.results:
        self.finalResult += value.simple
      self.finalResult += self.sumTerm
  
  # achar valores maximo e minimo da rolagem
  def __find_extreme_vals (self):
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
  def __arrange_results (self):
    arrowSign = ' \u27F5 '
    negSign = ' \u2013 '
    posSign = ' + '

    # define o nome do dado:
    sumDesc = ''
    diceNameSufix = ''
    if self.hasSumOverEach:
      diceNameSufix = ' each'
    if self.sumTerm < 0:
      sumDesc = negSign + str(self.sumTerm*(-1)) + diceNameSufix
    elif self.sumTerm > 0:
      sumDesc = posSign + str(self.sumTerm) + diceNameSufix
    self.name = str(self.amount)+'d'+str(self.faces) + sumDesc

    # define a estrutura da descricao dos valores maximo e minimo
    highestResultDescs = {False: 'Highest', True: '**Critical Strike**'}
    lowestResultDescs = {False: 'Lowest', True: '**Critical Failure**'}
    highestResult = self.results[self.highestResultIds[0]]
    lowestResult = self.results[self.lowestResultIds[0]]
    hasCriticalStrike = (highestResult.simple == self.faces)
    hasCriticalFailure = (lowestResult.simple == 1)
    hiResDesc = highestResultDescs[hasCriticalStrike]
    loResDesc = lowestResultDescs[hasCriticalFailure]
    hiResIds = ' ('+str([i+1 for i in self.highestResultIds])[1:-1]+')th'
    loResIds = ' ('+str([i+1 for i in self.lowestResultIds])[1:-1]+')th'
    
    # transcreve resultados maximo e minimo da rolagem
    diceResults = []
    if self.hasSumOverEach:
      hiResValue = '\u0060 '+str(highestResult.compound)+' \u0060'
      loResValue = '\u0060 '+str(lowestResult.compound)+' \u0060'
      for diceResult in self.results:
        diceResults.append(diceResult.compound)
    else:
      hiResValue = '\u0060 '+str(highestResult.simple)+' \u0060'
      loResValue = '\u0060 '+str(lowestResult.simple)+' \u0060'
      for diceResult in self.results:
        diceResults.append(diceResult.simple)
    
    # transcreve descricao dos valores maximo e minimo
    rollDesc = ''
    if self.amount == 1:
      if hasCriticalStrike:
        rollDesc = '\n' + hiResDesc
      elif hasCriticalFailure:
        rollDesc = '\n' + loResDesc
    elif highestResult == lowestResult:
      if hasCriticalStrike:
        rollDesc = '\n' + hiResValue + arrowSign + hiResDesc + hiResIds
      elif hasCriticalFailure:
        rollDesc = '\n' + loResValue + arrowSign + loResDesc + loResIds
    else:
      rollDesc = '\n' + hiResValue + arrowSign + hiResDesc + hiResIds + '\n' + loResValue + arrowSign + loResDesc + loResIds
    
    # retorna resultados da rolagem
    finalResult = '\u0060 '+str(self.finalResult)+' \u0060'
    self.rollResults = finalResult + arrowSign + str(diceResults) + ' ' + self.name + rollDesc

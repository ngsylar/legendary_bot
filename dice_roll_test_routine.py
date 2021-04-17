from collections import namedtuple

class DiceTest:
  def define_routine (self):
    diceProps = namedtuple('diceProperties', ['name', 'results'])

    testRoutine = [
      # teste para um dado
      diceProps(name = '1d8', results = [5]),
      diceProps(name = '1d8', results = [8]),
      diceProps(name = '1d8', results = [1]),

      # teste para um dado com soma ao final
      diceProps(name = '1d8+5', results = [5]),
      diceProps(name = '1d8+5', results = [8]),
      diceProps(name = '1d8+5', results = [1]),
        
      # teste para varios dados
      diceProps(name = '4d8', results = [4, 5, 4, 5]),
      diceProps(name = '4d8', results = [4, 8, 8, 5]),
      diceProps(name = '4d8', results = [4, 1, 1, 5]),
      diceProps(name = '4d8', results = [4, 8, 1, 5]),

      # teste para varios dados com soma ao final
      diceProps(name = '4d8+5', results = [4, 5, 4, 5]),
      diceProps(name = '4d8+5', results = [4, 8, 8, 5]),
      diceProps(name = '4d8+5', results = [4, 1, 1, 5]),
      diceProps(name = '4d8+5', results = [4, 8, 1, 5]),
        
      # teste para varios dados com soma em cada
      diceProps(name = '4d8+5e', results = [4, 5, 4, 5]),
      diceProps(name = '4d8+5e', results = [4, 8, 8, 5]),
      diceProps(name = '4d8+5e', results = [4, 1, 1, 5]),
      diceProps(name = '4d8+5e', results = [4, 8, 1, 5])]
      
    return testRoutine

  def validate_response (self, receivedMsg):
    # receivedMsg.replace('\u0060','\\u0060').replace('\u27F5','\\u27F5').replace('\u2013','\\u2013').replace('\u2013','\\u2013').replace('*','\\*')
    expectedMsg = '\u0060 5 \u0060 \u27F5 [5] 1d8\n\n\u0060 8 \u0060 \u27F5 [8] 1d8\n**Critical Strike**\n\n\u0060 1 \u0060 \u27F5 [1] 1d8\n**Critical Failure**\n\n\u0060 10 \u0060 \u27F5 [5] 1d8 + 5\n\n\u0060 13 \u0060 \u27F5 [8] 1d8 + 5\n**Critical Strike**\n\n\u0060 6 \u0060 \u27F5 [1] 1d8 + 5\n**Critical Failure**\n\n\u0060 18 \u0060 \u27F5 [4, 5, 4, 5] 4d8\n\u0060 5 \u0060 \u27F5 Highest (2, 4)th\n\u0060 4 \u0060 \u27F5 Lowest (1, 3)th\n\n\u0060 25 \u0060 \u27F5 [4, 8, 8, 5] 4d8\n\u0060 8 \u0060 \u27F5 **Critical Strike** (2, 3)th\n\u0060 4 \u0060 \u27F5 Lowest (1)th\n\n\u0060 11 \u0060 \u27F5 [4, 1, 1, 5] 4d8\n\u0060 5 \u0060 \u27F5 Highest (4)th\n\u0060 1 \u0060 \u27F5 **Critical Failure** (2, 3)th\n\n\u0060 18 \u0060 \u27F5 [4, 8, 1, 5] 4d8\n\u0060 8 \u0060 \u27F5 **Critical Strike** (2)th\n\u0060 1 \u0060 \u27F5 **Critical Failure** (3)th\n\n\u0060 23 \u0060 \u27F5 [4, 5, 4, 5] 4d8 + 5\n\u0060 5 \u0060 \u27F5 Highest (2, 4)th\n\u0060 4 \u0060 \u27F5 Lowest (1, 3)th\n\n\u0060 30 \u0060 \u27F5 [4, 8, 8, 5] 4d8 + 5\n\u0060 8 \u0060 \u27F5 **Critical Strike** (2, 3)th\n\u0060 4 \u0060 \u27F5 Lowest (1)th\n\n\u0060 16 \u0060 \u27F5 [4, 1, 1, 5] 4d8 + 5\n\u0060 5 \u0060 \u27F5 Highest (4)th\n\u0060 1 \u0060 \u27F5 **Critical Failure** (2, 3)th\n\n\u0060 23 \u0060 \u27F5 [4, 8, 1, 5] 4d8 + 5\n\u0060 8 \u0060 \u27F5 **Critical Strike** (2)th\n\u0060 1 \u0060 \u27F5 **Critical Failure** (3)th\n\n\u0060 38 \u0060 \u27F5 [9, 10, 9, 10] 4d8 + 5 each\n\u0060 10 \u0060 \u27F5 Highest (2, 4)th\n\u0060 9 \u0060 \u27F5 Lowest (1, 3)th\n\n\u0060 45 \u0060 \u27F5 [9, 13, 13, 10] 4d8 + 5 each\n\u0060 13 \u0060 \u27F5 **Critical Strike** (2, 3)th\n\u0060 9 \u0060 \u27F5 Lowest (1)th\n\n\u0060 31 \u0060 \u27F5 [9, 6, 6, 10] 4d8 + 5 each\n\u0060 10 \u0060 \u27F5 Highest (4)th\n\u0060 6 \u0060 \u27F5 **Critical Failure** (2, 3)th\n\n\u0060 38 \u0060 \u27F5 [9, 13, 6, 10] 4d8 + 5 each\n\u0060 13 \u0060 \u27F5 **Critical Strike** (2)th\n\u0060 6 \u0060 \u27F5 **Critical Failure** (3)th\n\n'

    if receivedMsg == expectedMsg:
      return True
    return False

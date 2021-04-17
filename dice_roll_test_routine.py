from collections import namedtuple

def define_test_routine ():
  diceProps = namedtuple('diceProperties', ['name', 'results'])

  testRoutine = [
    # teste para um dado
    diceProps(name = '1d8', results = ['5']),
    diceProps(name = '1d8', results = ['8']),
    diceProps(name = '1d8', results = ['1']),

    # teste para um dado com soma ao final
    diceProps(name = '1d8+5', results = ['5']),
    diceProps(name = '1d8+5', results = ['8']),
    diceProps(name = '1d8+5', results = ['1']),
      
    # teste para varios dados
    diceProps(name = '4d8', results = ['4','5','4','5']),
    diceProps(name = '4d8', results = ['4','8','8','5']),
    diceProps(name = '4d8', results = ['4','1','1','5']),
    diceProps(name = '4d8', results = ['4','8','1','5']),

    # teste para varios dados com soma ao final
    diceProps(name = '4d8+5', results = ['4','5','4','5']),
    diceProps(name = '4d8+5', results = ['4','8','8','5']),
    diceProps(name = '4d8+5', results = ['4','1','1','5']),
    diceProps(name = '4d8+5', results = ['4','8','1','5']),
      
    # teste para varios dados com soma em cada
    diceProps(name = '4d8+5e', results = ['4','5','4','5']),
    diceProps(name = '4d8+5e', results = ['4','8','8','5']),
    diceProps(name = '4d8+5e', results = ['4','1','1','5']),
    diceProps(name = '4d8+5e', results = ['4','8','1','5'])]
    
  return testRoutine

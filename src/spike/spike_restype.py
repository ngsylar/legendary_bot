import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from p_action import PlayerAction

# userInput = '4h3d4'
# userInput = '8d4+2e'

userInputs = [
    '1d8', '4d8', '4d8+2', '4d8+2e',
    '4d8h', '4d8h+2e',
    '4d8l', '4d8l+2e',
    '4d8!h', '4d8!h3',
    '4d6{nl}', '4d6nl3',
    '4d8h4', '4d8!h4',
    '4d8l4', '4d8nl4',
]

for userInput in userInputs:
    action = PlayerAction()
    result = action.compute(userInput)

    print(result['value'])
    print(result['description'])
    print('-------------------')

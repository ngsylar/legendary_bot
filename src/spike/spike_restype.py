import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from p_action import PlayerAction

# userInput = '4h3d4'
# userInput = '8d4+2e'

userInputs = [
    '1d8', '4d8', '4d8+2', '4d8+2e',
    # '4hd8', '4hd8+2e',
    # '4!ld8', '4nld8',
    # '4ld8', '4ld8+2e',
    # '4!hd8', '4nhd8',
    # '4h2d8', '4nl2d8',
    # '4l2d8', '4nh2d8',
    '4h2d8+2e']

for userInput in userInputs:
    action = PlayerAction()
    result = action.compute(userInput)

    print(result['value'])
    print(result['description'])
    print('-------------------')

import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from p_action import PlayerAction

userInput = '4h3d4'
userInput = '8d4+2e'

action = PlayerAction()
result = action.compute(userInput)

print(result['value'])
print(result['description'])

from randomstuff import *
import math
from builder import *
from activations import *
from evaluators import basic
from solvers import autodiff

''' Simplifying my code since I use these blocks a couple times... --------------------------------------------------------------------------------------------------- '''
def evaluate():
    # Re-evaluate the network...
    global infomap
    global inputs
    global action

    action = infomap.lookup[infomap.evaluator(infomap, inputs)]

def resetInputs():
    global inputs
    newi  = []
    for i in range(len(inputs)):
        newi.append(randrange(-100000, 100000) * 0.00001)
        while( (newi[i] <= (inputs[i] + 0.1) and newi[i] >= (inputs[i] - 0.1)) ):
            newi[i] = randrange(-100000, 100000) * 0.00001
        inputs[i] = newi[i]

def print_simple(obj):
    global target
    print(
    f"ID    ={obj.id} |-----------------\n"
    f"Input ={obj.inputs:.6f} |\n"
    f"Weight={obj.weights} |\n"
    f"Bias  ={obj.bias:.6f}\n"
    f"Output={obj.output:.6f} |\n"
    f"Target={target:.6f} |"
    )

''' ------------------------------------------------------------------------------------------------------------------------------------------------------------------ '''

''' Book keeping variables for all network values. I can simplify all my code by declaring and modifying these values. ----------------------------------------------- '''
infomap    = Network(activation=linear, evaluator=basic, solver=autodiff)
neuro      = infomap.lookup
inputs     = [] # Input data array. Values should represent meaningful context, but for now I'm just verifying functionality.
numInputs  = 1
numOutputs = 1
layers     = 0
layerWidth = 0

# Creating input values array for evaluation later.
#'''
for i in range(numInputs):
    value = 4.0#randrange(-100000, 100000) * 0.00001
    #while(value >= -0.00001 and value <= 0.00001):
    #    value = randrange(-100000, 100000) * 0.00001
    inputs.append(value)
#'''

''' ------------------------------------------------------------------------------------------------------------------------------------------------------------------ '''
# FINALLY START OF REAL TEST MAIN!!!

# Don't forget to redefine "actions" and "targets" inside your head. You were on something that felt important. Actions are a bridge between the mind and the world, or something. Restart there.
action  = None       # Output node of the network for each evaluation pass. I'll eventually use output nodes to drive external interaction later, so "action" is actually very appropriate.
target  = None       # "The Solution"! Really though the target is called that here because "it's the answer" to the input. There's... definitely more to explain here and I'm off somewhat. Later o/

# I'm sticking with dense transformers rn. I strongly disagree with my decision but whatever.
buildDense(infomap, numInputs, numOutputs, layers, layerWidth)
# In case I start losing my mind, v that will help me verify that my basic evaluator works.
#infomap.lookup[0].weights = {-1: 1.0}
#infomap.lookup[0].bias    = 0.5

infomap.resetCurrents()
choices = infomap.end # List of actions to choose from. An action is an endpoint in the network, the endpoints represent final reconstruction of input. Make sure it's clear!
target  = 2 * inputs[0]#choices[randrange(0, (len(choices) - 1))] if len(choices) > 1 else choices[0] if len(choices) == 1 else None

# Right now I'm trying to make sure that my descend function converges regardless of network structure. It fails with layers.
print(f"{'\033[94m'}Initial network values are: Target={target}\n{printrawnetwork(infomap)}")
evaluate()

loop = 1

while(True):

    # When choosing between outputs, descent needs to reinforce(?) good moves and weaken(?) bad moves...
    autodiff(action, target, network=infomap) # TODO Please make it so 'autodiff' is tied to the network object instead of passing the object as a parameter!
    #print(f"Network after descent:\n{printrawnetwork(neuro)}------------------------------------------------------------------------------------")
    evaluate() # MAKE SURE THIS IS DONE AFTER GRADIENT DESCENT AND BEFORE PRINTING!!! You have stared at incorrect numbers in your console too many fucking times now, GET IT TOGETHER!!

    print(f"loop={loop}")
    print_simple(action)
    print(f"---------------------------------------------")

    # Sometimes when I do my math wrong a weight/bias will blow up to infinity and break learning (and my cycler) completely. This is a stopping rule to break out any time that happens.
    if( not math.isfinite(action.output) ):
        loop = 999999
        print("Learning exploded!")
        break
    loop += 1

    if(loop > 100000):
        print("learning took too long!")
        break

    if(action.output > (target - (10 ** infomap.precision)) and action.output < (target + (10 ** infomap.precision))):
        break

    #print(f"{'\033[94m'}Actual choice was: {action.id} with an output of {action.output:.5f}, Target choice was: {target}\nNetwork before descent:\n{printrawnetwork(neuro)}\n--------")

print(f"{'\033[94m'}Finished after {'\033[92m'}{loop}{'\033[94m'} cycles! Network values are: Target={target}\n{printrawnetwork(infomap)}")

#printToDo()

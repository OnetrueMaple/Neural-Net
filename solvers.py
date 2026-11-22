from network import *
from reward import MSELoss

'''
# Attempting to fix my bugged autodiff function, this one aims to work with layers and branches in the n-net
def autodiff(action, target, network=None):
    # TODO Remake this for compatibility with more than 1 output node. Essentially, remove 'action' parameter and just iterate through all output nodes, totalling the error.
    if(not isinstance(network, Network)):
        print(f"\n{'\033[91m'}Pass only a network object into descend!\n")
        raise AttributeError
    if(not isinstance(action, Neuron)):
        # I should probably make this more informative and verify that it's actually at the end of a network. This is hardly a good safeguard tbh.
        print(f"\n{'\033[91m'}Pass only Neuron objects into action!\n")
        raise AttributeError
    if(not (action.id in network.end)):
        print(f"The passed 'action' needs to be the end of a network for autodiff!\n")
        raise KeyError
    # If we get here we should be good to go!

    # I need to start by zeroing the multiplier variable for each neuron. Arbitrary graph navigation requires applying losses once they're all calculated and dependencies are evil.
    for node in network.lookup:
        network.lookup[node].multipliers = [] # TODO REPLACE WITH 'network.lookup[node].multiplier = 0.0' !!

    error = MSELoss(action, target) # Store the error
    network.currents = [action.id]

    while(network.currents != []): # Iterate until the start of the network is reached
        #
#'''

''' START OF DEBUG FUNCTIONS! I know these work, so use these for verifying the whole functionality chain. ---------------------------------------------------------------- '''
def debugReward():
    global neuro
    global action
    global target

    reward = 2 * (action.output - target)
    return reward

#'''
def autodiff(action, target, network=None):
    if(not isinstance(network, Network)):
        print(f"\n{'\033[91m'}Pass only a network object into descend!\n")
        raise AttributeError
    if(not isinstance(action, Neuron)):
        # I should probably make this more informative and verify that it's actually at the end of a network. This is hardly a good safeguard tbh.
        print(f"\n{'\033[91m'}Pass only Neuron objects into action!\n")
        raise AttributeError
    # If we get here we should be good to go!

    # Add this value to each neuron's multipliers separately and don't carry it forward bc chain rule, so it gets der-ived last. Math, baby.
    # There's a chance I mess up the gradient calculation here. If reward includes the term I'm deriving w.r.t in weird ways then the process looks different. Be careful!
    error = MSELoss(action, target)  # Remember that you're deriving w.r.t the output value. If that value changes or represents something different enough this algorithm WILL NOT WORK!
    network.currents = [action.id]   # Should point to an output node, I think. Gradient descent starts from the end and works backwards to the start.
    prevSet = []

    learn_rate = network.learning_rate * (10 ** network.precision)

    while(network.currents != []):
        # Set up next layer of losses BASED ON LAST EVALUATION OUTPUT VALUE...
        for i in network.currents:
            # Copy the multipliers stored in each node "ahead" of the current node.
            for j in network.lookup[i].out:
                network.lookup[i].multiplier *= network.lookup[j].multiplier
                # Also copy the weight between node i and each outgoing node. (I could add the following to the line above for slight optimization, but it's negligible honestly.)
                network.lookup[i].multiplier *= network.lookup[j].weights[i]

            # Each node adds the negative activation multiplier from ReLU if that node's output was negative.
            if(network.lookup[i].output < 0):
                network.lookup[i].multiplier *= 0.1

        # Apply loss to each weight/bias in last visited layer now that I have pulled the values that led to previous output...
        for each in prevSet:
            value = error * network.lookup[each].multiplier

            # Biases are easy. Value alone is the correct modifier, I think.
            network.lookup[each].bias -= (value * learn_rate)

            # Weights are more annoying since I need to multiply the specific output that was passed through a weight.
            for w in network.lookup[each].inc:
                network.lookup[each].weights[w] -= ((value * network.lookup[w].output) * learn_rate)

            # Gotta reset these each time descent is applied or else there will be carry-over issues. None of that, please...
            network.lookup[each].multiplier = 1.0

        # This *should* be everything given my current loss function... haha sike. We doin rewards now. Good luck soldier o7

        prevSet = network.currents
        network.back()

    return None
#'''
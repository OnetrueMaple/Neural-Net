from network import *
from reward import MSELoss

# My current understanding is that 'loss' is used to describe the sitution where a decision fails to produce a specific outcome, or 'loses out' on a 'reward'.
#   I think that framing this as reorganizing from feedback (loss) is a much more generally applicable framing. Descend refers to the process of reorganizing 'deeper', but I'm not
#   a fan of that name for this process. Sounds... okay on paper. I'm still going over it though.
# How do you 'nudge' the loss function (change incentives)...? Pretty hard to do when the shit is just hardcoded here I can't lie. Manual rewrites are so frustrating...
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

            # Weights are more annoying since I need to multiply the specific output that was passed through a weight. Descent is already computationally expensive as it is...
            for w in network.lookup[each].inc:
                network.lookup[each].weights[w] -= ((value * network.lookup[w].output) * learn_rate)

            # Gotta reset these each time descent is applied or else there will be carry-over issues. None of that, please...
            network.lookup[each].multiplier = 1.0

        # This *should* be everything given my current loss function... haha sike. We doin rewards now. Good luck soldier o7

        prevSet = network.currents
        network.back()

    return None

''' START OF DEBUG FUNCTIONS! I know these work, so use these for verifying functionality for simpler shit. ---------------------------------------------------------------- '''
def debugReward():
    global neuro
    global action
    global target

    reward = 2 * (action.output - target)
    return reward

''' CURRENTLY DOES NOT HAVE PARITY WITH THE REWARDFN() IN MAIN!!! I'LL ALSO BE MOVING THAT CODE INTO SOLVER SOON, ONCE IT'S MOVED IT SHOULD BE STATELESS!! '''
# Putting this here for now. MAKE SURE TO MAINTAIN PARITY BETWEEN THIS AND descend()!!
# I need to make a file specifically for descent, or whatever I'm gonna call this process. It's hard to put a good name to, especially since I'm trying to avoid industry-standard terms.
def debugDescend():
    # I'll write the multipliers to each node and print it out each time. They'll match what's in my notebook eventually...
    global neuro
    global action
    global target

    # Add this value to each neuron's multipliers separately and don't carry it forward bc chain rule, so it gets der-ived last. Math, baby.
    # There's a chance I mess up the gradient calculation here. If reward includes the term I'm deriving w.r.t in weird ways then the process looks different. Be careful!
    error = 2 * (action.output - target) # Remember that you're deriving w.r.t the output value. If that value changes or represents something different enough this algorithm WILL NOT WORK!
    neuro.currents = [action.id]
    prevSet = []

    # Start collecting those multipliers girl!
    while(neuro.currents != []):
        # Set up next layer of losses BASED ON LAST EVALUATION OUTPUT VALUE...
        for i in neuro.currents:
            # Copy the multipliers stored in each node "ahead" of the current node.
            for j in neuro.lookup[i].out:
                for k in neuro.lookup[j].multipliers:
                    neuro.lookup[i].multipliers.append(k)
                neuro.lookup[i].multipliers.append(neuro.lookup[j].weights[i]) # Copy the weight between node i and each outgoing node.

            # Each node adds the negative activation multiplier from ReLU if that node's output was negative.
            if(neuro.lookup[i].output < 0):
                neuro.lookup[i].multipliers.append(0.03)

        # Apply loss to each weight/bias in last visited layer now that I have pulled the values that led to previous output...
        for l in prevSet:
            value = error
            # Multiply all the multipliers for each node and error, because chain rule.
            for m in neuro.lookup[l].multipliers:
                value *= m

            # Biases are easy. Value alone is the correct modifier, I think.
            neuro.lookup[l].bias -= (value * learning_rate)

            # Weights are more annoying since I need to multiply the specific output that was passed through a weight. This operation is already expensive enough as it is...
            for m in neuro.lookup[l].inc:
                neuro.lookup[l].weights[m] -= ((value * neuro.lookup[m].output) * learning_rate)

            # Gotta reset these each time the function is called or else I'll get issues
            neuro.lookup[l].multipliers = []

        # This *should* be everything given my current loss function... haha sike. We doin rewards now. Good luck soldier o7

        prevSet = neuro.currents
        neuro.back()

    return None

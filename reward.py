''' LOSS FUNCTION = (output - target) ^ 2 (This is how we measure "how wrong" the network was... what is "smart" if not the right set of tools applied over and over again?)'''
def MSELoss(action, target):
    temp = target
    #if(action.id == target): # Force target node to converge towards 1.0
    #    temp = 1.0
    #else:                    # Force non-target nodes to converge towards 0.0
    #    temp = 0.0

    # Taking the derivative of the loss function since I'm feeding this directly into error.
    reward = 2 * (action.output - temp)
    return reward   # I need to return something for the network to reorganize around.

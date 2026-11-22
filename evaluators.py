from network import *

def basic(obj, context):
    # Checking for passed parameter compatibility...
    if(not isinstance(obj, Network)):
        print(f"Wrong object type passed into obj! Got a {type(obj)} instead of a Network!")
        raise ValueError
    if(not isinstance(context, list)):
        print(f"Wrong datatype passed into context. Got a {type(context)} instead of a list of floats and/or ints.")
        raise ValueError
    if(len(context) != len(obj.start)):
        print(f"List passed into context doesn't match the length of inputs. Expected {len(obj.start)} items, got {len(context)} instead.")
        raise ValueError
    for i in range(len(context)):
        if(not isinstance(context[i], float) and not isinstance(context[i], int)):
            print(f"Wrong datatype passed into context list. Got {type(context[i])} instead of a float or int.")
            raise ValueError
        obj.lookup[-(i + 1)].output = context[i] # Automatically assumes context data is ordered to what the starting nodes expect. This isn't necessarily the case, yknow!

    # If the code gets here, the passed input list is compatible. Passing inputs all the way through network...
    obj.resetCurrents()
    obj.frwd()
    while(obj.currents != []):
        for i in obj.currents:
            obj.lookup[i].inputs = 0.0
            for j in obj.lookup[i].inc:
                obj.lookup[i].inputs += obj.lookup[j].output * obj.lookup[i].weights[j]
            obj.lookup[i].output = obj.activation((obj.lookup[i].inputs + obj.lookup[i].bias))
        obj.frwd()

    # This should pick the highest OUTPUT VALUE between all output nodes.
    if (len(obj.end) > 0):
        choice = obj.lookup[obj.end[0]]
        for i in obj.end:
            if(choice.output < obj.lookup[i].output):
                choice = obj.lookup[i]
        return choice.id
    else:
        return None

from neuron import *

class Network:

    depthLimit = 50 # Helps find/break infinite cycles in graphs. 50 tends to be about the limit of what my current pc can handle within a couple minutes of large networks.
    restartOnEnd = False

    # Avoid declaring variables outside of init/functions, they're "global" variables for *every* instance of a class. Changing it once typically
    #   means that you change it for every instance unless the same variable is redeclared inside init. Be careful!

    def __init__(self, activation=None, evaluator=None, solver=None):

        # Adding this because it's good for organizing my things.
        self.modelID      = ""

        # Version number, used for checking whether or not code should work without issues.
        self.version      = 0.3

        # Activation function, the mathematical function determining how neurons handle inputs.
        self.activation   = activation if activation is not None else None          # I can't save actual python functions into files, so it has to be imported.

        # Evaluation function, determines how to navigate through a network from inputs all the way to the end.
        self.evaluator    = evaluator if evaluator is not None else None            # I can't save actual python functions into files, so it has to be imported.

        # Solver function, the way a network's values should change to better fit desired outputs.
        self.solver       = solver if solver is not None else None                  # I can't save actual python functions into files, so it has to be imported.

        # Lookup table of all Node objects. Can be managed thru files instead to save massive RAM overhead. (don't do that unless you're okay with destroying an SSD/HDD)
        self.lookup       = {}

        self.start        = [] # Set of starting points, set() of ids
        self.end          = [] # Set of ending points, set() of ids
        self.currents     = [] # Current nodes, set() of ids
        self.currentDepth = 0

        # These values together could find an "optimal step amount" depending on how far an estimated solution is from the current position.
        #   If implemented right, this idea that a network can guess a solution *should* fix some of the large variety in solution computation.
        self.base_precision     = -3                                       # This number corresponds to the decimal place where accuracy is checked.
        self.base_modifier      = 0                                        # This number nudges the accuracy check up or down.
        self.precision          = self.base_precision - self.base_modifier # Actual precision value, values represent decimal places. learning_rate value (12) set to work for 2pp by default.
        self.learning_rate      = 12                                       # How far the network should try to move away from the current position.
        # multiply learning_rate by (10 ^ precision) for use inside gradient descent! Most of these are derivable values.

    def resetCurrents(self):
        self.currentDepth = 0
        if(self.lookup != {}):
            self.start = findStarts(self.lookup)
            self.end   = findEnds(self.lookup)
        self.currents = self.start
        return None

    def recalcPrecision(self): # Unused for now...???? Supposed to help me while I figure out how long I'm willing to wait for a network to learn some thing.
        self.precision = self.base_precision - self.base_modifier

    def frwd(self): # Breadth first search, changes current to the next set of nodes based on what's inside current. If empty, does nothing or restarts.
        temp = set() # Builds next set of "currents"
        next = []

        if(self.currentDepth >= self.depthLimit):      # Break traversal if exceeding the depth limit. Currently my only workaround for graphs with loops.
            print("Depth limit reached!")
            ''' I removed 'self.currents = []' because I think that if traversal breaks it's more helpful to know where than to be left guessing. '''
            return None

        # Finds all connections in currents, then adds them to temporary set to remove duplicates
        for i in self.currents:
            for j in range(len(self.lookup[i].out)):
                if (self.lookup[i].out[j] == []):
                    continue
                else:
                    temp.add(self.lookup[i].out[j])
        if (len(temp) == 0 and self.restartOnEnd):    # If there are no connections to follow (indicated by no additions to temp) add every starting index to next
            self.resetCurrents()
            self.currentDepth = 0
            return None                               # Break from the function if restarting, otherwise next will be empty and looping behavior fails
        else:                                         # Add all unique output nodes found to next
            for i in temp:
                next.append(i)
        self.currents = next
        self.currentDepth += 1
        return None

    def back(self):
        temp = set() # Builds next set of "currents"
        next = []

        if(self.currentDepth >= self.depthLimit):      # Break traversal if exceeding the depth limit. Currently my only workaround for graphs with loops.
            print("Depth limit reached!")
            ''' I removed 'self.currents = []' because I think that if traversal breaks it's more helpful to know where than to be left guessing. '''
            return None

        # Finds all connections in currents, then adds them to temporary set to remove duplicates
        for i in self.currents:
            for j in range(len(self.lookup[i].inc)):
                if (self.lookup[i].inc[j] == []):
                    continue
                else:
                    temp.add(self.lookup[i].inc[j])
        if (len(temp) == 0 and self.restartOnEnd):    # If there are no connections to follow (indicated by no additions to temp) add every starting index to next
            self.resetCurrents()
            self.currentDepth = 0
            return None                               # Break from the function if restarting, otherwise next will be empty and looping behavior fails
        else:                                         # Add all unique output nodes found to next
            for i in temp:
                next.append(i)

        self.currents = next
        self.currentDepth += 1
        return None

'''

BASE CLASS FUNCTIONS...

THE ONLY TWO FUNCTIONS HERE SEEM TO BE MORE USEFUL FOR BUILDING NETWORKS THAN FOR THE ACTUAL NN OBJECT ITSELF.

'''

# Returns a list of starting points inside a passed lookup array.
def findStarts(lookup):
    if lookup is None:
        return None

    ''' Old code that searches for nodes with empty input sets as the signal for starting points. My new rule is that negative IDs signal which nodes are used as inputs for data.
    temp = []
    for i in lookup:
        if (lookup[i].inc == [] and lookup[i].out != []): # If a network has sub-networks isolated from the "main" one, this function doesn't differentiate those!
            temp.append(lookup[i].id)
    '''
    temp = []

    for i in lookup:
        if (lookup[i].id < 0):
            temp.append(lookup[i].id)

    return temp

# Returns a list of end points inside a passed lookup array.
def findEnds(lookup):
    if lookup is None:
        return None

    temp = []
    for i in lookup:
        if (lookup[i].out == [] and lookup[i].inc != []): # If a network has sub-networks isolated from the "main" one, this function doesn't differentiate those!
            temp.append(lookup[i].id)

    return temp

''' --------------------------------------------------------------------------------------------------------------------------------------------------------------------- '''
def printrawnetwork(network): # I should like to GRAPHICALLY see a network layout, actually. The text is fine if I don't care about ease of use, but text output really sucks to sort through.
    whitespace = 15
    data  = network.__dict__
    strin = "\033[97m"
    for key in data:
        if(key == 'lookup'):
            ids = []
            for node in data['lookup']:
                ids.append(node)
            strin += f"node ids       = {ids}\n"
        else:
            temp = f"{key} "
            while(len(temp) < whitespace):
                temp += " "
            strin += f"{temp}= {data[key]}\n"
    for node in network.lookup:
        strin += f"node_data={neuron_format(network.lookup[node])}\n"
    return f"{strin[:-1]}{'\033[94m'}"

def map_attributes(obj): # This function is used for saving a network object.

    if isinstance(obj, Network):
        data = {}
        data["version"]        = obj.version
        data["modelID"]        = obj.modelID
        data["nodes"]          = len(obj.lookup) # This allows me to guess a filesize and also to enforce data-retreival limits.
        data["base_precision"] = obj.base_precision
        data["learning_rate"]  = obj.learning_rate

        # THIS HAS TO BE LAST! It's the largest part of the file and the easiest place to mess with the data to trick my program into breaking.
        # Matter of fact, actually... don't even include it here. Write it into a file from the save function because RAM usage doubles to store a duplicate.
        #data["lookup"] = obj.lookup

        # I will not include these values for the stated reasons.
        #data["base_modifier"] = obj.base_modifier  # <---- this gets modified according to learning needs by the program. Since it's a contexually derived value, don't save.
        #data["precision"]     = obj.precision      # Same as ^, but it's the final modifier for learning rate.
        return data
    raise TypeError(f'Cannot serialize object of {type(obj)}')

def nav_attributes(obj):
    if isinstance(obj, Network):
        data = {}
        data["start"] = obj.start
        data["end"]   = obj.end

        return data
    raise TypeError(f"Cannot serialize object of {type(obj)}")

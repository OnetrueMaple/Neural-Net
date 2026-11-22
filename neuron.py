class Neuron:

    def __init__(self, id=None, out=None, inc=None, weights=None, bias=None, inputs=None, output=None):
        self.id = id if id is not None else 0       # Might remove this. IDs are already being used in the lookup for navigation and making sense of the data.
        self.out = out if out is not None else []   # Outgoing IDs
        self.inc = inc if inc is not None else []   # Incoming IDs

        self.weights = weights if weights is not None else {}
        self.bias = bias if bias is not None else 0.0
        self.inputs = 0.0
        self.output = 0.0

        # Don't forget that multiplier is used for gradient calculation but isn't saved to files!
        self.multiplier = 1.0

        # Debug value for comparing passed multipliers during gradient calculation.
        #self.multipliers = []

''' DATA RETREIVAL / PRINTING FUNCTIONS '''

def neuron_format(obj): # I want this to have configurable precision. Hardware data stops being accurate at a particular point. Not sure about my machine yet.
    if isinstance(obj, Neuron):
        data = {}
        data["id"]      = obj.id
        data["out"]     = obj.out
        data["inc"]     = obj.inc
        data["inputs"]  = float( f"{obj.inputs:.5f}" )
        data["output"]  = float( f"{obj.output:.5f}" )
        data["weights"] = obj.weights
        data["bias"]    = float( f"{obj.bias:.5f}" )
        #data["multis"]  = obj.multiplier
        return data
    raise TypeError(f'Cannot serialize object of {type(obj)}')

def node_attributes(obj): # Saving and Loading uses this function. Don't change it!
    # I'm currently looking at each node costing ~90 bytes before connections. Holy storage! Uh, good enough for testing my code at small scales I guess?
    #    I can instead store data in a sequence between lines or between byte chunks to save all that char space.
    if isinstance(obj, Neuron):
        data = {}
        data["id"]      = obj.id
        data["out"]     = obj.out
        data["inc"]     = obj.inc
        data["weights"] = obj.weights
        data["bias"]    = obj.bias
        data["inputs"]  = obj.inputs
        data["output"]  = obj.output
        return data
    raise TypeError(f'Cannot serialize object of {type(obj)}')
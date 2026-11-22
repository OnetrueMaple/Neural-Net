import sys
from traceback import print_tb
sys.path.insert(0, "../")
from builder import *
from time import perf_counter
from random import random

start = perf_counter()
end   = 0

def exception_handler(exception_type, exception, traceback):
    if (exception_type.__name__ == "AssertionError"): # My own assertion failures should give suitable information.
        end = perf_counter() - start
        print(f"{'\033[95m'}Completion time: {'\033[96m'}{end:.6f}s")
    else:                                             # Otherwise, I'd actually like the full stack trace as well as total program uptime.
        print(f"\n{'\033[91m'}------------------------------------------------------------------------------{'\033[0m'}")
        print_tb(traceback)
        print(f"{'\033[91m'}{exception_type.__name__}:{'\033[95m'} {exception}")
        end = perf_counter() - start
        print(f"{'\033[92m'}Completion time: {'\033[94m'}{end:.6f}s")
sys.excepthook = exception_handler

def test_building():
    print(f"{'\033[94m'}Going over all info map building functionalities...{'\033[0m'}")

    #''' Node Test ---------------------------------------------------------------------------------------------------------------------------------------- '''
    print(f"{'\033[94m'}Checking node fields...{'\033[0m'}")
    testNode   = Neuron()
    expected   = {'id': 0, 'out': [], 'inc': [], 'inputs': 0.0, 'output': 0.0, 'weights': {}, 'bias': 0.0, 'multiplier': 1.0}
    actual     = testNode.__dict__
    differences= {}
    ignore     = {} # In case keys from expected are missing from actual, I can ignore specific keys to avoid the key error.

    # Checks to make sure the correct parameters show up inside a new, uninitialized object. Differences will be noted and passed with an error!
    # Collect missing, extra, and invalid fields.
    for key in actual:
        if key not in expected:
            differences[key] = actual[key]
    for key in expected:
        if key not in actual and key not in differences:
            differences[key] = expected[key]
            ignore[key]     = True
    # Checks to make sure each value inside of the new uninitialized object matches the expected value. Differences will be noted and passed with an error!
    for key in expected:
        if key not in ignore:
            if(expected[key] != actual[key]):
                differences[key] = actual[key]
    # Print all differences along with source of error! ...implicitly checks for type matching this time.
    if(len(differences) != 0):
        print(f"{'\033[91m'}FAILED!{'\033[94m'} Found {'\033[95m'}{len(differences)}{'\033[94m'} differences between expected values and actual values. See below:{'\033[0m'}")
        for key in differences:
            if key not in actual:
                print(f"{'\033[93m'}\'{key}\'{'\033[94m'} is missing from object!{'\033[0m'}")
            elif key not in expected:
                print(f"{'\033[93m'}\'{key}\'{'\033[94m'} is not in expected values!{'\033[0m'}")
            else:
                print(f"{'\033[93m'}\'{key}\'{'\033[94m'} is {'\033[95m'}{actual[key]}{'\033[94m'}, expected was {'\033[95m'}{expected[key]}{'\033[94m'}!{'\033[0m'}")
        raise AssertionError

    print(f"{'\033[92m'}PASSED!{'\033[0m'}")
    #''' Network Test ------------------------------------------------------------------------------------------------------------------------------------- '''
    print(f"{'\033[94m'}Checking network fields, version 0.3{'\033[0m'}") # Hardcoded ver number because this test should be EXPLICITLY CLEAR what the test is comparing against.
    testN      = Network() # I'll operate on this node lookup to make sure the rest of the functions actually work as intended.
    nmap       = testN.lookup
    expected   = {'version': 0.3, 'modelID': '', 'activation': None, "evaluator": None, "solver": None, 'lookup': {}, 'start': [], 'end': [], 'currents': [], 'currentDepth': 0, 'base_precision': -3, 'base_modifier': 0, 'precision': -2, 'learning_rate': 12}
    actual     = testN.__dict__
    differences= {}
    ignore     = {} # In case keys from expected are missing from actual, I can ignore specific keys to avoid the key error.

    # Checks to make sure the correct parameters show up inside a new, uninitialized object. Differences will be noted and passed with an error!
    # Collect missing, extra, and invalid fields.
    for key in actual:
        if key not in expected:
            differences[key] = actual[key]
    for key in expected:
        if key not in actual and key not in differences:
            differences[key] = expected[key]
            ignore[key]     = True
    # Checks to make sure each value inside of the new uninitialized object matches the expected value. Differences will be noted and passed with an error!
    for key in expected:
        if key not in ignore:
            if(expected[key] != actual[key]):
                differences[key] = actual[key]
    # Print all differences along with source of error! ...implicitly checks for type matching this time.
    if(len(differences) != 0):
        print(f"{'\033[91m'}FAILED!{'\033[94m'} Found {'\033[95m'}{len(differences)}{'\033[94m'} differences between expected values and actual values. See below:{'\033[0m'}")
        for key in differences:
            if key not in actual:
                print(f"{'\033[93m'}\'{key}\'{'\033[94m'} is missing from object!{'\033[0m'}")
            elif key not in expected:
                print(f"{'\033[93m'}\'{key}\'{'\033[94m'} is not in expected keys!{'\033[0m'}")
            else:
                print(f"{'\033[93m'}\'{key}\'{'\033[94m'} is {'\033[95m'}{actual[key]}{'\033[94m'}, expected was {'\033[95m'}{expected[key]}{'\033[94m'}!{'\033[0m'}")
        raise AssertionError

    print(f"{'\033[92m'}PASSED!{'\033[0m'}")
    testN.modelID = "testN" # Setting this for later...
    #''' Basic Building Functions -------------------------------------------------------------------------------------------------------------------------------------------------- '''
    print(f"{'\033[94m'}Going over build functions...{'\033[0m'}")

    # Making sure I can create individual nodes inside maps.
    print(f"{'\033[94m'}Testing node creation...")

    # I'll only say this once, but it's true of my testing methodology as a whole so I should make it clear. Comparing against a dictionary generated by my functions necessarily
    #   means that any updates to the fields of these objects means I need to rewrite most of my testing code. It's also not an effective way to make sure that my code is conceptually
    #   accomplishing what it should. For foundational pieces I think this is fine, but it will bite me in the ass if I use this strategy for the more abstract problems. For example,
    #   solver-class problems will be *very* hard to validate behavior for if I attempt to use a sample run I've generated in the past as the success metric like I am now.
    #   Once I verify behavior for these foundational pieces, testing should be more about checking what's possible (or impossible!) to build rather than "is this value correct".
    expectedN   = [{'id': 1, 'out': [], 'inc': [], 'inputs': 0.0, 'output': 0.0, 'weights': {}, 'bias': 0.0}]
    valid_struc = True
    touch(testN, 1)

    #       These failures prevent value comparison, checking these first.
    if(len(nmap) == 0):
        print(f"{'\033[91m'}FAILED!{'\033[94m'} touch() failed to interact with network lookup!{'\033[0m'}")
        raise AssertionError
    elif(len(nmap) != 1):
        print(f"{'\033[91m'}FAILED!{'\033[94m'} touch() created too many entries!{'\033[0m'}")
        raise AssertionError
    for key in nmap:
        valid_key = True if isinstance(key, int) else False
        valid_obj = True if isinstance(nmap[key], Neuron) else False
        if(not valid_key and valid_obj):
            print(f"{'\033[91m'}FAILED!{'\033[94m'} touch() created an object with the wrong key type! Expected {'\033[95m'}int{'\033[94m'}, got {'\033[95m'}{type(key)}{'\033[94m'}!{'\033[0m'}")
        elif(valid_key and not valid_obj):
            print(f"{'\033[91m'}FAILED!{'\033[94m'} touch() created the wrong object! Expected {'\033[95m'}Neuron{'\033[94m'}, got {'\033[95m'}{type(nmap[key])}{'\033[94m'}!{'\033[0m'}")
        elif(not valid_key and not valid_obj):
            print(f"{'\033[91m'}FAILED!{'\033[94m'} touch() created an incorrect key and the wrong object! Expected {'\033[95m'}" + "{int: <Neuron>}" + f"{'\033[94m'}, got {'\033[95m'}" "{" f"{type(key)}: {type(nmap[key])}" + "}" + f"{'\033[94m'}!")
        if(not valid_key or not valid_obj):
            raise AssertionError
    #       Checking to make sure that touch assigns only the correct values.
    for node in nmap:
        ndata = neuron_format(nmap[node])
        if(ndata != expectedN[0]):
            if(ndata['id'] != expectedN[0]['id']):
                nid   = ndata['id']
                exid  = expectedN[0]['id']
                print(f"{'\033[91m'}FAILED!{'\033[94m'} IDs don\'t match! Expected {'\033[95m'}{exid}{'\033[94m'}, got {'\033[95m'}{nid}{'\033[94m'}!")
                valid_struc = False
            if(ndata['out'] != expectedN[0]['out']):
                nout   = ndata['out']
                exout  = expectedN[0]['out']
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Outs don\'t match! Expected {'\033[95m'}{exout}{'\033[94m'}, got {'\033[95m'}{nout}{'\033[94m'}!")
                valid_struc = False
            if(ndata['inc'] != expectedN[0]['inc']):
                ninc   = ndata['inc']
                exinc  = expectedN[0]['inc']
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Incs don\'t match! Expected {'\033[95m'}{exinc}{'\033[94m'}, got {'\033[95m'}{ninc}{'\033[94m'}!")
                valid_struc = False
            if(ndata['inputs'] != expectedN[0]['inputs']):
                ninputs   = ndata['inputs']
                exinputs  = expectedN[0]['inputs']
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Inputs don\'t match! Expected {'\033[95m'}{exinputs}{'\033[94m'}, got {'\033[95m'}{ninputs}{'\033[94m'}!")
                valid_struc = False
            if(ndata['output'] != expectedN[0]['output']):
                noutput   = ndata['output']
                exoutput  = expectedN[0]['output']
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Outputs don\'t match! Expected {'\033[95m'}{exoutput}{'\033[94m'}, got {'\033[95m'}{noutput}{'\033[94m'}!")
                valid_struc = False
            if(ndata['weights'] != expectedN[0]['weights']):
                nweights   = ndata['weights']
                exweights  = expectedN[0]['weights']
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Weights don\'t match! Expected {'\033[95m'}{exweights}{'\033[94m'}, got {'\033[95m'}{nweights}{'\033[94m'}!")
                valid_struc = False
            if(ndata['bias'] != expectedN[0]['bias']):
                nbias   = ndata['bias']
                exbias  = expectedN[0]['bias']
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Biases don\'t match! Expected {'\033[95m'}{exbias}{'\033[94m'}, got {'\033[95m'}{nbias}{'\033[94m'}!")
                valid_struc = False
    if(not valid_struc):
        raise AssertionError
    print(f"{'\033[92m'}PASSED!{'\033[0m'}")

    #''' Node Connection ------------------------------------------------------------------------------------------------------------------------------------------------ '''

    # Making sure that I can create connections between nodes inside maps.
    print(f"{'\033[94m'}Testing individual node connection...")

    #       Manually checking each node's data values against a valid configuration...
    expectedN   = [
                   {'id': 1, 'out': [2], 'inc': [], 'inputs': 0.0, 'output': 0.0, 'weights': {}, 'bias': 0.0},
                   {'id': 2, 'out': [], 'inc': [1], 'inputs': 0.0, 'output': 0.0, 'weights': {1: 0.03}, 'bias': 0.0},
                   {'id': 3, 'out': [], 'inc': [], 'inputs': 0.0, 'output': 0.0, 'weights': {}, 'bias': 0.0}
                  ]
    valid_struc = True

    touch(testN, 2)
    touch(testN, 3)
    connect(testN, 1, 2, weight=0.03, assumeExists=False)

    #       These failures prevent value comparison, checking these first.
    if(len(nmap) > len(expectedN)):
        print(f"{'\033[91m'}FAILED!{'\033[94m'} connect() created an incorrect node!")
        raise AssertionError
    if(len(nmap) < len(expectedN)):
        print(f"{'\033[91m'}FAILED!{'\033[94m'} connect() removed a node!")
        raise AssertionError
    tally = 0
    for node in nmap:
        ndata = neuron_format(nmap[node])
        if(ndata['weights'] != 0):
            tally += len(ndata['weights'])
    if(tally > 1):
        print(f"{'\033[91m'}FAILED!{'\033[94m'} connect() created {'\033[95m'}more than one{'\033[94m'} weight! It created {'\033[95m'}{tally}{'\033[94m'} weights!")

    #       Checking each data value against my expected values...
    i = 0
    for node in nmap:
        ndata = neuron_format(nmap[node])
        if(ndata != expectedN[i]):
            mismatch = False
            if(ndata['id'] != expectedN[i]['id']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} IDs don\'t match!")
                valid_struc = False
                mismatch = True
            if(ndata['out'] != expectedN[i]['out']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Outs don\'t match!")
                valid_struc = False
                mismatch = True
            if(ndata['inc'] != expectedN[i]['inc']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Incs don\'t match!")
                valid_struc = False
                mismatch = True
            if(ndata['inputs'] != expectedN[i]['inputs']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Inputs don\'t match!")
                valid_struc = False
                mismatch = True
            if(ndata['output'] != expectedN[i]['output']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Outputs don\'t match!")
                valid_struc = False
                mismatch = True
            if(ndata['weights'] != expectedN[i]['weights']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Weights don\'t match!")
                valid_struc = False
                mismatch = True
            if(ndata['bias'] != expectedN[i]['bias']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Biases don\'t match!")
                valid_struc = False
                mismatch = True
            if(mismatch):
                print(f"{'\033[94m'}Expected {'\033[95m'}{expectedN[i]}{'\033[94m'}\nGot      {'\033[95m'}{ndata}{'\033[94m'}")
        i += 1
    if(not valid_struc):
        raise AssertionError
    print(f"{'\033[92m'}PASSED!{'\033[0m'}")

    #''' Node Deletion ------------------------------------------------------------------------------------------------------------------------------------ '''

    print(f"{'\033[94m'}Testing node deletion...{'\033[0m'}")

    expectedN   = [
                   {'id': 2, 'out': [], 'inc': [], 'inputs': 0.0, 'output': 0.0, 'weights': {}, 'bias': 0.0},
                   {'id': 3, 'out': [], 'inc': [], 'inputs': 0.0, 'output': 0.0, 'weights': {}, 'bias': 0.0}
                  ]
    valid_struc = True

    invtouch(testN, 1)

    if(len(nmap) < 2):
        print(f"{'\033[91m'}FAILED!{'\033[94m'} invtouch() deleted too many nodes!")
        raise AssertionError
    if(len(nmap) == 3):
        print(f"{'\033[91m'}FAILED!{'\033[94m'} invtouch() failed to delete any nodes!")
        raise AssertionError
    if(len(nmap) > 3):
        print(f"{'\033[91m'}FAILED!{'\033[94m'} invtouch() created nodes instead of deleting!")
        raise AssertionError

    #       Checking each data value against my expected values...
    i = 0
    for node in nmap:
        ndata = neuron_format(nmap[node])
        if(ndata != expectedN[i]):
            mismatch = False
            if(ndata['id'] != expectedN[i]['id']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} IDs don\'t match!")
                valid_struc = False
                mismatch = True
            if(ndata['out'] != expectedN[i]['out']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Outs don\'t match!")
                valid_struc = False
                mismatch = True
            if(ndata['inc'] != expectedN[i]['inc']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Incs don\'t match!")
                valid_struc = False
                mismatch = True
            if(ndata['inputs'] != expectedN[i]['inputs']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Inputs don\'t match!")
                valid_struc = False
                mismatch = True
            if(ndata['output'] != expectedN[i]['output']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Outputs don\'t match!")
                valid_struc = False
                mismatch = True
            if(ndata['weights'] != expectedN[i]['weights']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Weights don\'t match!")
                valid_struc = False
                mismatch = True
            if(ndata['bias'] != expectedN[i]['bias']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Biases don\'t match!")
                valid_struc = False
                mismatch = True
            if(mismatch):
                print(f"{'\033[94m'}Expected {'\033[95m'}{expectedN[i]}{'\033[94m'}\nGot      {'\033[95m'}{ndata}{'\033[94m'}")
        i += 1
    if(not valid_struc):
        raise AssertionError
    print(f"{'\033[92m'}PASSED!{'\033[0m'}")

    #''' Multi-Node Connection ------------------------------------------------------------------------------------------------------------------------------------ '''

    print(f"{'\033[94m'}Testing many-to-one node connections...{'\033[0m'}")

    expectedN = [
                 {'id': 2, 'out': [6], 'inc': [], 'inputs': 0.0, 'output': 0.0, 'weights': {}, 'bias': 0.0},
                 {'id': 3, 'out': [6], 'inc': [], 'inputs': 0.0, 'output': 0.0, 'weights': {}, 'bias': 0.0},
                 {'id': 1, 'out': [6], 'inc': [], 'inputs': 0.0, 'output': 0.0, 'weights': {}, 'bias': 0.0},
                 {'id': 4, 'out': [6], 'inc': [], 'inputs': 0.0, 'output': 0.0, 'weights': {}, 'bias': 0.0},
                 {'id': 5, 'out': [6], 'inc': [], 'inputs': 0.0, 'output': 0.0, 'weights': {}, 'bias': 0.0},
                 {'id': 6, 'out': [], 'inc': [1, 2, 3, 4, 5], 'inputs': 0.0, 'output': 0.0, 'weights': {1: 0.3, 2: 0.59, 3: 0.4, 4: 0.67, 5: 0.77}, 'bias': 0.0}
                ]
    valid_struc = True

    touch(testN, 1) # Putting this back for an easy-to-follow list iteration...
    for i in range(4):
        touch(testN, (i + 3)) # +3 because we're starting with three nodes already.
    connectManyToOne(testN, [1,2,3,4,5], 6, {1: 0.3, 2: 0.59, 3: 0.4, 4: 0.67, 5: 0.77})

    # Check for implementation failures which prevent value comparison...
    if(len(nmap) < len(expectedN)):
        print(f"{'\033[91m'}FAILED!{'\033[94m'} manyToOne() deleted nodes!")
        raise AssertionError
    if(len(nmap) > len(expectedN)):
        print(f"{'\033[91m'}FAILED!{'\033[94m'} manyToOne() created nodes!")
        raise AssertionError

    #       Checking each data value against my expected values...
    i = 0
    for node in nmap:
        ndata = neuron_format(nmap[node])
        if(ndata != expectedN[i]):
            mismatch = False
            if(ndata['id'] != expectedN[i]['id']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} IDs don\'t match!")
                valid_struc = False
                mismatch = True
            if(ndata['out'] != expectedN[i]['out']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Outs don\'t match!")
                valid_struc = False
                mismatch = True
            if(ndata['inc'] != expectedN[i]['inc']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Incs don\'t match!")
                valid_struc = False
                mismatch = True
            if(ndata['inputs'] != expectedN[i]['inputs']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Inputs don\'t match!")
                valid_struc = False
                mismatch = True
            if(ndata['output'] != expectedN[i]['output']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Outputs don\'t match!")
                valid_struc = False
                mismatch = True
            if(ndata['weights'] != expectedN[i]['weights']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Weights don\'t match!")
                valid_struc = False
                mismatch = True
            if(ndata['bias'] != expectedN[i]['bias']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Biases don\'t match!")
                valid_struc = False
                mismatch = True
            if(mismatch):
                print(f"{'\033[94m'}Expected {'\033[95m'}{expectedN[i]}{'\033[94m'}\nGot      {'\033[95m'}{ndata}{'\033[94m'}")
        i += 1
    if(not valid_struc):
        raise AssertionError
    print(f"{'\033[92m'}PASSED!{'\033[0m'}")


    print(f"{'\033[94m'}Testing one-to-many node connections...{'\033[0m'}")

    expectedN = [
                 {'id': 2, 'out': [6], 'inc': [6], 'inputs': 0.0, 'output': 0.0, 'weights': {6: 0.31}, 'bias': 0.0},
                 {'id': 3, 'out': [6], 'inc': [6], 'inputs': 0.0, 'output': 0.0, 'weights': {6: 0.38}, 'bias': 0.0},
                 {'id': 1, 'out': [6], 'inc': [6], 'inputs': 0.0, 'output': 0.0, 'weights': {6: 0.29}, 'bias': 0.0},
                 {'id': 4, 'out': [6], 'inc': [6], 'inputs': 0.0, 'output': 0.0, 'weights': {6: 0.54}, 'bias': 0.0},
                 {'id': 5, 'out': [6], 'inc': [6], 'inputs': 0.0, 'output': 0.0, 'weights': {6: 0.67}, 'bias': 0.0},
                 {'id': 6, 'out': [1, 2, 3, 4, 5], 'inc': [1, 2, 3, 4, 5], 'inputs': 0.0, 'output': 0.0,  'weights': {1: 0.3, 2: 0.59, 3: 0.4, 4: 0.67, 5: 0.77}, 'bias': 0.0}
                ]
    valid_struc = True

    connectOneToMany(testN, 6, [1, 2, 3, 4, 5], {1: 0.29, 2: 0.31, 3: 0.38, 4: 0.54, 5: 0.67})

    # Check for implementation failures which prevent value comparison...
    if(len(nmap) < len(expectedN)):
        print(f"{'\033[91m'}FAILED!{'\033[94m'} oneToMany() deleted nodes!")
        raise AssertionError
    if(len(nmap) > len(expectedN)):
        print(f"{'\033[91m'}FAILED!{'\033[94m'} oneToMany() created nodes!")
        raise AssertionError

    #       Checking each data value against my expected values...
    i = 0
    for node in nmap:
        ndata = neuron_format(nmap[node])
        if(ndata != expectedN[i]):
            mismatch = False
            if(ndata['id'] != expectedN[i]['id']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} IDs don\'t match!")
                valid_struc = False
                mismatch = True
            if(ndata['out'] != expectedN[i]['out']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Outs don\'t match!")
                valid_struc = False
                mismatch = True
            if(ndata['inc'] != expectedN[i]['inc']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Incs don\'t match!")
                valid_struc = False
                mismatch = True
            if(ndata['inputs'] != expectedN[i]['inputs']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Inputs don\'t match!")
                valid_struc = False
                mismatch = True
            if(ndata['output'] != expectedN[i]['output']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Outputs don\'t match!")
                valid_struc = False
                mismatch = True
            if(ndata['weights'] != expectedN[i]['weights']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Weights don\'t match!")
                valid_struc = False
                mismatch = True
            if(ndata['bias'] != expectedN[i]['bias']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Biases don\'t match!")
                valid_struc = False
                mismatch = True
            if(mismatch):
                print(f"{'\033[94m'}Expected {'\033[95m'}{expectedN[i]}{'\033[94m'}\nGot      {'\033[95m'}{ndata}{'\033[94m'}")
        i += 1
    if(not valid_struc):
        raise AssertionError
    print(f"{'\033[92m'}PASSED!{'\033[0m'}")

    #''' Disconnection ------------------------------------------------------------------------------------------------------------------------------------ '''

    print(f"{'\033[94m'}Testing node disconnection...{'\033[0m'}")

    expectedN   = [
                 {'id': 2, 'out': [6], 'inc': [], 'inputs': 0.0, 'output': 0.0, 'weights': {}, 'bias': 0.0},
                 {'id': 3, 'out': [6], 'inc': [6], 'inputs': 0.0, 'output': 0.0, 'weights': {6: 0.38}, 'bias': 0.0},
                 {'id': 1, 'out': [6], 'inc': [6], 'inputs': 0.0, 'output': 0.0, 'weights': {6: 0.29}, 'bias': 0.0},
                 {'id': 4, 'out': [6], 'inc': [6], 'inputs': 0.0, 'output': 0.0, 'weights': {6: 0.54}, 'bias': 0.0},
                 {'id': 5, 'out': [6], 'inc': [6], 'inputs': 0.0, 'output': 0.0, 'weights': {6: 0.67}, 'bias': 0.0},
                 {'id': 6, 'out': [1, 3, 4, 5], 'inc': [1, 2, 3, 4, 5], 'inputs': 0.0, 'output': 0.0, 'weights': {1: 0.3, 2: 0.59, 3: 0.4, 4: 0.67, 5: 0.77}, 'bias': 0.0}
                  ]
    #expectedN = testN.__dict__["lookup"] # Find a way to make this work instead. It's generalizable and doesn't care as much about underlying implementation.
    valid_struc = True

    disconnect(testN, 6, 2)

    # Check for implementation failures which prevent value comparison...
    if(len(nmap) < len(expectedN)):
        print(f"{'\033[91m'}FAILED!{'\033[94m'} disconnect() deleted nodes!")
        raise AssertionError
    if(len(nmap) > len(expectedN)):
        print(f"{'\033[91m'}FAILED!{'\033[94m'} disconnect() created nodes!")
        raise AssertionError

    #       Checking each data value against my expected values...
    i = 0
    for node in nmap:
        ndata = neuron_format(nmap[node])
        if(ndata != expectedN[i]):
            mismatch = False
            if(ndata['id'] != expectedN[i]['id']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} IDs don\'t match!")
                valid_struc = False
                mismatch = True
            if(ndata['out'] != expectedN[i]['out']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Outs don\'t match!")
                valid_struc = False
                mismatch = True
            if(ndata['inc'] != expectedN[i]['inc']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Incs don\'t match!")
                valid_struc = False
                mismatch = True
            if(ndata['inputs'] != expectedN[i]['inputs']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Inputs don\'t match!")
                valid_struc = False
                mismatch = True
            if(ndata['output'] != expectedN[i]['output']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Outputs don\'t match!")
                valid_struc = False
                mismatch = True
            if(ndata['weights'] != expectedN[i]['weights']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Weights don\'t match!")
                valid_struc = False
                mismatch = True
            if(ndata['bias'] != expectedN[i]['bias']):
                print(f"{'\033[91m'}FAILED!{'\033[94m'} Biases don\'t match!")
                valid_struc = False
                mismatch = True
            if(mismatch):
                print(f"{'\033[94m'}Expected {'\033[95m'}{expectedN[i]}{'\033[94m'}\nGot      {'\033[95m'}{ndata}{'\033[94m'}")
        i += 1
    if(not valid_struc):
        raise AssertionError
    print(f"{'\033[92m'}PASSED!{'\033[0m'}")

    #''' Save to file ------------------------------------------------------------------------------------------------------------------------------------- '''
    # TODO Make tests for file descriptors (lstat) and pathname boundaries, not just saved data accuracy!

    print(f"{'\033[94m'}Testing file saving...{'\033[0m'}")
    # Being able to load may logically imply that saving worked fine, but I want to have some way to verify the save structure per version.

    print(f"{'\033[94m'}--- Checking filename boundaries...{'\033[0m'}")
    # This list should test for INVALID filenames. Check for filesystem traversal and OS disallowed characters.
    invalidFilenames = ['', '~/etc/password.json', 'temp..json', 'file?.json', '../password.txt', 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.json', f"{'\033[0m'}cringe.md"]
    for name in invalidFilenames:
        try:
            save(testN, name)
            save(testN, name, overwrite=True)
            print(f"{'\033[91m'}FAILED!{'\033[94m'} save() allowed the illegal filename {'\033[95m'}\'{name}\'{'\033[94m'}!{'\033[0m'}")
            raise AssertionError
        except KeyError: # This is expected behavior. All these filenames should fail inspection.
            pass
    print(f"{'\033[92m'}--- PASSED!{'\033[0m'}")
    # ''' Shouldn't I also check to make sure it isn't creating a file that is too big? How would I even check for that?? '''
    print(f"{'\033[94m'}--- Checking respect for symbolic links...{'\033[0m'}")
    print(f"{'\033[91m'}--- FAILED!{'\033[94m'} ... no test exists. Moving on...{'\033[0m'}")

    # The 'expectedOutput' string will need to be hand modified every time the save structure is modified. I literally pulled these from the file after saving and verifying manually. Cringe.
    expectedOutput = "testN\n0.3 6 -2 12\n\n\n\n2 0.0 0.0 0.0\n\n6\n\n\n3 0.0 0.0 0.0\n6\n6\n6 0.38\n\n1 0.0 0.0 0.0\n6\n6\n6 0.29\n\n4 0.0 0.0 0.0\n6\n6\n6 0.54\n\n5 0.0 0.0 0.0\n6\n6\n6 0.67\n\n6 0.0 0.0 0.0\n1 2 3 4 5\n1 3 4 5\n1 0.3\n2 0.59\n3 0.4\n4 0.67\n5 0.77\n\n"
    actual = ""

    save(testN, overwrite=True) #''' TODO Don't forget that the 'True' needs to be removed. This section tests for checking overwrite confirmation and saving accuracy! '''
    try:
        f = open("temp.json", "r", encoding="utf-8")
        line = f.readline()
        while(line != ""):
            if(line != ""):
                actual += line
            line = f.readline()
        f.close()
    except FileNotFoundError:   # I should only need to check this once, but the reality is that I don't know how the functions are implemented. Checking it every time then!
        print(f"{'\033[91m'}FAILED!{'\033[94m'} File was never saved!")
        raise AssertionError

    if(actual != expectedOutput):
        print(f"{'\033[91m'}FAILED!{'\033[94m'} Saved data doesn\'t match the current network object! Printing expected and actual for comparison...")
        print(f"---- expected: ------\n{expectedOutput}\n---- actual: ------\n{actual}")
        raise AssertionError

    invtouch(testN, 6)

    actual = ""

    # This one should NOT overwrite the current state.
    save(testN, overwrite=False)
    try:
        f = open("temp.json", "r", encoding="utf-8")
        line = f.readline()
        while(line != ""):
            if(line != ""):
                actual += line
            line = f.readline()
        f.close()
    except FileNotFoundError:   # I should only need to check this once, but the reality is that I don't know how the functions are implemented. Checking it every time then!
        print(f"{'\033[91m'}FAILED!{'\033[94m'} File was deleted!")
        raise AssertionError

    if(actual != expectedOutput):
        print(f"{'\033[91m'}FAILED!{'\033[94m'} Saved data was modified!")
        raise AssertionError

    expectedOutput = "testN\n0.3 5 -2 12\n\n\n\n2 0.0 0.0 0.0\n\n\n\n\n3 0.0 0.0 0.0\n\n\n\n\n1 0.0 0.0 0.0\n\n\n\n\n4 0.0 0.0 0.0\n\n\n\n\n5 0.0 0.0 0.0\n\n\n\n\n"
    actual = ""

    # This one SHOULD overwrite the current state.
    save(testN, overwrite=True)
    try:
        f = open("temp.json", "r", encoding="utf-8")
        line = f.readline()
        while(line != ""):
            if(line != ""):
                actual += line
            line = f.readline()
        f.close()
    except FileNotFoundError:   # I should only need to check this once, but the reality is that I don't know how the functions are implemented. Checking it every time then!
        print(f"{'\033[91m'}FAILED!{'\033[94m'} File was deleted!")
        raise AssertionError

    if(actual != expectedOutput):
        print(f"{'\033[91m'}FAILED!{'\033[94m'} Saved data doesn\'t match the current network object! Printing expected and actual for comparison...")
        print(f"---- expected: ------\n{expectedOutput}\n---- actual: ------\n{actual}")
        raise AssertionError
    print(f"{'\033[92m'}PASSED!{'\033[0m'}")

    #''' Load from file ----------------------------------------------------------------------------------------------------------------------------------- '''
    # TODO Make tests for file descriptors (lstat) and pathname boundaries, not just loaded data accuracy!

    print(f"{'\033[94m'}Testing file loading without validation...{'\033[0m'}")

    print(f"{'\033[94m'}--- Checking filename boundaries...{'\033[0m'}")
    for name in invalidFilenames:
        try:
            load(name, testN, validate=False)
            print(f"{'\033[91m'}FAILED!{'\033[94m'} load() allowed the illegal filename {'\033[95m'}\'{name}\'{'\033[94m'}!{'\033[0m'}")
        except KeyError: # This is expected behavior. All these filenames should fail inspection.
            pass
    print(f"{'\033[92m'}--- PASSED!{'\033[0m'}")
    print(f"{'\033[94m'}--- Checking respect for \'too large\' files...{'\033[0m'}")
    try:
        large = Network()
        load('temp.json', large, validate=False, max_filesize=0) # Nothing should be less than 0 bytes
        print(f"{'\033[91m'}FAILED!{'\033[94m'} load() allowed a file that was too big!{'\033[0m'}")
        raise AssertionError
    except MemoryError: # If the memory error gets raised then it respects large files.
            pass
    print(f"{'\033[92m'}--- PASSED!{'\033[0m'}")
    print(f"{'\033[94m'}--- Checking respect for symbolic links...{'\033[0m'}")
    print(f"{'\033[91m'}--- FAILED!{'\033[94m'} ... no test exists. Moving on...{'\033[0m'}")

    # So I can compare weights when I load data...
    connect(testN, 1, 4)
    connect(testN, 2, 3)
    connect(testN, 3, 4)
    save(testN, 'temp.json', True)

    # Implicitly check for current data replacement on load...
    rando = Network()
    rando.modelID = "rando"
    for i in range(20):
        touch(rando, i)
    connect(rando, 1, 7)

    # We are going to compare against testN. Since testN was saved into temp.json, rando should have the same data when I load temp.json into it.
    load('temp.json', rando, validate=False)

    # Network comparison variables
    expectedMap   = testN.__dict__
    actualMap     = rando.__dict__
    differencesMap= {}
    ignoreMap     = {"lookup": 0} # Ignoring lookup, I'll explain later. Anyway, in case keys from expected are missing from actual I can skip missing keys to avoid the key error.

    # TODO For the sum of all errors sections... print the problematic key or values before listing unexpected entries. That will make errors far more interpretable.
    # TODO Check for inc and out matching more thoroughly! I think I'm just doing a surface level comparison check instead of matching data types manually right now.
    ''' Checking map attributes first since it doesn't have dictionaries inside a dictionary... '''
    # Collect missing, extra, and invalid keys...
    for key in actualMap:
        if key not in expectedMap:
            differencesMap[key] = actualMap[key]
    for key in expectedMap:
        if key not in actualMap and key not in differencesMap:
            differencesMap[key] = expectedMap[key]
            ignoreMap[key]     = True
    # Checks to make sure each value inside of the loaded object matches the expected values. Differences will be noted and passed with an error!
    for key in expectedMap:
        if key not in ignoreMap:
            if(expectedMap[key] != actualMap[key]):
                differencesMap[key] = actualMap[key]
    # Print all differences along with source of error!
    if(len(differencesMap) != 0):
        print(f"{'\033[91m'}FAILED!{'\033[94m'} Found {'\033[95m'}{len(differencesMap)}{'\033[94m'} differences between expected/actual object fields! See below:{'\033[0m'}")
        for key in differencesMap:
            if key not in actualMap:
                print(f"{'\033[93m'}\'{key}\'{'\033[94m'} is missing from actual object!{'\033[0m'}")
            elif key not in expectedMap:
                print(f"{'\033[93m'}\'{key}\'{'\033[94m'} is not in expected values!{'\033[0m'}")
            else:
                print(f"{'\033[93m'}\'{key}\'{'\033[94m'} is {'\033[95m'}{actualMap[key]}{'\033[94m'} in actual, expected was {'\033[95m'}{expectedMap[key]}{'\033[94m'}!{'\033[0m'}")
        raise AssertionError

    # Node comparison variables
    differencesMap = {}
    invalidKeys    = {}
    failed         = False

    # TODO For the sum of all errors sections... print the problematic key or values before listing unexpected entries. That will make errors far more interpretable.
    ''' Checking the node lookup... '''
    # I only need to check for keys, not the values for an object in lookup. The value comparision here fails because different memory addresses are counted as not identical.
    ''' This is going to require that I customize the comparision code a good bit. I need to compare data types against each other, not just their values or names like I have been. '''
    # Collect missing, extra, and invalid keys...
    for key in actualMap["lookup"]:
        if key not in expectedMap["lookup"]:
            differencesMap[key] = actualMap["lookup"][key]
    for key in expectedMap["lookup"]:
        if key not in actualMap["lookup"] and key not in differencesMap:
            differencesMap[key] = expectedMap["lookup"][key]
    # Checks to make sure each object inside of the loaded object is a neuron object. If it is, makes sure each obj has the right values. Differences will be noted and passed with an error!
    for key in actualMap["lookup"]:
        if(not isinstance(key, int)):                         # Add if key is not int
            invalidKeys[key] = actualMap["lookup"][key]
        if(not isinstance(actualMap["lookup"][key], Neuron)): # Add if entry for key is not Neuron object
            invalidKeys[key] = actualMap["lookup"][key]
    # Print all key/value differences along with source of error...
    if(len(differencesMap) != 0):
        failed = True
        print(f"{'\033[91m'}FAILED!{'\033[94m'} Found {'\033[95m'}{len(differencesMap)}{'\033[94m'} differences in node lookup between expected and actual object. See below:{'\033[0m'}")
        for key in differencesMap:
            if key not in actualMap["lookup"]:
                print(f"{'\033[93m'}\'{key}\'{'\033[94m'} is missing from actual lookup!{'\033[0m'}")
            elif key not in expectedMap["lookup"]:
                print(f"{'\033[93m'}\'{key}\'{'\033[94m'} is not in expected lookup!{'\033[0m'}")
            else:
                print(f"{'\033[93m'}\'{key}\'{'\033[94m'} is {'\033[95m'}{actualMap[key]}{'\033[94m'} in actual, expected was {'\033[95m'}{expectedMap[key]}{'\033[94m'}!{'\033[0m'}")
    # Print all invalid key/entry types along with expected corresponding types...
    if(len(invalidKeys) != 0):
        failed = True
        print(f"{'\033[91m'}FAILED!{'\033[94m'} Found {'\033[95m'}{len(invalidKeys)}{'\033[94m'} invalid key/value types inside actual lookup! See below:{'\033[0m'}")
        for key in invalidKeys:
            if(not isinstance(key, int)):
                print(f"{'\033[94m'}Key {'\033[95m'}\'{key}\'{'\033[94m'} is not of type {'\033[95m'}{type(0)}{'\033[94m'}, is instead type {'\033[95m'}{type(key)}{'\033[94m'}!{'\033[0m'}")
            if(not isinstance(invalidKeys[key], Neuron)):
                print(f"{'\033[94m'}For key {'\033[95m'}\'{key}\'{'\033[94m'}, Entry {'\033[95m'}\'{invalidKeys[key]}\'{'\033[94m'} is not of type {'\033[95m'}{type(Neuron())}{'\033[94m'}, is instead type {'\033[95m'}{type(invalidKeys[key])}{'\033[94m'}!{'\033[0m'}")
    if(failed):
        raise AssertionError

    # TODO For the sum of all errors sections... print the problematic key or values before listing unexpected entries. That will make errors far more interpretable.
    # TODO Test these by adding fields to neuron objects inside the actual lookup dictionary!
    errors = ""
    # Comparing known valid entries' object values against each other...
    for node in expectedMap["lookup"]:
        if node not in invalidKeys:
            expectedNode   = expectedMap["lookup"][node].__dict__
            actualNode     = actualMap["lookup"][node].__dict__
            differencesNode= {}
            ignoreNode     = {"weights": 0} # Skipping weights, I'll explain later. Anyway, in case keys from expected are missing from actual I can skip missing keys to avoid the key error.
            # Collect missing, extra, and invalid keys per node...
            for key in actualNode:
                if key not in expectedNode:
                    differencesNode[key] = actualNode[key]
            for key in expectedNode:
                if key not in actualNode and key not in differencesNode:
                    differencesNode[key] = expectedNode[key]
                    ignoreNode[key] = True
            # Check to make sure each key present in actual has the correct values.
            for key in expectedNode:
                if key not in ignoreNode:
                    if(expectedNode[key] != actualNode[key]):
                        differencesNode[key] = actualNode[key]
            # Collect all differences along with source of error into a string to print later. I'd rather collect the sum of all errors since there are likely error patterns in the loader.
            if(len(differencesNode) != 0):
                errors += f"{'\033[91m'}FAILED!{'\033[94m'} Found {'\033[95m'}{len(differencesNode)}{'\033[94m'} differences between expected values and actual values for node {'\033[95m'}\'{node}\'{'\033[94m'}! See below:{'\033[0m'}\n"
                for key in differencesNode:
                    if key not in actualNode:
                        errors += f"{'\033[93m'}\'{key}\'{'\033[94m'} is missing from object!{'\033[0m'}\n"
                    elif key not in expectedNode:
                        errors += f"{'\033[93m'}\'{key}\'{'\033[94m'} is not in expected values!{'\033[0m'}\n"
                    else:
                        errors += f"{'\033[93m'}\'{key}\'{'\033[94m'} is {'\033[95m'}{actualNode[key]}{'\033[94m'}, expected was {'\033[95m'}{expectedNode[key]}{'\033[94m'}!{'\033[0m'}\n"
    if(errors != ""):
        print(f"{errors[:-1]}")
        raise AssertionError

    errors = ""
    correctKey = int  # I would just fetch these each time in case I change the structure later, but I don't have an acceptable solution coming to mind and idk I'm just not feelin it rn.
    correctVal = float
    # Checking for correct keys and values inside of weights per node.
    for node in expectedMap["lookup"]:
        expectedC = expectedMap["lookup"][node].weights
        actualC   = actualMap["lookup"][node].weights
        ignoreKeys= {} # Once again I need to ignore missing keys...
        if(expectedC != actualC):
            errors += f"{'\033[91m'}FAILED!{'\033[94m'} Weights on node {'\033[95m'}{node}{'\033[94m'} don't match expected network! See below:{'\033[0m'}\n"
            incorrectKeys = []
            for key in actualC:
                if(type(key) != correctKey):
                    errors += f"{'\033[94m'}An incorrect key type of {'\033[95m'}{type(key)}{'\033[94m'} was found! It should be a {'\033[95m'}{correctKey}{'\033[94m'}!\n"
                # Just to be clear on something, if keys are in the wrong type, off-by-one, or otherwise, I literally can't know which it's meant to refer to. The IDs are too important!
            if(len(expectedC) != len(actualC)):
                errors += f"{'\033[94m'}Weights on node {'\033[95m'}{node}{'\033[94m'} aren't the same length on network! Expected {'\033[95m'}{len(expectedC)}{'\033[94m'}, got {'\033[95m'}{len(actualC)}{'\033[94m'}!{'\033[0m'}\n"
            for key in expectedC:
                if key not in actualC:
                    errors += f"{'\033[94m'}Key {'\033[95m'}\'{key}\'{'\033[94m'} is missing!\n"
                    ignoreKeys[key] = 0
                if key not in ignoreKeys:
                    if(expectedC[key] != actualC[key]):
                        errors += f"{'\033[94m'} Weight between nodes {'\033[95m'}{key}{'\033[94m'} and {'\033[95m'}{node}{'\033[94m'} is wrong! Expected {'\033[95m'}{expectedC[key]}{'\033[94m'}, got {'\033[95m'}{actualC[key]}{'\033[94m'}!\n"

    if(errors != ""):
        print(f"{errors[:-1]}")
        raise AssertionError

    print(f"{'\033[92m'}PASSED!{'\033[0m'}")

    print(f"{'\033[94m'}Testing file validation...{'\033[0m'}") # Last thing in this list. Hoooooly that last one was a lot of work, but this will be even more work still...
    # I'm gonna have to manually set (and reset) the validation file's contents to make sure that the validation function does its job... Checklist should go as follows:
    # -  I need a way to immediately filter out most malicious/malformed files.
    # -  First, check for larger than mathematically possible (given the size of objects) files. This puts an upper limit on data parsing.
    # -  Then, check each entry against currently accepted data types.
    # -  Then, check each entry against known maximum values, or else reasonable limits.
    # -  Repeat this process for each line of data passed into validation.
    # This should account for all "reasonable" net structures. All remaining behavior should be due to net/evaluation/modification functions!
    # I should also note, my validation function should also provide a specific error related to whatever it finds invalid.
    # This way, logical holes inside the function should be easy to spot! I highly doubt I will get this correct the second time, unfortunately.

    validationfile = "validate.json"

    print(f"{'\033[94m'}--- Checking filename boundaries...{'\033[0m'}")
    for name in invalidFilenames:
        try:
            validate_file(name, log_errors=False)
            print(f"{'\033[91m'}FAILED!{'\033[94m'} validate_file() allowed the illegal filename {'\033[95m'}\'{name}\'{'\033[94m'}!{'\033[0m'}")
        except KeyError: # This is expected behavior. All these filenames should fail inspection.
            pass
    print(f"{'\033[92m'}--- PASSED!{'\033[0m'}")
    print(f"{'\033[94m'}--- Checking respect for \'too large\' files...{'\033[0m'}")
    try:
        validate_file('temp.json', log_errors=False, max_filesize=0) # Nothing should be less than 0 bytes
        print(f"{'\033[91m'}FAILED!{'\033[94m'} validate_file() tried to validate a file that was too big!{'\033[0m'}")
        raise AssertionError
    except MemoryError: # If the memory error gets raised then it respects large files.
            pass
    print(f"{'\033[92m'}--- PASSED!{'\033[0m'}")
    print(f"{'\033[94m'}--- Checking respect for symbolic links...{'\033[0m'}")
    print(f"{'\033[91m'}--- FAILED!{'\033[94m'} ... no test exists. Moving on...{'\033[0m'}")

    # Replace with actual test code...

    print(f"{'\033[91m'}FAILED!{'\033[94m'} ...tests unfinished.{'\033[0m'}")
    raise AssertionError

    print(f"{'\033[94m'}All building tests {'\033[92m'}PASSED{'\033[94m'}! --------------------------------------------------------{'\033[0m'}\n")

def test_basic():
    print(f"{'\033[94m'}Going over all basic functionalities...{'\033[0m'}")

    print(f"Making sure arbitrary graph building works first...\n")
    test_building()
    print(f"Testing forwards/backwards traversal...")

    print(f"{'\033[91m'}FAILED!{'\033[94m'} ...tests unfinished.{'\033[0m'}")
    raise AssertionError

    print(f"Testing restart functionality...")

    print(f"{'\033[91m'}FAILED!{'\033[94m'} ...tests unfinished.{'\033[0m'}")
    raise AssertionError

def test_evaluator(eval_function, test_dependencies=True): # Used to test an arbitrary evaluation function... figured I'd need these to test functions I make.
    print(f"{'\033[94m'}Going over all evaluation functionalities...{'\033[0m'}")

    if(test_dependencies):
        print(f"Making sure basic functionality works first...\n")
        test_basic()

    print(f"Testing input acquisition...")

    print(f"{'\033[91m'}FAILED!{'\033[94m'} ...tests unfinished.{'\033[0m'}")
    raise AssertionError

    print(f"Testing activation feedforward...")

    print(f"{'\033[91m'}FAILED!{'\033[94m'} ...tests unfinished.{'\033[0m'}")
    raise AssertionError

def test_solver(optimizer_function, test_dependencies=True, eval_function=None): # Used to test an arbitrary solver function... figured I'd need these to test functions I make.
    print(f"{'\033[94m'}Going over all solver functionalities...{'\033[0m'}")

    if(test_dependencies):
        if(not isinstance(eval_function, type(optimizer_function))): # type(optimizer_function) just lets me check if the eval_function is a function. I don't know how to indicate the data type.
            print(f"Please pass a function into eval_function!")
            raise AssertionError # Color code this ^ please
        print(f"Making sure all dependencies work first...\n")
        test_basic()

    print(f"Testing reward measurement...")

    print(f"{'\033[91m'}FAILED!{'\033[94m'} ...tests unfinished.{'\033[0m'}")
    raise AssertionError

    print(f"Testing gradient values...")

    print(f"{'\033[91m'}FAILED!{'\033[94m'} ...tests unfinished.{'\033[0m'}")
    raise AssertionError

    print(f"Testing gradient descent...")

    print(f"{'\033[91m'}FAILED!{'\033[94m'} ...tests unfinished.{'\033[0m'}")
    raise AssertionError

# Add more tests as they become necessary! ALSO KEEP BACKUPS!!!

test_basic()

#print("We good!")
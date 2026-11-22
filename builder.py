import os
from neuron import *
from network import *
from random import random, randrange
from sys import getsizeof
from _io import TextIOWrapper

# Limit set to 20MB. Number represents bytes. To change the limit to your needs, follow:
    #   001(PB),  001(TB),  001(GB),  001(MB),  001(KB),  001(B)
    #   Petabyte, Terabyte, Gigabyte, Megabyte, Kilobyte, Byte
    #   Example: 20MB = 20 000 000 -> 20000000, 64GB = 64 000 000 000 -> 64000000000
max_bytes = 20000000

def touch(obj, ID): # Creates nodes. Named after the 'touch' command in terminal which creates files. "Imaginary" nodes become "Real".
    if(not isinstance(ID, int)):
        raise AttributeError(f"Please pass only ints into ID! Got {type(ID)} instead of 'int'! Usage: touch(lookup, ID) lookup=<dictionary> ID=<int>")
    if(not isinstance(obj, Network)):
        raise AttributeError(f"Please pass in a network object to add to! Usage: touch(obj, ID) lookup=<Network> ID=<int>")
    if ID in obj.lookup:
        pass
    else:
        obj.lookup[ID] = Neuron(id=ID)

def invtouch(obj, ID, checkData=True): # WIP Name, inverse touch. Deletes nodes.
    if(checkData):
        if(not isinstance(ID, int) or not isinstance(obj, Network)):
            raise TypeError("Please pass in correct data for invtouch! Usage: invtouch(obj, ID) lookup=<Network> ID=<int>")
        if ID not in obj.lookup:
            raise KeyError(f"Node '{ID}' does not exist!")

    lookup = obj.lookup

    # Disconnect other node's connections first, then the node.
    prevs = lookup[ID].inc
    nexts = lookup[ID].out

    for key in prevs:
        lookup[key].out.remove(ID)
    for key in nexts:
        lookup[key].inc.remove(ID)
        del lookup[key].weights[ID]

    del lookup[ID]

def connect(obj, id1, id2, weight=0.5, assumeExists=True, checkData=True): # Connects two nodes in the direction of id1 -> id2. id1 outputs, into id2.
    # assumeExists is set to true by default because I should be explicitly aware of what nodes I'm interacting with. Certain functions may set it to false once I abstract stuff away.
    # I MAY ACTUALLY DELETE THIS OPTION ENTIRELY. It depends on whether or not the logical guarantee of 'real' node interaction is as helpful as I assume.

    if(not isinstance(obj, Network)):
        raise TypeError("Only pass in Network objects into obj! Usage: connect(obj=Network, id1=int, id2=int, weight=float, assumeExists=bool, checkData=bool)")

    lookup = obj.lookup

    # checkData is set to true by default because I don't trust that I'll always pass in the correct datatypes the first time. Certain functions may set it to false once I abstract stuff away.
    if(checkData):
        if(not isinstance(id1, int) or not isinstance(id2, int) or (not isinstance(weight, int) and not isinstance(weight, float))):
            raise TypeError("Please pass in correct data for connect!")
        if id1 not in lookup:
            raise KeyError(f"Node {id1} does not exist!")
        if id2 not in lookup:
            raise KeyError(f"Node {id2} does not exist!")

    if(assumeExists == False):
        # Since I'm unsure whether the passed nodes are in the lookup, I need to make sure they are before connecting them or else I'll get a key error.
            touch(obj, id1)
            touch(obj, id2)

    '''
    # Now that I know the nodes exist and all data passed is valid I need to update the network object's starts and ends...
    # TODO I think that being able to mutate the starts/ends in place is an interesting problem, but right now I think it would be easier to just require they be checked before eval/solving.
    if(lookup[id1].out == []):
        obj.end.remove(id1)   # I will allow the ValueError from the passed ID being missing inside of lookup stop my program. If that case shows up, I messed up my logic somewhere.
    if(lookup[id2].inc == []):
        obj.start.remove(id2) # I will allow the ValueError from the passed ID being missing inside of lookup stop my program. If that case shows up, I messed up my logic somewhere.
    '''

    # Now connect the two nodes!
    # Add id2 to id1's output nodes...
    lookup[id1].out.append(id2)
    # Add the weight between id1 and id2 to id2's weights.
    #   If weights are on id2's side, faster backprop. If weights are on id1's side, faster eval. Not mutually exclusive, but requires more system RAM to actually get the benefits.
    lookup[id2].weights[id1] = weight
    ''' lookup[id1].weights[id2] = weight #'''
    # Add id1 to id2's input nodes...
    lookup[id2].inc.append(id1)

def disconnect(obj, id1, id2):
    if(not isinstance(id1, int) or not isinstance(id2, int) or not isinstance(obj, Network)):
        raise AttributeError(f"Pass in correct data for disconnect()! Usage: disconnect(obj, id1, id2) obj=<Network> id1=<int> id2=<int>")

    lookup = obj.lookup
    if id1 not in lookup:
        raise KeyError(f"Node {id1} does not exist!")
    if id2 not in lookup:
        raise KeyError(f"Node {id2} does not exist!")

    lookup[id1].out.remove(id2)
    lookup[id2].inc.remove(id1)
    del lookup[id2].weights[id1]

def connectManyToOne(obj, list1, nodeid, weights={}, checkData=True, assumeExists=True):
    if(checkData == True): # Check that passed values are legitimate...
        if(not isinstance(list1, list) or not isinstance(nodeid, int) or not isinstance(weights, dict) or not isinstance(obj, Network)):
            raise TypeError(f"Pass the correct data types into list1, nodeid, weights, and obj please!")
        for i in range(len(list1)):
            if not isinstance(list1[i], int):
                raise TypeError(f"Please pass only int IDs into list1!")
        if(len(weights) != len(list1)):
            if(len(weights) != 0):
                raise TypeError(f"Please make sure you pass exactly enough weights for each node being connected!")
        for key in weights:
            if(not isinstance(key, int) or (not isinstance(weights[key], float) and not isinstance(weights[key], int)) ):
                raise TypeError(f"Please make sure that keys are int IDs and that weights are floats or ints!")
    # Will just trust that lookup is set up correctly. Errors will happen on evaluation if it's wrong, anyway.
    # TODO Fix that ^ attitude. I can do better than that. Check that the passed IDs actually exist. AssumeExists isn't even handled, though maybe I could do more.

    if(len(weights) != 0):
        for i in range(len(list1)):
            connect(obj, list1[i], nodeid, weight=weights[list1[i]], checkData=checkData, assumeExists=assumeExists)
    else:
        for i in range(len(list1)):
            connect(obj, list1[i], nodeid, checkData=checkData, assumeExists=assumeExists)

def connectOneToMany(obj, nodeid, list1, weights={}, checkData=True, assumeExists=True):
    if(checkData == True): # Check that passed values are legitimate...
        if(not isinstance(nodeid, int) or not isinstance(list1, list) or not isinstance(weights, dict) or not isinstance(obj, Network)):
            raise TypeError(f"Pass the correct data types into nodeid, list1, weights, and obj please!")
        for i in range(len(list1)):
            if not isinstance(list1[i], int):
                raise TypeError(f"Please pass only int IDs into list1!")
        if(len(weights) != len(list1)):
            if(len(weights) != 0):
                raise TypeError(f"Please make sure you pass exactly enough weights for each node being connected!")
        for key in weights:
            if(not isinstance(key, int) or (not isinstance(weights[key], float) and not isinstance(weights[key], int)) ):
                # I'm leaving this section alone because this is a more thorugh and informative error than all the rest before. This is a good habit, come back to it!
                print(f"\n{'\033[91m'}Please make sure that keys are int IDs and that weights are floats or ints!\n")
                print(f"Values were: key={type(key)}, weights[key]={type(weights[key])}")
                raise TypeError("Please make sure that keys are int IDs and that weights are floats or ints!")
    # Will just trust that lookup is set up correctly. Errors will happen on evaluation if it's wrong, anyway.
    # TODO Fix that ^ attitude. I can do better than that. Check that the passed IDs actually exist. AssumeExists isn't even handled, though maybe I could do more.

    if(len(weights) != 0):
        for i in range(len(list1)):
            connect(obj, nodeid, list1[i], weight=weights[list1[i]], checkData=checkData, assumeExists=assumeExists)
    else:
        for i in range(len(list1)):
            connect(obj, nodeid, list1[i], checkData=checkData, assumeExists=assumeExists)

def buildDense(obj, inputs, outputs, layers, width):
    if(not isinstance(obj, Network)):
        print(f"\n{'\033[91m'}Pass only a network object into buildDense! Expected Network, got {type(obj)}!\n")
        raise TypeError
    lookup = obj.lookup
    # Until I can create arbitrary network arrangements I'll assume a dense transformer structure.
    if(not isinstance(lookup, dict)):
        print(f"\n{'\033[91m'}Pass only an empty network into buildDense!\n")
        raise TypeError
    if(len(lookup) > 0):
        print(f"\n{'\033[91m'}Pass only an empty network into buildDense!\n")
        raise TypeError
    # If we get here, we should be good to go. I could check the other data values but eh fuck it.

    #print(f"Starting values are:\nnumInputs={inputs}, numOutputs={outputs}, layers={layers}, width={width}")

    # '''
    # Create all necessary nodes according to values passed. Inputs have negative IDs and all others have positive IDs.
    for i in range( outputs + (width * layers) ):
        lookup[i] = Neuron(id=i, bias=(float(f"{(randrange(-100000, 100000) * 0.00001):.5f}")))
    for i in range( inputs ):
        lookup[-(i + 1)] = Neuron(id=(-(i + 1)), bias=0.0)

    #print(f"Network after generating nodes:\n{printrawnetwork()}")

    # Body...
    # Each network requires I generate and assign weights between each layer.
    # Don't forget that findEnds doesn't work yet! That function relies on traversal, and that's being set up here!
    if(layers >= 2 and width > 0):
        for k in range( (layers - 1) ):                     # Each layer requires...
            prevLayer = []
            nextLayer = []
            tempweights = {}
            for prev in range(width):                       # Connecting every node in the previous layer...
                prevLayer.append( (k * width) + prev )
            for next in range(width):                       # To every node in the next layer!
                nextLayer.append( ((k + 1) * width) + next )

            for new in nextLayer:
                for i in prevLayer:
                    tempweights[i] = float( f"{(randrange(-100000, 100000) * 0.00001):.5f}" ) # I need weights for the new connections...
                connectManyToOne(obj, prevLayer, new, weights=tempweights, checkData=False)

    #print(f"Network after making body:\n{printrawnetwork()}")

    # Inputs...
    if(layers >= 1 and width > 0):
        layer1 = []
        for i in range(width): # I'm referring to each node in the layer. The total number of nodes in the whole network should be below 'width' so I assume this line shouldn't break anything.
            layer1.append(i)
        for i in range(inputs):
            tempweights = {}
            for j in layer1:
                tempweights[j] = float( f"{(randrange(-100000, 100000) * 0.00001):.5f}" )
            connectOneToMany(obj, -(i + 1), layer1, weights=tempweights, checkData=False)
    else:
        layer1 = []
        for i in range(outputs): # I'm using outputs because the network needs to output something from input data.
            layer1.append(i)
        for i in range(inputs):
            tempweights = {}
            for j in layer1:
                tempweights[j] = float( f"{(randrange(-100000, 100000) * 0.00001):.5f}" )
            connectOneToMany(obj, -(i + 1), layer1, weights=tempweights, checkData=False)

    #print(f"Network after creating and linking inputs:\n{printrawnetwork()}")

    # Outputs...
    if(layers >= 1 and width > 0): # I only need to manually set outputs if there are layers. Otherwise, everything should be set up by now. Should be...
        layerlast = findEnds(lookup) # Works as long as layers isn't 1 or 0, but will in the case that input weights are assigned first.
        outputlayer = []
        for i in range(outputs): # I'm going to refer *explicitly* to the remaining nodes inside the lookup. I believe abstracting this away will cause me serious problems later.
            outputlayer.append( (layers * width) + i )
        for i in outputlayer:
            tempweights = {}
            for node in layerlast:
                tempweights[node] = float( f"{(randrange(-100000, 100000) * 0.00001):.5f}" )
            connectManyToOne(obj, layerlast, i, weights=tempweights, checkData=False)
    #'''

    obj.resetCurrents()

    #print(f"Network after linking outputs:\n{printrawnetwork()}")
    return None

''' ----------- DATA VALIDATION, FILE SAVING, FILE LOADING ---------- '''

'''
 os.stat(path, *, dir_fd=None, follow_symlinks=True)

    Get the status of a file or a file descriptor. Perform the equivalent of a stat() system call on the given path.
    path may be specified as either a string or bytes – directly or indirectly through the PathLike interface – or as an open file descriptor. Return a stat_result object.

    This function normally follows symlinks; to stat a symlink add the argument follow_symlinks=False, or use lstat().

    This function can support specifying a file descriptor and not following symlinks.

    On Windows, passing follow_symlinks=False will disable following all name-surrogate reparse points, which includes symlinks and directory junctions.
    Other types of reparse points that do not resemble links or that the operating system is unable to follow will be opened directly. When following a chain of multiple links,
    this may result in the original link being returned instead of the non-link that prevented full traversal. To obtain stat results for the final path in this case,
    use the os.path.realpath() function to resolve the path name as far as possible and call lstat() on the result. This does not apply to dangling symlinks or junction points,
    which will raise the usual exceptions.

Example:
>>> import os
>>> statinfo = os.stat('somefile.txt')
>>> statinfo
>>>   os.stat_result(st_mode=33188, st_ino=7876932, st_dev=234881026,
>>>   st_nlink=1, st_uid=501, st_gid=501, st_size=264, st_atime=1297230295,
>>>   st_mtime=1297230027, st_ctime=1297230027)
>>> statinfo.st_size
>>>   264

 os.lstat(path, *, dir_fd=None)

    Perform the equivalent of an lstat() system call on the given path. Similar to stat(), but does not follow symbolic links. Return a stat_result object.

    On platforms that do not support symbolic links, this is an alias for stat().

    As of Python 3.3, this is equivalent to os.stat(path, dir_fd=dir_fd, follow_symlinks=False).
'''

allowedChars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_', '-', ' ', '.']

# This function will validate a passed line of data into it to make sure it is usable by a network given its specific constraints. Constraints include:
#   [node count, max precision, data types, ]
def validate_data(line, mode):
    if(not isinstance(line, str) or not isinstance(mode, str)):
        raise TypeError("Invalid data passed into validate_data()! Usage: validate_data(line=str, mode=str)")

    # I'm somewhat concerned about my tendancy to favor 'logical guarantees' inside my code. For validation it's fine, just be careful with that elsewhere.

    # Upper limit for each line is determined inside of 'validate_file', if we get here just parse and validate the data against the passed type.
    match mode:
        case "connections": # Individual node data: ID, Weight
            data = line.split()
            if(len(data) != 2):
                raise AssertionError(f"Connection data has too many values!")

            id     = int(data[0])
            weight = float(data[1])

            if(id < -4294967296 or id > 4294967296):
                raise AssertionError(f"An id went beyond the 32-bit integer limit!")

            pass

        case "node-header": # Individual node data: ID, Bias, Input, Output
            data = line.split()
            if(len(data) != 4):
                raise AssertionError(f"node-header data was malformed! Too many/few data values!")

            id     = int(data[0])   # Just check for 32-bit integer limit
            bias   = float(data[1]) # Just check for 32-bit precision boundary
            inputs = float(data[2]) # Just check for 32-bit precision boundary
            output = float(data[3]) # Just check for 32-bit precision boundary

            if(id < -4294967296 or id > 4294967296):
                raise AssertionError(f"An id went beyond the 32-bit integer limit!")

            # if(bias < )
            '''
            I'm gonna be so real, I have no clue how to enforce precision limits *this once* for a single value, let alone repeatedly for a whole network at runtime.
            Huge skill issue on my end probably, but until I have a decent answer I'm just gonna let whatever values are here slide. I'm pretty sure python doesn't care because hardware
                imprecision makes accuracy past a certain decimal-place impossible without special math libraries, which I'm not even using here. Ignored it goes, for now.

            Just to be clear, the above is a serious logical problem capable of creating several hard-to-detect bugs in my code through typical usage. It's far more useful to solve sooner
                rather than later. Learning how these things work with a hole like this in my code's reasoning is bound to create issues for me down the line. Please resolve this soon.
            '''
            pass

        case "endpoints":   # Incoming/Outgoing node ID Lists
            points = line.split()
            # I should probably find a way to check that each ID corresponds to an actual ID present in the network instead of *assuming it does exist during validation*.
            for i in points:
                num = int(i) # If this fails then it'll stop the program from reading the file.
                if(num < -4294967296 or num > 4294967296):
                    raise AssertionError(f"An id went beyond the 32-bit integer limit!")

            pass

        case "net-header":  # Network values: Version, Node count, Precision, Learning Rate
            data = line.split()
            if(len(data) != 4):
                raise AssertionError(f"net-header data was malformed! Too many/few data values!")
            version    = float(data[0]) # Only necessary check tbh
            nodes      = int(data[1])   # I need to check that the number isn't bigger than the bounds set inside of load (or less than zero)....
            precision  = int(data[2])   # I need to check to make sure the precision value is within the expected boundaries...
            learn_rate = int(data[3])   # I need to check to make sure the learning rate is within 32 bits of precision...

            if(nodes > 1000000000):
                raise MemoryError(f"There are too many nodes inside this network!")
            if(nodes < 0):
                raise AssertionError(f"There can't be a negative number of nodes inside a network!")
            if(precision >= 0 or precision <= -33):
                raise AssertionError(f"Precision value was not between expected boundaries! Expected range was [-1, -32] but got {precision}!")
            if(learn_rate < -4294967296 or learn_rate > 4294967296):
                raise AssertionError(f"Learn_rate value was outside the range of +-4294967296! (Hardcoded 32-bit limit)")
            pass

        case _: # "else" case
            raise AssertionError(f"Else case inside match statement triggered")
    pass

# I always have to check for non-numerical data. This immediately filters out most malicious files.
# First, check for larger than mathematically possible (given the logistics of graph building) files. This puts an upper limit on data parsing (no corrupted data, either!)
# Then, check each entry for matching key/value names where appropriate.
# Then, check each entry for matching key/value variable types.
# Repeat this process for each line of data passed into validation.
# This should account for all "reasonable" map structures. All remaining behavior should be due to map/evaluation/modification and not map building functions!
def validate_file(filename, log_errors=True, max_filesize=max_bytes):

    # This value SHOULD match that of network. If the two do not match, I will throw an error, but continue validation with a warning!
    validator_version = 0.3

    # Will validate a passed file. Useful as a standalone function, however I'll be combining these steps inside of my loader to save compute time.
    if(not isinstance(filename, str) or filename == ''):
        raise KeyError("Only pass in a string under 30 characters as the filename.")
    if(len(filename) > 30):
        raise KeyError("Only pass in a string under 30 characters as the filename.")

    period = False
    for char in filename:
        if char in allowedChars:
            if(char == '.'):
                if(period == True):
                    raise KeyError(f"For file \'{filename}\', \'{char}\' is not allowed in filenames! a")
                else:
                    period = True
            else:
                continue
        else:
            raise KeyError(f"For file \'{filename}\', \'{char}\' is not allowed in filenames!")

    ''' Make sure to check that the filename passed is not a symbolic link using stat or lstat! '''
    # Okay, now to attempt to actually validate the file

    actual_size    = 0
    do_load        = False
    try:
        actual_size = os.path.getsize(filename) # Check main file against the limit before deciding whether or not to read data.
        if(actual_size >= max_filesize):
            raise MemoryError(f"File \'{filename}\' is at or past the limit of {max_filesize} bytes, it is {actual_size} bytes!")
        do_load = True
    except FileNotFoundError:
        print(f"File \'{filename}\' not found. Cancelling validation...")
        #raise FileNotFoundError # I could raise this instead of continuing to run the program but... I'm not sure which is better.

    # Let's start with a per-line character limit based on the data I obtained from the first line... I have to implement a function for this one.
    def readtochar(fileobj, limit, char="\n"):
        strin  = ""
        data   = fileobj.read(1)
        strin += data
        while(len(strin) < limit and data != "" and data != char):
            data   = fileobj.read(1)
            strin += data

        return strin

    if(do_load): # If we get here the file is *probably* safe to open and read data from.

        f = open(filename, "r", encoding="utf-8")
        modelID = readtochar(f, 31)

        if(len(modelID) == 31 and modelID[31] != "\n"):
            raise AssertionError("ModelID was too long!")
        elif(len(modelID) < 31 and modelID[len(modelID) - 1] != "\n"):
            raise AssertionError("ModelID was malformed!")
        for char in modelID[:-1]:
            if char in allowedChars:
                continue
            else:
                raise KeyError("Invalid char found in modelID!")

        # Read network data (3 lines)
        data_raw = readtochar(f, 33) # 7-char ver (including '.'), 10-char node count (32-bit limit), 3-char precision (max 32: '-32'), 11-char learn rate (32-bit limit, positive and negative)
        validate_data(data_raw, "net-header")
        data = data_raw.split()
        file_ver   = float(data[0])
        node_count = int(data[1])
        precision  = int(data[2])
        learn_rate = int(data[3])

        max_points_characters = 12 * node_count # How many characters should never be passed for nodes connected line. (10-digits + 1 negative sign + 1 space/newline = 12 per node connected)
        discovered = set()                      # Used to check if node_count was an accurate measurement.

        if(validator_version != file_ver):
            print(f"{'\033[91m'}WARNING:{'\033[94m'} Validator version does not match the network version! Please don't assume all errors are real or that all data checked is valid!{'\033[0m'}")

        data_raw = readtochar(f, max_points_characters)
        validate_data(data_raw, "endpoints")

        data_raw = readtochar(f, max_points_characters)
        validate_data(data_raw, "endpoints")

        data_raw = readtochar(f, 1)
        if(data_raw != '\n'):
            print(f"Line 4 should\'ve only had a newline character! It instead had \'{data_raw}\'!")
            raise AssertionError

        def checkheader(fileobj):
            line = readtochar(fileobj, 77)
            print(f"{line[:-1]}")
            validate_data(line, "node-header")
        def checkinc(fileobj):
            line = readtochar(fileobj, max_points_characters)
            print(f"{line[:-1]}")
            validate_data(line, "endpoints")
            nodelist = []
            for i in line.split():
                nodelist.append(int(i))
                discovered.add(int(i))
            return nodelist
        def checkout(fileobj):
            line = readtochar(fileobj, max_points_characters)
            print(f"{line[:-1]}")
            validate_data(line, "endpoints")
            nodelist = []
            for i in line.split():
                nodelist.append(int(i))
                discovered.add(int(i))
            #return nodelist # Uncomment this if weights are ever stored on the sending node instead of receiveing node.
        def checkweights(fileobj, num_incoming):
            line = readtochar(fileobj, 33)
            if(num_incoming == 0):
                readtochar(fileobj, 1)
            else:
                for i in range(num_incoming):
                    print(f"{line[:-1]}")
                    validate_data(line, "connections")
                    line = readtochar(fileobj, 33)
        def check_node(fileobj):
            checkheader(fileobj)
            num_incoming = len(checkinc(fileobj))
            checkout(fileobj)
            checkweights(fileobj, num_incoming)

        check_node(f) # Still doesn't check every node in a file, but it's reading one node fine.

    pass

def save(obj=None, filename="temp.json", overwrite=None): # Write a network to a file. Leaves out activation, evaluation, and solver functions!
    # First, I need to make sure I'm not allowing arbitrary filesystem traversal. A char limit and bans should help somewhat, but symbolic links are still unaccounted for.
    if(not isinstance(filename, str) or filename == ''):
        raise KeyError("Only pass in a string under 30 characters as the filename.")
    if(len(filename) > 30):
        raise KeyError("Filename cannot be over 30 characters long!")

    period = False
    for char in filename:
        if char in allowedChars:
            if(char == '.'):
                if(period == True):
                    raise KeyError(f"For file \'{filename}\', \'{char}\' is not allowed in filenames! a")
                else:
                    period = True
            else:
                continue
        else:
            raise KeyError(f"For file \'{filename}\', \'{char}\' is not allowed in filenames!")

    ''' Make sure to check that the filename passed is not a symbolic link using stat or lstat! '''

    if(len(obj.lookup) > 1000000000):
        raise MemoryError(f"There are too many nodes in the network! I dunno how we even got this far LMAO")

    # Now actually attempt to save the file.

    obj.resetCurrents()

    map_data = map_attributes(obj)
    nav_data = nav_attributes(obj)
    f = None

    # Sorry, I'm not rewriting this 3 seperate times every time I decide to change how save files are structured, absolutely fucking not.
    def save_format():
        f = open(filename, "w", encoding="utf-8") # Doing this over and over creates a race condition where the file I'm writing to could be a different file for subsequent calls.

        # Writing the modelID into its own line as it could cause problems if located elsewhere...
        tempstr = ""
        namelen = len(map_data["modelID"])
        index   = 0
        while(index < 30 and len(tempstr) < 30 and index < namelen):
            char = map_data["modelID"][index]
            if char in allowedChars:
                index   += 1
                tempstr += char
            else:
                index += 1
                pass # Skip the invalid character and go to the next one.
        f.write(f"{tempstr}\n")

        tempstr = ""
        for key in map_data: # This is fairly straightforward. I only need to skip the modelID key...
            if(key != "modelID"):
                tempstr += f"{map_data[key]} "
        f.write(f"{tempstr[:-1]}\n")
        tempstr = ""
        for key in nav_data: # Currently, only the start and end node ids are stored inside of nav_data. If that changes, this part of the function will need to change with it.
            for id in nav_data[key]:
                tempstr += f"{id} "
            if(len(nav_data[key]) == 0):
                tempstr += "\n"
            else:
                tempstr = f"{tempstr[:-1]}\n"
        f.write(f"{tempstr}\n")

        for key in obj.lookup:
            node_data = node_attributes(obj.lookup[key])
            statickeys = ["id", "bias", "inputs", "output"]
            tempstr = ""
            for data in statickeys:
                tempstr += f"{node_data[data]} "
            tempstr = f"{tempstr[:-1]}\n"
            f.write(tempstr)

            tempstr = ""
            for startID in node_data["inc"]:
                tempstr += f"{startID} "
            f.write(f"{tempstr[:-1]}\n")
            tempstr = ""
            for endID in node_data["out"]:
                tempstr += f"{endID} "
            f.write(f"{tempstr[:-1]}\n")

            tempstr = ""
            for weight in node_data["weights"]:
                value = node_data["weights"][weight]
                tempstr += f"{weight} {value}\n"
            if (len(tempstr) == 0):
                tempstr += '\n'
            tempstr += '\n'
            f.write(tempstr)

        f.close()

    try:
        f = open(filename, "x", encoding="utf-8")
        f.close()

        print(f"{'\033[94m'}Saving object to {'\033[95m'}{filename}{'\033[94m'}!{'\033[0m'}")
        save_format()

    except FileExistsError:
        if(overwrite == True): # I guess the user just doesn't care about their old data for some reason. Nice to have this option for testing, at least.
            print(f"{'\033[94m'}Overwriting {'\033[95m'}\'{filename}\'{'\033[94m'} with network {'\033[95m'}\'{obj.modelID}\'{'\033[94m'}...{'\033[0m'}")
            save_format()

        elif(overwrite == False):
            print(f"{'\033[94m'}Keeping original {'\033[95m'}\'{filename}\'{'\033[94m'} and aborting overwrite...{'\033[0m'}")
        else:                  # The default option... confirm whether or not to overwrite old data at runtime.
            userinput = ''
            print("{'\033[93m'}Save file already exists! Overwrite old {'\033[95m'}\'{filename}\'{'\033[94m'} with network {'\033[95m'}\'{obj.modelID}\'{'\033[94m'}? (y/n){'\033[0m'}")
            userinput = input()
            if(len(userinput) > 1):
                print("{'\033[094m'}User input wasn't y, keeping original file and aborting save...{'\033[0m'}")
            userinput = userinput.lower()
            if(userinput == 'y'):
                save_format()
            else:
                print("{'\033[094m'}User input wasn't y, keeping original file and aborting save...{'\033[0m'}")


def load(filename, obj, validate=True, max_filesize=max_bytes): # Extract network information from a file. Gonna have to safely rederive reward, activation, and descent functions!
    # First, I need to make sure I'm not allowing arbitrary filesystem traversal. A char limit and bans should help somewhat, but symbolic links are still unaccounted for.
    if(not isinstance(filename, str) or filename == ''):
        raise KeyError("Only pass in a string under 30 characters as the filename.")
    if(len(filename) > 30):
        raise KeyError("Only pass in a string under 30 characters as the filename.")
    if(not isinstance(obj, Network)):
        raise ValueError("Only pass in a Network object as the obj!")

    period = False
    for char in filename:
        if char in allowedChars:
            if(char == '.'):
                if(period == True):
                    raise KeyError(f"For file \'{filename}\', \'{char}\' is not allowed in filenames! a")
                else:
                    period = True
            else:
                continue
        else:
            raise KeyError(f"For file \'{filename}\', \'{char}\' is not allowed in filenames!")

    ''' Make sure to check that the filename passed is not a symbolic link using stat or lstat! '''
    # Okay, now to attempt to actually load the file

    actual_size    = 0
    do_load        = False
    try:
        actual_size = os.path.getsize(filename) # Check main file against the limit before deciding whether or not to read data.
        if(actual_size >= max_filesize):
            raise MemoryError(f"File \'{filename}\' is at or past the limit of {max_filesize} bytes, it is {actual_size} bytes!")
        do_load = True
    except FileNotFoundError:
        print(f"File \'{filename}\' not found. Aborting load...")
        #raise FileNotFoundError # I could raise this instead of continuing to run the program but... I'm not sure which is better.

    if(do_load):
        if(validate == False): # Even though I'm "not validating" anything, I need to ensure the program doesn't read arbitrary save files. Certain limits *must* be enforced!
            # Reset all informational values inside object to default value...
            default_values = Network()
            obj.version       = default_values.version
            obj.lookup        = default_values.lookup
            obj.start         = default_values.start
            obj.end           = default_values.end
            obj.currents      = default_values.currents
            obj.currentDepth  = 0
            obj.base_modifier = 0

            # I'm going to need one value to make sure right away that reading data from this file won't cause serious problems...
            currentVer = 0.3

            f = open(filename, "r", encoding="utf-8")

            actualID = f.readline().strip()
            if(len(actualID) >= 31):
                raise RuntimeError(f"Invalid modelID found on line 1! It was too long!")
            for char in actualID:
                if(char not in allowedChars):
                    raise RuntimeError(f"Invalid modelID found on line 1! It had an invalid character!")
            obj.modelID = actualID

            # The comparisons implicity check for datatype compatibility as well as explicitly checking boundaries. The program should stop itself if it finds something it doesn't like.
            map_data = f.readline().split()
            ''' I'm currently expecting 4 values, "{version} {nodeCount} {base_precision} {learning_rate}" '''
            # Since I'm not going to verify file structure integrity, I decided I'll hard crash the program with an error if the necessary data to reconstruct a network isn't there.
            #   I can do this with functions I know will cause errors (ex: int(), float()) and checks for incorrect data boundaries.
            if(len(map_data) != 4):
                raise RuntimeError(f"Improper data fields found in the second line of file '{filename}'!")

            if (float(map_data[0]) != currentVer):
                raise RuntimeError(f"Version mismatch! Expected {currentVer}, got {map_data[0]}! Aborting to protect your data!")
            obj.version = currentVer

            num_nodes = int(map_data[1])
            limit = 1000000000
            if(num_nodes >= limit): # A billion nodes might actually hard crash my personal computer lmaoooo
                raise RuntimeError(f"Too many nodes are present inside the given network! Should be below {limit}, but the cited count was {num_nodes} nodes!")

            bit_precision = int(map_data[2])
            if(bit_precision > 0 or bit_precision < -32): # I personally think 32-bit precision is logistically fucking absurd so I'm drawing the line there.
                raise RuntimeError(f"Precision cannot be a positive integer nor indicate higher than 32-bits of precision! Expected range is [-1, -32] but got {bit_precision}!")
            obj.base_precision = bit_precision

            learn_rate = float(map_data[3])
            if(learn_rate < 0 or learn_rate > 4294967296): # Enforcing the above limitation...
                # Just to be clear, 2^32 = 4294967296, I won't be using more than 16 bit precision but I'm drawing the line there.
                raise RuntimeError(f"Learning rate isn't allowed to be less than 0 or be more precise than 32 bits! Expected range: [0, 4294967296], got {learn_rate}!")
            obj.learning_rate  = learn_rate

            # I have to do this since the values inside the file may be different from an initialized object.
            obj.recalcPrecision()

            # The next line is for all the input nodes...
            #print(f"Inputs:")
            nodes = f.readline().split()
            #print(nodes)
            for num in nodes:
                obj.start.append(int(num)) # int() implicity checks datatype compatibility. Failures indicate corrupted or invalid data.

            # The next line is for all the output nodes...
            #print(f"Outputs:")
            nodes = f.readline().split()
            #print(nodes)
            for num in nodes:
                obj.end.append(int(num)) # int() implicity checks datatype compatibility. Failures indicate corrupted or invalid data.

            char = f.read(1) # Skipping what's supposed to be a newline so that I can...
            if(char != "\n"):
                raise RuntimeError("Incorrect data format found at line 5! Expected sentinel newline character, got data instead!")

            # ...Read in all node data!
            def readheader(fileobj):
                headerline = fileobj.readline().split()
                return headerline
            def readincoming(fileobj):
                line = fileobj.readline().split()
                incomingnodes = []
                for i in range(len(line)):
                    incomingnodes.append(int(line[i]))
                return incomingnodes
            def readoutgoing(fileobj):
                line = fileobj.readline().split()
                outgoingnodes = []
                for i in range(len(line)):
                    outgoingnodes.append(int(line[i]))
                return outgoingnodes
            def readweights(fileobj, num_incoming):
                connections = {}
                line = fileobj.readline().split()
                if(num_incoming == 0):
                    fileobj.readline()
                else:
                    for i in range(num_incoming): # I need to check whether or not the data which was read in actually fits the weight format (ID weight-value).
                        connections[int(line[0])] = float(line[1])
                        line = fileobj.readline().split()
                return connections

            def readnode(fileobj):
                data = []

                data.append(readheader(fileobj))
                data.append(readincoming(fileobj))
                data.append(readoutgoing(fileobj))
                data.append(readweights(fileobj, len(data[1])))

                newnode = None
                if(data != [[], [], [], {}]):
                    newnode = Neuron(id=int(data[0][0]), bias=float(data[0][1]), inputs=float(data[0][2]), output=float(data[0][3]), inc=data[1], out=data[2], weights=data[3])
                else:
                    pass # Leave 'newnode' alone, at None.
                return newnode

            if(num_nodes > 0):
                node = readnode(f)
                while(node != None):
                    #print(f"node=\n{neuron_format(node)}\nnew cycle")
                    obj.lookup[node.id] = node
                    node = readnode(f)
            else:
                pass # Nothing more to read at this point.

            obj.resetCurrents()
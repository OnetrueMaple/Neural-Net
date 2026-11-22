# Simple To-Do list. Just modify this and print it out or something, idk. Who cares.
def printToDo():
    divider = "--------------------------------------------------------------------------------------------------------------"
    items = []
    items.append("Break apart other items in list into smaller tasks. This is important, it keeps my workflow relatively consistent, so don't downplay it. No real end rule for this one.")
    items.append("Change up the comments or structure of the code to more closely reflect principles and concepts you find while working. No real end rule for this one.")
    items.append("Check over parts of the testing program from time to time and try to find anything that might not be covered in my tests. No real end rule for this one.")
    items.append("Verify/Fix descent functionality for when there are reward functions and/or multiple outputs.")
    items.append("Keep searching for when/how it would be appropriate to add nodes to a network.")
    # The two above are actually related... adding even a single node between all inputs and outputs breaks the reward function which does what it's supposed to when that node isn't there. Fun!
    items.append("Allow outputs to represent probabilities. My math will suffer here...")
    items.append("Printing network data should follow eval order and data shown should be configurable (for ease of testing)")

    strin = f"{'\033[90m'}{divider}\n{'\033[93m'}To-Do List (No real order, besides obvious dependency chains):\n"
    for i in range(len(items)):
        temp = f"{'\033[95m'}  {i + 1}. {'\033[94m'}{items[i]}\n"
        strin += temp
    print(f"{strin[:-1]}")
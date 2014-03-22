'''
Created on Dec 4th 2013

@author: Zhang, Jinhui

Email: jinhzhan@indiana.edu
'''

import os
import time
import csv
import cPickle as pickle
from pydoc import deque
from heapq import heappush, heappop
goalState = []

# Uninformed Search - BFS
# This part is not used in homework 6
def uninformedSearch(queue, limit, numRuns):

    # List to keep track of visited nodes
    visited = []

    # Get first list of states in queue
    path = deque([queue])

    # cloning path
    temp_path = [queue]

    # If no more states available then return false
    if queue == []:
        print "No Solution Exists"
        return
    elif testProcedure(queue[0]):
	# Check state is goal state and print output
        outputProcedure(numRuns, queue[0])
    elif limit == 0:
        print "Limit reached"
        return
    
    q = deque(queue)
                
    while len(q) > 0:     
	# Get first element in queue
        n = q.popleft()
        
        temp_path = path.popleft()
        if n not in visited:
	    # add node to visited nodes
            visited.append(n)
            limit -= 1
            numRuns += 1

	    
            if queue == []:     # check for elements in queue
	        print "No Solution Exists"
                return 
            elif testProcedure(n):      # check if reached goal state 
                outputProcedure(numRuns, temp_path)
                return temp_path
            elif limit == 0:
	        print "Limit reached"
                return
            
            successors = expandProcedure(n)     #find successors of current state
            for succ in successors:
                new_path = temp_path + [succ]
                path.append(new_path)
			
            q.extend(successors)      # Add successors in queue
    print "No Solution Exists"                
    return


# Informed search - A*
def informedSearch(initialState, goal, limit, numRuns, choice):
    # Reset the goal state
    global goalState
    goalState = goal
    # List to keep track of visited nodes
    visited = []

    # path of the tree
    temp_path = [initialState[0]]

    # If empty state, return
    if initialState == []:
        print "No Solution Exists"
        return 
    elif testProcedure(initialState[0]):
        # Check state is goal state and print output
        # outputProcedure(numRuns, initialState[0])
        return numRuns, [initialState[0]]
    elif limit == 0:
        # If limit reached return
        print "Limit reached"
        return
    
    # calculate g(n),h(n) and f(n) for the root node
    g_n = 0
    h_n = heuristicFunction(initialState[0], choice)
    f_n = g_n + h_n

    # implement a heap
    heap = []
    
    # push the root, path as well as its f(n) into the heap
    heappush(heap, (f_n, [initialState[0], temp_path]))
    
    while len(heap) > 0:
        # Pop node with highest f(n)
        (cost_unwanted, nodeList) = heappop(heap)

        # Glean state and path to state
        n = nodeList[0]
        temp_path = nodeList[1]

        if n not in visited:
            visited.append(n)   # Append state to visited state
            limit -= 1
            numRuns += 1
            if testProcedure(n):    # Test if goal state
                # outputProcedure(numRuns, temp_path)
                return numRuns, temp_path    # Return the solution path and store as one case
            elif limit == 0:    # Test if limit reached
                print "Limit reached"
                return
            
            successors = expandProcedure(n) # Generate successors
            for succ in successors:
                # Calculate f_n for the successor
                g_n = len(temp_path)-1
                h_n = heuristicFunction(succ, choice)
                f_n = g_n + h_n;

                # Push f(n), successor and path to successor to the heap
                heappush(heap, (f_n, [succ, (temp_path + [succ])]))

    print "No Solution Exists"                
    return

# Calculate the manhatten distance between two states
def manhatten(currentState, goalState):
    # This should ideally work for any goal statedefined in the program
        posTilesGoal = dict()
        posTilesState = dict()

        # Find position of each node and add to dict ("value":position)
        # for both goal state and current state
        for i in range(0,len(goalState)):
            posTilesGoal[goalState[i]] = i;
            posTilesState[currentState[i]] = i;

        # Counter for sum of manhatten distances
        manhattenDst = 0

        # For each value in current state, find the number of blocks away from
        # it's position in goal state and sum it up
        for i in range(1,len(goalState)):
            # For pairs on the right corner and left corner, we need two additional moves
            if ((posTilesGoal[i] == 2 and posTilesState[i] == 3) or \
                (posTilesGoal[i] == 3 and posTilesState[i] == 2) or \
                (posTilesGoal[i] == 2 and posTilesState[i] == 6) or \
                (posTilesGoal[i] == 6 and posTilesState[i] == 2) or \
                (posTilesGoal[i] == 5 and posTilesState[i] == 6) or \
                (posTilesGoal[i] == 6 and posTilesState[i] == 5)) :
                posTilesGoal[i] += 6
                    
            diff = abs(posTilesGoal[i]-posTilesState[i])
            
            manhattenDst += (diff/3) + (diff%3)
        return manhattenDst

def heuristicFunction(currentState, choice):
    
    if choice == "one": # Misplaced Tile hueristic
        noTilesMismatch = 0;
        for i in range(0,len(goalState)):
            # Find mispalced tiles and add to counter
            if (goalState[i] != currentState[i]):
                noTilesMismatch += 1
        return noTilesMismatch

    elif choice == "two":   # Manhatten Distance
        manhattenDst = manhatten(currentState, goalState)
        return manhattenDst
        
# Check if the queue is the same as goalState
def testProcedure(queue):
    if (queue == goalState):
        return True
    else:
        return False
     
# Print the path from initialState to goalState
def outputProcedure(numRuns, path):
    print "Total number of runs=", numRuns
    print "Path Cost=", len(path)-1

    idx = 0   
    for i in path:
        
        print "Game State: ", idx
        idx += 1
        print (" " if i[0] == 0 else i[0]) , " " , (" " if i[1] == 0 else i[1]) , " " , (" " if i[2] == 0 else i[2]) 
        print (" " if i[3] == 0 else i[3]) , " " , (" " if i[4] == 0 else i[4]) , " " , (" " if i[5] == 0 else i[5]) 
        print (" " if i[6] == 0 else i[6]) , " " , (" " if i[7] == 0 else i[7]) , " " , (" " if i[8] == 0 else i[8]), "\n"
        
        
# Successor function        
def expandProcedure(state):
    successors = []
    blankPos = 0
    adjacent = []
    # Get position of blank tile
    for i in range(len(state)):
        if state[i] == 0:
            blankPos = i
	
    # Check whether left(right?) edge tiles
    if (blankPos % 3 != 2):
        nextPos = blankPos + 1
        adjacent.append(nextPos)

    # Check whether right(left?) edge tiles
    if (blankPos % 3 != 0):
        prev = blankPos - 1
        adjacent.append(prev)

    # Check up tile
    if (blankPos > 2):
        up = blankPos - 3
        adjacent.append(up)

    # Check down tile
    if (blankPos < 6):
        down = blankPos + 3
        adjacent.append(down)

    succ = state
    for pos in adjacent:
        succ = list(state)
		
	# Swap tiles and make new state. Add to successor
        if pos >= 0 and pos <= 8:
            succ[blankPos], succ[pos] = succ[pos], succ[blankPos]
            successors.append(succ)
    return successors
    
# Create state from initial and goal state
def makeState(nw, n, ne, w, c, e, sw, s, se):
    statelist = [nw, n, ne, w, c, e, sw, s, se]
    for i in range(len(statelist)):
	# Replace blank with 0
        if statelist[i] == "blank":
            statelist[i] = 0
    return statelist
    

def testInformedSearch(initialState, goalState, limit):
    # print "\nHueristic: No of mispalced Tiles"
    # t1 = time.time()
    # informedSearch ([initialState], goalState, limit, 0, "one")
    # print "Time taken for Informed Search(Misplaced Tiles): ", (time.time()-t1) ," Seconds"
    print "\nHueristic: Manhatten Distance"
    t = time.time()
    numRuns, path = informedSearch ([initialState], goalState, limit, 0, "two")
    t1 = time.time()
    print "Time taken for Informed Search(Manhatten Distance): ", (t1 - t) ," Seconds"
    return t1 - t, numRuns

def testUninformedSearch(initialState, goalState, limit):
    uninformedSearch ([initialState], limit, 0)

"""
One class for one case. Used to representing cases. It contains: 
Attributes:
    initialState
    goalState
    path
Mathod:
    getInitialState()
    getGoalState()
    getPath(): get the path from initialState to goalState
"""
class Case:

    def __init__(self, initialState, goalState, path):
        self.initialState = initialState
        self.goalState = goalState
        self.path = path

    def getInitialState(self):
        return self.initialState

    def getGoalState(self):
        return self.goalState

    def getPath(self):
        return self.path

# Calculate the similarity between two states using manhatten distance
def similarity(state1, state2):
    manhattenDst = manhatten(state1, state2)
    return manhattenDst

# Get all the cases from casebase
def getCases():
    case_file = open("casebase", "rb")
    pick = pickle.Unpickler(case_file)
    case_set = []
    while True:
        try:
            data = pick.load()
            case_set.append(data)
        except EOFError: # If there is no more cases, break
            break
    case_file.close()
    return case_set

# Initialization of casebase       
def init_casebase():
    case_file = open("casebase", "w")
    pick = pickle.Pickler(case_file)
    # First group of test cases - should have solutions with depth <= 5
    initialState1 = makeState(2, "blank", 3, 1, 5, 6, 4, 7, 8)
    initialState2 = makeState(1, 2, 3, "blank", 4, 6, 7, 5, 8)
    initialState3 = makeState(1, 2, 3, 4, 5, 6, 7, "blank", 8)
    initialState4 = makeState(1, "blank", 3, 5, 2, 6, 4, 7, 8)
    initialState5 = makeState(1, 2, 3, 4, 8, 5, 7, "blank", 6)


    # Second group of test cases - should have solutions with depth <= 10
    initialState6 = makeState(2, 8, 3, 1, "blank", 5, 4, 7, 6)
    initialState7 = makeState(1, 2, 3, 4, 5, 6, "blank", 7, 8)
    initialState8 = makeState("blank", 2, 3, 1, 5, 6, 4, 7, 8)
    initialState9 = makeState(1, 3, "blank", 4, 2, 6, 7, 5, 8)
    initialState10 = makeState(1, 3, "blank", 4, 2, 5, 7, 8, 6)


    # Third group of test cases - should have solutions with depth <= 20
    initialState11 = makeState("blank", 5, 3, 2, 1, 6, 4, 7, 8)
    initialState12 = makeState(5, 1, 3, 2, "blank", 6, 4, 7, 8)
    initialState13 = makeState(2, 3, 8, 1, 6, 5, 4, 7, "blank")
    initialState14 = makeState(1, 2, 3, 5, "blank", 6, 4, 7, 8)
    initialState15 = makeState("blank", 3, 6, 2, 1, 5, 4, 7, 8)
    goalState = makeState(1,2,3,4,5,6,7,8,"blank")

    initial_set = [initialState1, initialState2, initialState3, 
                    initialState4, initialState5, initialState6, 
                    initialState7, initialState8, initialState9, 
                    initialState10, initialState11, initialState12, 
                    initialState13, initialState14, initialState15]

    for initState in initial_set:
        # Using the second heuristic function(manhatten distance) to find the path solution
        numRuns, path = informedSearch([initState], goalState, 200000, 0, "two")
        case = Case(initState, goalState, path)
        pick.dump(case)

    case_file.close()

# Find the case with the lowest similarity value
def find_similar_case(initialState, goalState, case_set):
    min_res = 10000
    print "Cases in casebase(initialState, goalState, similar score):"
    for case in case_set:
        res = similarity(initialState, case.getInitialState()) + similarity(goalState, case.getGoalState())
        print str(case.getInitialState()) + " " + str(case.getGoalState()) + " " + str(res)
        if min_res > res:
            min_res = res
            min_case = case
    if min_res > 5: # If the similarity value is greater than 5, return nothing and find solution from scratch
        return None, None
    return min_res, min_case

# Case-based Search
def caseBasedSearch(initialState, goalState):
    # If casebase hasn't been generated, generate it
    if "casebase" not in os.listdir("."):
        init_casebase()

    print "Current initialState: " + str(initialState)
    print "Current goalState: " + str(goalState)
    if initialState == goalState:
        numRuns = 0
        path1 = [initialState]
    else:
        # Case retrival
        print "\nCase retrieval step: "
        case_set = getCases()
        score, case = find_similar_case(initialState, goalState, case_set)
        if case == None:
            # Scratch
            print "\nThere is no similar case in the base"
            numRuns, path1 = informedSearch([initialState], goalState, 200000, 0, "two")
        elif score == 0:
            # If the old case is exactly the same as the new one
            print "\nThe similar prior case is(exactly the same): "
            print "Initial State: " + str(case.getInitialState())
            print "Goal State: " + str(case.getGoalState())
            print "Similar score: " + str(score)
            path1 = case.getPath()
            numRuns = 0
        else:
            # Case adaptation
            print "\nThe similar prior case is: "
            print "Initial State: " + str(case.getInitialState())
            print "Goal State: " + str(case.getGoalState())
            print "Similar score: " + str(score)
            numRuns1, path1 = informedSearch([initialState], case.getInitialState(), 200000, 0, "two")
            print "\nCase adaptation: "
            print "Path from new initialState to old initialState: "
            outputProcedure(numRuns1, path1)
            path2 = case.getPath()
            numRuns3, path3 = informedSearch([case.getGoalState()], goalState, 200000, 0, "two")
            print "\nPath from old goalState to new goalState"
            outputProcedure(numRuns3, path3)
            path1.extend(path2[1:-1])
            path1.extend(path3)
            numRuns = numRuns1 + numRuns3
    print "\nThe whole solution for new case: "
    outputProcedure(numRuns, path1)

    # Case storage
    case_file = open("casebase", "a")
    pick = pickle.Pickler(case_file)
    case = Case(initialState, goalState, path1)
    pick.dump(case)
    case_file.close()
    return numRuns

def testCaseBasedSearch(init, goal):
    print "Case-based Search: "
    t = time.time()
    numRuns = caseBasedSearch(init, goal)
    t1 = time.time()
    print "Time taken for Case-based Search: ", (t1 - t) ," Seconds\n\n"
    return t1 - t, numRuns
    
# Main()
if __name__ == "__main__":
    # Test cases
    # Dissimilar, hard
    initialState16 = makeState(2, 6, 5, 4, "blank", 3, 7, 1, 8)
    initialState17 = makeState(3, 6, "blank", 5, 7, 8, 2, 1, 4)
    initialState18 = makeState(1, 5, "blank", 2, 3, 8, 4, 6, 7)
    initialState19 = makeState(2, 5, 3, 4, "blank", 8, 6, 1, 7)
    initialState20 = makeState(3, 8, 5, 1, 6, 7, 4, 2, "blank")
    # Similar, easy
    initialState21 = makeState(2, 3, 6, 1, 5, "blank", 4, 7, 8)
    initialState22 = makeState(1, 2, 3, 4, 6, "blank", 7, 5, 8)
    initialState23 = makeState(1, "blank", 3, 4, 2, 6, 7, 5, 8)
    initialState24 = makeState(1, 3, "blank", 5, 2, 6, 4, 7, 8)
    initialState25 = makeState(1, 2, 3, 4, 8, 5, "blank", 7, 6)
    # Dissimilar, easy
    initialState26 = makeState(4, 1, 2, 7, "blank", 3, 8, 5, 6)
    initialState27 = makeState(4, 1, 3, "blank", 2, 6, 7, 5, 8)
    initialState28 = makeState("blank", 2, 3, 1, 5, 6, 4, 7, 8)
    initialState29 = makeState("blank", 2, 3, 1, 4, 5, 7, 8, 6)
    initialState30 = makeState(2, "blank", 3, 1, 4, 6, 7, 5, 8)
    # Similar, hard
    initialState31 = makeState(2, 6, 5, 4, 3, "blank", 7, 1, 8)
    initialState32 = makeState(3, "blank", 6, 5, 7, 8, 2, 1, 4)
    initialState33 = makeState(1, 5, 8, 2, 3, "blank", 4, 6, 7)
    initialState34 = makeState(2, 5, 3, "blank", 4, 8, 6, 1, 7)
    initialState35 = makeState(3, 8, 5, 1, 6, "blank", 4, 2, 7)
    goalState = makeState(1,2,3,4,5,6,7,8,"blank")

    test_cases = [initialState16, initialState17, initialState18, initialState19, 
                  initialState20, initialState21, initialState22, initialState23, 
                  initialState24, initialState25, initialState26, initialState27, 
                  initialState28, initialState29, initialState30, initialState31, 
                  initialState32, initialState33, initialState34, initialState35]

    # Test case based reasoning using test cases above, and write the time and numRuns results into a csv file
    with open("casebased.csv", "wb") as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        count = 0
        for init_state in test_cases:
            count += 1
            t, numRuns = testCaseBasedSearch(init_state, goalState)
            print t, numRuns
            writer.writerow([count, t, numRuns])
    
    # Test informed search as comparison, and write the time and numRuns results into a csv file
    with open("informed.csv", "wb") as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        count = 0
        for init_state in test_cases:
            count += 1
            t, numRuns = testInformedSearch(init_state, goalState, 200000)
            writer.writerow([count, t, numRuns])

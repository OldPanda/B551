'''
Created on Oct 5th 2013

@author: Shreya, Mukesh
'''

import time
from pydoc import deque
from heapq import heappush, heappop
goalState = []

# Uninformed Search - BFS
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
                return
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
def informedSearch(initialState, limit, numRuns, choice):
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
        outputProcedure(numRuns, initialState[0])
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
                outputProcedure(numRuns, temp_path)
                return
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

def heuristicFunction(currentState, choice):
    
    if choice == "one": # Misplaced Tile hueristic
        noTilesMismatch = 0;
        for i in range(0,len(goalState)):
            # Find mispalced tiles and add to counter
            if (goalState[i] != currentState[i]):
                noTilesMismatch += 1
        return noTilesMismatch

    elif choice == "two":   # Manhatten Distance
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
        
def testProcedure(queue):
    if (queue == goalState):
        return True
    else:
        return False
     
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
	
    # Check whether left edge tiles
    if (blankPos % 3 != 2):
        nextPos = blankPos + 1
        adjacent.append(nextPos)

    # Check whether right edge tiles
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
            temp = succ[blankPos]
            succ[blankPos] = succ[pos]
            succ[pos] = temp
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
    print "\nHueristic: No of mispalced Tiles"
    t1 = time.time()
    informedSearch ([initialState], limit, 0, "one")
    print "Time taken for Informed Search(Misplaced Tiles): ", (time.time()-t1) ," Seconds"
    print "\nHueristic: Manhatten Distance"
    t2 = time.time()
    informedSearch ([initialState], limit, 0, "two")
    print "Time taken for Informed Search(Manhatten Distance): ", (time.time()-t2) ," Seconds"
    return

def testUninformedSearch(initialState, goalState, limit):
    uninformedSearch ([initialState], limit, 0)
        
# Main()
if __name__ == "__main__":
    # initialState = makeState("blank", 5, 3, 2, 1, 6, 4, 7, 8)
    initialState = makeState(1, 2, 3, 4, 5, 6, 8, 7, "blank")
    goalState = makeState(1,2,3,4,5,6,7,8,"blank")

    print "Uninformed Search"
    t1 = time.time()
    testUninformedSearch(initialState, goalState, 200000)
    t2 = time.time()
    print "Time taken for Uninformed Search: ", (t2-t1), " Seconds"
    
    print "\n\nInformed Search"
    testInformedSearch(initialState, goalState, 200000)

    

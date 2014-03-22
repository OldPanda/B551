'''
Author: Jinhui Zhang
Course: Elements of AI
Username: jinhzhan
Email: jinhzhan@indiana.edu
'''

import time

class State:
	'''
	A class used to denote states of the game
	'''
	def __init__(self, tile_order):
		'''
		Initialization with tile_order which denotes the 2-dimension game board by linear list.
		For example, if we have a state:
		2 5 3
		  1 6
		4 7 8
		then we write it as state = State([2, 5, 3, 'blank', 1, 6, 4, 7, 8])
		Class State has two variables, 
		tile_order ---- the linear shape of a state
		parent ---- a state that can generate the current state by moving blank tile one step
		'''
		self.tile_order = tile_order
		self.parent = "root" 
	
	def __eq__(self, state):
		'''
		Overide the __eq__ method for comparison between current state and the goal state
		'''
		for i in range(9):
			if self.tile_order[i] != state.tile_order[i]:
				return False
		return True
	
	def __str__(self):
		return str(self.tile_order)

	def set_parent(self, state):
		'''
		Set the parent state of the state
		'''
		self.parent = state

	def get_parent(self):
		'''
		Get the parent state of the state
		'''
		return self.parent

	def get_tile_order(self):
		'''
		Get the tile order of the state to initialize a new state which has the same state of the current state. 
		Used in mathod action(). 
		'''
		return list(self.tile_order)

	def action(self):
		'''
		Get the possible states that can be reached from the current state
		'''
		position = self.tile_order.index("blank") # find where the blank tile is
		# calculate the x, y coordinate through the position in list
		pos_x = position / 3
		pos_y = position - 3 * pos_x
		child_states = []
		# there are four directions, so do loop four times. And before exchanging the blank tile and its neighbor,
		# check if the blank tile is cross the border. If not, do the move. 
		for i in range(4):
			lst = self.get_tile_order() # the tile list used to generate new state with the same tile order
			if pos_x - 1 >= 0 and i == 0:
				# blank tile goes left
				state = State(lst)
				state.tile_order[3 * (pos_x - 1) + pos_y], state.tile_order[3 * pos_x + pos_y] = state.tile_order[3 * pos_x + pos_y], state.tile_order[3 * (pos_x - 1) + pos_y] # swap the blank tile and its left neighbor
				state.set_parent(self) # set the current state as the new state's parent
				child_states.append(state)# add the new state to a list that is going to be returned
			if pos_x + 1 <= 2 and i == 1:
				# blank tile goes right
				state = State(lst)
				state.tile_order[3 * (pos_x + 1) + pos_y], state.tile_order[3 * pos_x + pos_y] = state.tile_order[3 * pos_x + pos_y], state.tile_order[3 * (pos_x + 1) + pos_y]
				state.set_parent(self)
				child_states.append(state)
			if pos_y - 1 >= 0 and i == 2:
				# blank tile goes up
				state = State(lst)
				state.tile_order[3 * pos_x + (pos_y - 1)], state.tile_order[3 * pos_x + pos_y] = state.tile_order[3 * pos_x + pos_y], state.tile_order[3 * pos_x + (pos_y - 1)]
				state.set_parent(self)
				child_states.append(state)
			if pos_y + 1 <= 2 and i == 3:
				# blank tile goes down
				state = State(lst)
				state.tile_order[3 * pos_x + (pos_y + 1)], state.tile_order[3 * pos_x + pos_y] = state.tile_order[3 * pos_x + pos_y], state.tile_order[3 * pos_x + (pos_y + 1)]
				state.set_parent(self)
				child_states.append(state)
		return child_states
	
	def is_in_set(self, stateset):
		'''
		Check if the state is in some stateset like "frontier" or "explored"
		'''
		for item in stateset:
			if item == self:
				return True
		return False

def BFS(state, limit):
	'''
	Breadth-First Search algorithm
	'''
	if goal_test(state):
		# if the initial state is the goal state, return the solution
		return solution(state)
	# or initial the frontier and explored variables, start searching
	frontier = [state]
	explored = []
	while True:
		if len(frontier) == 0:
			# when the frontier is empty and no solution is found, this is an unsolvable problem
			return "No solution for ", str(state)
		now_state = frontier.pop(0) # get the first element in frontier and explore it
		explored.append(now_state) # label it as explored
		child_state = now_state.action() # obtain all the children from the state
		limit -= 1
		for s in child_state:
			# check each child state to see if it is the same as goal state, run out of limit, 
			# or keep checking the next. 
			if not s.is_in_set(explored) and not s.is_in_set(frontier):
				if goal_test(s):
					return solution(s)
				elif limit == 0:
					return "Limit reached"
				else:
					frontier.append(s)

def solution(state):
	'''
	According to the parent state stored in the solution state, get the path iteratively
	'''
	result = [state]
	parent = state.get_parent()
	while parent != "root":
		# add the parent state to the result list until getting to root
		result.append(parent)
		parent = parent.get_parent()
	result.reverse()
	return result

def goal_test(state):
	'''
	Checking if state is exactly the goal state. If so, return true. 
	'''
	if state == goal_state:
		return True
	else:
		return False

def makeState(nw, n, ne, w, c, e, sw, s, se):
	'''
	nw      |  NorthWest element of the puzzle
	n       |  North element of the puzzle
	ne      |  NorthEast element of the puzzle
	w       |  West element of the puzzle
	c       |  Center element of the puzzle
	e       |  East element of the puzzle
	sw      |  SouthWest element of the puzzle
	s       |  South element of the puzzle
	se      |  SouthEast element of the puzzle
	'''
	l = list([nw, n, ne, w, c, e, sw, s, se])
	state = State(l)
	return state

def testUninformedSearch(init, goal, limit):
	global goal_state
	goal_state = goal # configure the goal state
	result = BFS(init, limit) # get the solution or failure message
	if isinstance(result, str):
		# if it's a message, just print it and return
		print result
		return
	# otherwise, print the solution path
	for r in result:
		for i in range(3):
			for j in range(3):
				if r.tile_order[3 * i + j] == "blank":
					print " ",
				else:
					print r.tile_order[3 * i + j],
			print
		print "-----------------\n"
        print "Depth is", len(result)
	# return len(result)
	

goal_state = makeState(1, 2, 3, 4, 5, 6, 7, 8, "blank") # global variable "goal_state" 

goalState = makeState(1, 2, 3, 4, 5, 6, 7, 8, "blank")
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

# Fourth group of test cases - should have solutions with depth <= 50
initialState16 = makeState(2, 6, 5, 4, "blank", 3, 7, 1, 8)
initialState17 = makeState(3, 6, "blank", 5, 7, 8, 2, 1, 4)
initialState18 = makeState(1, 5, "blank", 2, 3, 8, 4, 6, 7)
initialState19 = makeState(2, 5, 3, 4, "blank", 8, 6, 1, 7)
initialState20 = makeState(3, 8, 5, 1, 6, 7, 4, 2, "blank")
initialState = [initialState1, initialState2, initialState3, initialState4, initialState5, initialState6, initialState7, initialState8, initialState9, initialState10, initialState11, initialState12, initialState13, initialState14, initialState15, initialState16, initialState18, initialState19, initialState20]
testUninformedSearch(initialState1, goalState, 2000)
'''
t = []
depth = []
for item in initialState:
	start = time.time()
	depth.append(testUninformedSearch(item, goalState, 200000))
	end = time.time()
	t.append(end - start)
	print len(t)
# print "Time elapsed:", end - start
print "time:", t
print "depth:", depth
'''


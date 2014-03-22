'''
Author: Jinhui Zhang
Username: jinhzhan
Email: jinhzhan@indiana.edu
Time: 11/03/2013
'''

import gamePlay
import sys
from copy import deepcopy

'''Set alpha and beta as global variables so that when updating them, they are changed permanently'''
alpha = -100000
beta = 100000
def get_successors(board, color):
	'''Get current situation's children nodes'''
	return [(i, j) for i in range(8) for j in range(8) if gamePlay.valid(board, color, (i, j))]

def evaluation(board, color):
	'''Use the number of black minus white as evaluation for current situation'''
	black, white = gamePlay.score(board)
	return black - white

def max_value(board, color, depth):
	'''Calculate the max value'''
	global alpha, beta
	if gamePlay.gameOver(board) or depth == 0:
		'''If the game board is full of pieces, or reach the search depth, give the evaluation of the situation'''
		return evaluation(board, color)
	depth -= 1
	val = -100000
	next_positions = get_successors(board, color) # Get the child nodes
	next_color = gamePlay.opponent(color) # Get the opponent's color
	if len(next_positions) == 0:
		return evaluation(board, color) # If no child node, return the evaluation
	for pos in next_positions:
		tempboard = deepcopy(board) # Create a new board for mock moves
		gamePlay.doMove(tempboard, color, pos) # Do a mock move
		val = max(val, min_value(tempboard, next_color, depth))
		'''Alpha-beta pruning'''
		if val >= beta:
			return val
		alpha = max(alpha, val) # Update alpha value
	return val

def min_value(board, color, depth):
	'''Calculate the min value. The comments are the same as in max_value()'''
	global alpha, beta
	if gamePlay.gameOver(board) or depth == 0:
		return evaluation(board, color)
	depth -= 1
	val = 100000
	next_positions = get_successors(board, color)
	next_color = gamePlay.opponent(color)
	if len(next_positions) == 0:
		return evaluation(board, color)
	for pos in next_positions:
		tempboard = deepcopy(board)
		gamePlay.doMove(tempboard, color, pos)
		val = min(val, max_value(tempboard, next_color, depth))
		if val <= alpha:
			return val
		beta = min(beta, val) # Update beta value
	return val

def alpha_beta(board, color):
	'''Alpha-beta pruning'''
	next_positions = get_successors(board, color)
	if len(next_positions) == 0:
		return "pass"
	next_color = gamePlay.opponent(color)
	best_value = -100000
	best_move = (-1, -1)
	'''This for loop works as max_value(), so here starts the recursion with min_value()'''
	for pos in next_positions:
		tempboard = deepcopy(board)
		gamePlay.doMove(tempboard, color, pos)
		val = min_value(tempboard, next_color, 6) # Search depth is 6. If it is deeper, we need to wait too long for result
		if val >= best_value:
			best_value = val
			best_move = pos
	return best_move

'''The three methods below are used for greedy strategy'''
def value(board, color):
	'''Evaluate the board situation based on the number of black and white on the board'''
	black, white = gamePlay.score(board)
	if color == "W": # If agent plays white, do white minus black
		return white - black
	elif color == "B": # If agent plays black, do black minus white
		return black - white

def better_than(val1, val2, color, reversed):
	'''Compare val1 and val2'''
	if color == "W":
		retVal = val1 > val2
	else:
		retVal = val1 < val2
	if reversed:
		return not retVal
	else:
		return retVal

def simple_greedy(board, color, reversed = False):
	'''Simple greedy strategy'''
	moves = get_successors(board, color)
	if len(moves) == 0:
		return "pass"
	best = None
	for move in moves:
		new_board = deepcopy(board)
		gamePlay.doMove(new_board, color, move)
		move_value = value(new_board, color)
		if best == None or better_than(move_value, best, color, reversed):
			best_move = move
			best = move_value
		return best_move

def nextMove(board, color, time):
	'''If the rest time is more than 20 seconds, do alpha-beta pruning. Otherwise, do greedy strategy'''
	if time > 20:
		return alpha_beta(board, color)
	else:
		return simple_greedy(board, color)

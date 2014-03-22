'''
My name: Jinhui Zhang
My username: jinhzhan
'''
def print_board():
    for i in range(0, 3):
        for j in range(0, 3):
            print map[2 - i][j],
            if j != 2:
                print "|",
        print ""

def check_done():
    for i in range(0, 3):
        if map[i][0] == map[i][1] == map[i][2] != " " \
	or map[0][i] == map[1][i] == map[2][i] != " ":
            #print turn, "won!!!"
            return turn, True

        if map[0][0] == map[1][1] == map[2][2] != " " \
	or map[0][2] == map[1][1] == map[2][0] != " ":
            #print turn, "won!!!"
            return turn, True

        if " " not in map[0] and " " not in map[1] and " " not in map[2]:
            #print "Draw"
            return "", True
    
    return "", False

class Agent(object):
    '''Computer agent that can play this game with you'''
    def __init__(self, turn, opponent_turn):
        '''Initialization with the players that the agent plays and human plays'''
        self.turn = turn
        self.opponent_turn = opponent_turn
    
    def is_agent_turn(self, turn):
        '''Check if it is computer's turn'''
        if self.turn == turn:
            return True
        else:
            return False
    
    def agent_move(self):
        '''Simulate the computer and give the best position. Try to maximize each step's value of agent'''
        best_pos = 0
        best_value = 0
        for i in range(1, 10):
            Y = i / 3
            X = i % 3
            if X != 0:
                X -= 1
            else:
                X = 2
                Y -= 1
            if map[Y][X] == " ":
                map[Y][X] = self.turn
                winner, flag = check_done()
                
                # One more step and agent will win. Good, it should be the highest priority
                # Return its position and priority
                if len(winner) > 0 and flag == True:
                    map[Y][X] = " "
                    return i, 1
                
                # A draw is OK. Just with the mediate priority
                elif winner == "" and flag == True:
                    map[Y][X] = " "
                    return i, 0
                
                # If not the situations above, let imaginary human move a step,
                # and find the most possible action that can lead to human's failure
                else:
                    pos, value = self.human_move()
                    map[Y][X] = " "
                    if best_pos == 0 or value >= best_value:
                        best_pos = i
                        best_value = value
        return best_pos, best_value
            
    
    def human_move(self):
        '''Simulate human's action. Try to minimize each step's value of human'''
        best_pos = 0
        best_value = 0
        for i in range(1, 10):
            Y = i / 3
            X = i % 3
            if X != 0:
                X -= 1
            else:
                X = 2
                Y -= 1
            if map[Y][X] == " ":
                map[Y][X] = self.opponent_turn
                winner, flag = check_done()
                
                # The agent doesn't want human to win, so give it the lowest priority
                if len(winner) > 0 and flag == True:
                    map[Y][X] = " "
                    return i, -1
                
                # Draw
                elif winner == "" and flag == True:
                    map[Y][X] = " "
                    return i, 0
                
                # Give human minimal possible to win
                else:
                    pos, value = self.agent_move()
                    map[Y][X] = " "
                    if best_pos == 0 or value <= best_value:
                        best_pos = i
                        best_value = value
        return best_pos, best_value
    
    def __str__(self):
        print "Hello all, I'm computer agent"

turn = "X"
choice = False

# Choose the player and initialize the agent
while choice != True:
    player = raw_input("Choose the player you want to play, X or O?('X' goes first)")
    if player == "X":
        agent = Agent("O", "X")
        choice = True
    elif player == "O":
        agent = Agent("X", "O")
        choice = True
    else:
        print "Make the choice again"

map = [[" ", " ", " "],
       [" ", " ", " "],
       [" ", " ", " "]]
done = False

while done != True:
    print_board()
    
    print turn, "'s turn"
    print
    
    moved = False
    while moved != True:
        print "Please select position by typing in a number between 1 and 9, see below for which number that is which position..."
        print "7|8|9"
        print "4|5|6"
        print "1|2|3"
        print

        try:
            
            # Judge whose turn now
            if agent.is_agent_turn(turn) != True:
                pos = input("Select: ")
            else:
                pos, value = agent.agent_move()
                print "Agent's choice: ", pos
                
            # Convert position number to coordinate
            if pos <= 9 and pos >= 1:
                Y = pos / 3
                X = pos % 3
                if X != 0:
                    X -= 1
                else:
                    X = 2
                    Y -= 1
                                     
                if map[Y][X] == " ":                          
                    map[Y][X] = turn
                    moved = True
                    winner, done = check_done()

                    if done == False:
                        if turn == "X":
                            turn = "O"
                        else:
                            turn = "X"
                    elif done == True and winner == "":
                        print_board()
                        print "Draw"
                    else:
                        print_board()
                        print winner, "won!!!"

        except:
            print "You need to add a numeric value"

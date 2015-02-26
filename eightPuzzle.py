#Look for #IMPLEMENT tags in this file. These tags indicate changes in the 
#file to implement the required routines. 


'''8-Puzzle STATESPACE 
'''
import copy

from search import *

class eightPuzzle(StateSpace):
    StateSpace.n = 0
    
    def __init__(self, action, gval, state, parent = None):
        '''Create an 8-puzzle state object.
        The parameter state represents the puzzle configation as a list of 9 numbers in the range [0-8] 
        The 9 numbers specify the position of the tiles in the puzzle from the
        top left corner, row by row, to the bottom right corner. E.g.:

        [2, 4, 5, 0, 6, 7, 8, 1, 3] represents the puzzle configuration

        |-----------|
        | 2 | 4 | 5 |
        |-----------|
        |   | 6 | 7 |
        |-----------|
        | 8 | 1 | 3 |
        |-----------|
        '''
        #Note we represent the puzzle configuration in the state member.
        #the list of tile positions.
        StateSpace.__init__(self, action, gval, parent)
        self.state = state

    def successors(self) :
        #IMPLEMENT
        '''Implement the actions of the 8-puzzle search space.'''
        #   IMPORTANT. The list of successor states returned must be in the ORDER
        #   Move blank down move, move blank up, move blank right, move blank left
        #   (with some successors perhaps missing if they are not available
        #   moves from the current state, but the remaining ones in this  
        #   order!)

        states = list()
        blank_index = self.state.index(0)

        #if you can move blank down
        if blank_index != 6 and blank_index != 7 and blank_index != 8:
            new_state_down = copy.deepcopy(self.state)
            new_state_down[blank_index] = new_state_down[blank_index+3]
            new_state_down[blank_index+3] = 0
            states.append(eightPuzzle("Blank-Down", self.gval+1, new_state_down, self))

        #if you can move blank up
        if blank_index != 0 and blank_index != 1 and blank_index != 2:
            new_state_up = copy.deepcopy(self.state)
            new_state_up[blank_index] = new_state_up[blank_index-3]
            new_state_up[blank_index-3] = 0
            states.append(eightPuzzle("Blank-Up", self.gval+1, new_state_up, self))

        #if you can move blank right
        if blank_index != 2 and blank_index != 5 and blank_index != 8:
            new_state_right = copy.deepcopy(self.state)
            new_state_right[blank_index] = new_state_right[blank_index+1]
            new_state_right[blank_index+1] = 0
            states.append(eightPuzzle("Blank-Right", self.gval+1, new_state_right, self))

        #if you can move blank left
        if blank_index != 0 and blank_index != 3 and blank_index != 6:
            new_state_left = copy.deepcopy(self.state)
            new_state_left[blank_index] = new_state_left[blank_index-1]
            new_state_left[blank_index-1] = 0
            states.append(eightPuzzle("Blank-Left", self.gval+1, new_state_left, self))
        return states

    def hashable_state(self) :
    #IMPLEMENT
        return (tuple(self.state))

    def print_state(self):
        #DO NOT CHANGE THIS METHOD
        if self.parent:
            print("Action= \"{}\", S{}, g-value = {}, (From S{})".format(self.action, self.index, self.gval, self.parent.index))
        else:
            print("Action= \"{}\", S{}, g-value = {}, (Initial State)".format(self.action, self.index, self.gval))


        print("|-----------|")
        print("| {} | {} | {} |".format(self.state[0],self.state[1],self.state[2]))
        print("|-----------|")
        print("| {} | {} | {} |".format(self.state[3],self.state[4],self.state[5]))
        print("|-----------|")
        print("| {} | {} | {} |".format(self.state[6],self.state[7],self.state[8]))
        print("|-----------|")

#Set up the goal.
#We allow any full configuration of the puzzle to be a goal state. 
#We use the class variable "eightPuzzle.goal_state" to store the goal configuration. 
#The goal test function compares a state's configuration with the goal configuration

eightPuzzle.goal_state = False

def eightPuzzle_set_goal(state):
    '''set the goal state to be state. Here state is a list of 9
       numbers in the same format as eightPuzzle.___init___'''
    eightPuzzle.goal_state = state

def eightPuzzle_goal_fn(state):
    return (eightPuzzle.goal_state == state.state)

def heur_zero(state):
    '''Zero Heuristic use to make A* search perform uniform cost search'''
    return 0

def h_misplacedTiles(state):
    #IMPLEMENT
    #return the number of tiles (NOT INCLUDING THE BLANK) in state that are not in their goal 
    #position. (will need to access the class variable eigthPuzzle.goal_state)

    misplaced_tiles = 0
    for x in range(len(state.state)):
                if (state.state[x] != eightPuzzle.goal_state[x] and state.state[x] != 0):
                    misplaced_tiles += 1
    return misplaced_tiles




    
def h_MHDist(state):
    #return the sum of the manhattan distances each tile (NOT INCLUDING
    #THE BLANK) is from its goal configuration. 
    #The manhattan distance of a tile that is currently in row i column j
    #and that has to be in row x column y in the goal is defined to be
    #  abs(i - x) + abs(j - y)

    array = matrixfy(state.state)
    goal_state = matrixfy(eightPuzzle.goal_state)
    manhattan_distance = 0

    for x in state.state:
        if x != 0:
            i, j = locate(x, array)
            x, y = locate(x, goal_state)
            manhattan_distance += (abs(i - x) + abs(j - y))
    return manhattan_distance


def matrixfy(lst):

    array = []
    array.append(lst[0:3])
    array.append(lst[3:6])
    array.append(lst[6:9])
    return array

def locate(number, array):
    for x in array:
        if number in x:
            return (array.index(x), x.index(number))


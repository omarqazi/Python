""" Harsh Pathak
    B551 - Assignment 4 : Othello using minimax and alpha beta pruning
    hpathak@indiana.edu
"""    

"""Python funtions for calculating heuristics and doing alpha beta pruning """

"""
The general idea of heuristic used is as follows :

1) Number of valid moves left ; for both players
2) Corner positions. These are good in the sense that one corner place can give us a BIG flip and hence possibly a win. Bad because sometimes you cant play the corner
3) Total number of pieces of each player on the board
4) Pieces which have a blank (and hence open valid positions) nearby. This is advantageous for the other player but bad for us since our coins might get flanked. This is a bit tricky to implement

The final score is a combination of above heuristics. For each heuristic I define a weight based on the importance. For example number of pieces is not as good a heuristic
for calculating a winning move, but corner tiles is. Hence the latter gets more weight. 

Finally, each move is assigned a score. The alpha/beta pruning strategy cuts-off branches which are not required. We then make the move with the highest score. 
"""

from gamePlay import *
from copy import deepcopy
from operator import itemgetter
import sys

def number_of_legal_moves( board, color ):
	count=0
	for i in range (0,8):
		for j in range(0,8):
			if(validMove(board,color,(i,j))):
				count=count+1
	return count			


def othello_multiple_hueristics(move, board, color, time):


    if color == 'W':
        my_color = 'B'
        other_color = 'W'
    else:
        my_color = 'W'
        other_color = 'B'

    corner_score=0.0
    corner_closeness=0.0
    final_score=0.0
    my_frontier = 0
    other_frontier = 0
    frontier= 0
    


    my_pieces=0
    other_pieces=0
    for i in range(0,8):
        for j in range(0,8):
            if (board[i][j] == my_color ):
                my_pieces = my_pieces + 1
            elif (board[i][j] == other_color):
                other_pieces = other_pieces + 1

    if ( my_pieces > other_pieces ):
        piece_score = my_pieces/(my_pieces + other_pieces)
    elif ( other_pieces > my_pieces):
        piece_score = (-1) * (other_pieces)/(my_pieces + other_pieces)
    else:
        piece_score = 0





    """ Find number of remaining moves """

    my_pieces = number_of_legal_moves( board, my_color)
    other_pieces = number_of_legal_moves( board, other_color)

    if ( my_pieces > other_pieces):
        mobility = my_pieces / (my_pieces + other_pieces)
    elif ( other_pieces > my_pieces):
        mobility = (-1)*(other_pieces) / ( my_pieces + other_pieces)
    else:
        mobility = 0    


    """ Next check for corner tiles """
    
    my_pieces = 0 
    other_pieces = 0
    if (board[0][0] == my_color):
        my_pieces+=1
    elif (board[0][0] == other_color): 
        other_pieces += 1
    if ( board[0][7] == my_color ):
        my_pieces += 1
    elif (board[0][7] == other_color):
        other_pieces += 1
    if( board[7][0] == my_color):
        my_pieces += 1
    elif (board [7][0] == other_color):
        other_pieces += 1
    if( board[7][7] == my_color):
        my_pieces += 1
    elif( board[7][7] == other_color):
        other_pieces += 1
   
    corner_score = 35*(my_pieces - other_pieces)


    """Here we calculate the frontier discs. That is the number of discs which have an empty position nearby """

    if time > 30 :
        for x,y in [(a,b) for a in range( 8 ) for b in range( 8 ) if board[a][b] == '.']:
            for i,j in [(a,b) for a in [-1,0,1] for b in [-1,0,1]]:
                if 0 <= x+i <= 7 and 0 <= y+j <= 7:
                    if board[x+i][y+j] == my_color:
                        my_frontier+=1
                    else:
                        other_frontier+=1
    
        if ( my_frontier > other_frontier):
            frontier = -(100 * my_frontier ) / (my_frontier + other_frontier)
        elif ( my_frontier < other_frontier):
            frontier = (100 * other_frontier)/ (my_frontier + other_frontier)   
        else:
            frontier = 0 




    """If corner is empty , we might wanna take it since it has a better chance of giving us a bigger flip. Check nearby pieces in this case"""


    if(board[0][0] == '.'):
        if(board[0][1] == my_color):
            my_pieces +=1
        elif(board[0][1] == other_color):
            other_pieces += 1
        if(board[1][0] == my_color):
            my_pieces += 1
        elif(board[1][0] == other_color):
            other_pieces += 1
        if(board[1][1] == my_color):
            my_pieces += 1          
        elif(board[1][1] == other_color):
            other_pieces += 1
 


    if(board[0][7] == '.'):
        if(board[0][6] == my_color):
            my_pieces += 1
        elif(board[0][6] == other_color):
            other_pieces += 1
        if(board[1][6] == my_color):
            my_pieces += 1
        elif(board[1][6] == other_color):
            other_pieces += 1
        if(board[1][7] == my_color):
            my_pieces += 1          
        elif(board[1][7] == other_color):
            other_pieces += 1


    if(board[7][0] == '.'):
        if(board[7][1] == my_color):
            my_pieces += 1
        elif(board[7][1] == other_color):
            other_pieces += 1
        if(board[6][0] == my_color):
            my_pieces += 1
        elif(board[6][0] == other_color):
            other_pieces += 1
        if(board[6][1] == my_color):
            my_pieces += 1          
        elif(board[6][1] == other_color):
            other_pieces += 1


    if(board[7][7] == '.'):
        if(board[6][6] == my_color):
            my_pieces += 1
        elif(board[6][6] == other_color):
            other_pieces += 1
        if(board[7][6] == my_color):
            my_pieces += 1
        elif(board[7][6] == other_color):
            other_pieces += 1
        if(board[6][7] == my_color):
            my_pieces += 1          
        elif(board[6][7] == other_color):
            other_pieces += 1

    corner_closeness = (0.35)* ( my_pieces - other_pieces) 



    final_score = (20*corner_closeness) + (10 * mobility)+(5*piece_score) + (-10*corner_score) + (-10*frontier);
    return final_score



def alpha_beta_pruning( move, board, alpha, beta, depth, color, time):    

    temp_board = deepcopy(board)
    doMove(temp_board,color,move)
    possible_moves = []

    if depth == 0:
        if color == "B":
            eval = othello_multiple_hueristics (move, temp_board , color, time)
        else:
            eval = (-1)*othello_multiple_hueristics (move, temp_board , color, time)
        return eval
    

    for i in range(8):
        for j in range(8):
            if ( valid(board, color, (i,j))):
                possible_moves.append((i,j))


    if len(possible_moves) == 0:
        eval = othello_multiple_hueristics(move, board, color, time)
        return eval


    """MAX players move """
    a= -float('infinity')
    b= float('infinity')
    time = time - 1.0
    if depth%2 ==1:
            for move in possible_moves:
                score= alpha_beta_pruning(move, temp_board, a, min(beta, b),depth-1, opponent(color),time)
                b = min (b , score)
                if time < 5:
                    return b
                if alpha>= b:
                    return b
            return b
    else:
            for move in possible_moves:
                score= alpha_beta_pruning(move,temp_board, max(alpha, a), b, depth-1,color,time)
                a=max(a,score)
                if time < 2:
                    return a
                if a >= beta:
                    return a
                return a



def nextMove(board , color, time):
    depth = 8
    possible_moves = []
    each_move_score = []
    alpha = float('-infinity')
    beta = float('infinity')
    i=0
    bestMove = None

    temp_board = deepcopy(board)
    for i in range(8):
        for j in range(8):
            if (valid(board,color,(i,j))):
                possible_moves.append((i,j))
    if len(possible_moves) == 0:
        return "pass"

    for move in possible_moves:

        if time < 0:
            print "Time up !"
            sys.exit(1)


        if time > 30 and time < 45:
            depth = 4
        if time > 15 and time < 30:
            depth = 2
        if time < 5:
            depth = 1


        score = alpha_beta_pruning(move, temp_board, alpha, beta, depth,color, time)
        each_move_score .append(score)


    bestMove = possible_moves[each_move_score.index(max(each_move_score))] 

    return bestMove

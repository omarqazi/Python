# B551 - Elements of Artificial Intelligence 
# Assignment 2 (tic tac toe program) 
# Harsh Pathak
# hpathak@indiana.edu

##############################################################
## This code has been written and compiled in python
## version 2.7.2. Beginning Python version 3 , print command
## has been made in to a function. Output may vary
##############################################################


import random   # used to randomly select who goes first


########################################
#Code from tutorial , used to print out the board
########################################
def print_board():
    print "Current board status "
    print " "
    for i in range(0,3):
        for j in range(0,3):
            print map[2-i][j],
            if j != 2:
               print "|",
        print " "

######################################################
#Code from tutorial, used to check after each turn if the game is over
######################################################

def check_done():
    for i in range(0,3):
        if map[i][0] == map[i][1] == map[i][2] != " " \
        or map[0][i] == map[1][i] == map[2][i] != " ":
            print turn, "won!!" 
            return True


    if map[0][0] == map[1][1] == map[2][2] != " " \
    or map[0][2] == map[1][1] == map[2][0] != " ":
          print turn, "won!!"
          return True

    if " " not in map[0] and " " not in map[1] and " " not in map[2]:
        print "Draw"
        return True

    return False


###########################################################
## Function added to get players choice
##########################################################

""" This function returns a list of two elements. The first 
    element is the players choice while the second element 
    is the computers alphabet
""" 


def playerChoice():
     letter = ' ';
     while not ( letter == 'X' or letter == 'O'):
       temp = raw_input("Do you want to be X or 0 ?")
       letter = temp.upper()
       

     if letter == 'X': 
        return ['X','O']
     else: 
        return ['O','X'] 



############################################################
### Function added to decide who goes first randomly
############################################################

""" This function will randomly select if the player or
the computer goes first. The randint function will return 
either 0 or 1 randomly. If it returns 0 the computer goes first
else the player goes first 
"""

def goesFirst():
    if random.randint(0,1) == 0:
       return "computer"
    else:
       return "player"

###########################################################
## end function
##########################################################



#########################################################
## Function to check if user wants to play again
#######################################################

"""
This function checks if the player wants to play one more
game 
"""


def playAgain():
    choice = raw_input("Do you want to play again ? (yes /no )")
    return choice.lower().startswith('y')
#########################################################
##end function
########################################################



###########################################################
## The main game playing function with AI
###########################################################

""" This function decides the next move for the computer. 
    The general algorithm is as follows
    
     1) Check if the computer can win in the next move
     2) Check if the player can win in the next move. If so block it.
     3) Try to take one of the corners if possible
     4) Take the center if it is free
     5) Take one of the sides 

"""


def computerMove(map, computer):
    if computer == "X":
       player = "O"
    else: 
       player = "X"

 

#0 If the map is empty make a random move
# If the computer goes first then the board is emtpy
# Force the computer to make a random move
# The below snippet uses python iterators for traversing the 
#2 dimensional list

    for i in range(0,3):
        temp = all(v is " " for v in map[i])
    
    if temp:
       a = random.randint(0,2)
       b = random.randint(0,2)
       if map[a][b] == " ": 
            map[a][b] = computer
       return
       


#1 Check if we can win in next move
    


#2 Block players winning move
   

#3 Take one of the corners
 
    if map[0][0] == " " : 
       map[0][0] = computer
       return
    elif map[0][2] == " ":
       map [0][2] = computer
       return 
    elif map[2][0] == " ":
       map[2][0] = computer
       return
    elif map[2][2] == " ":
       map[2][2] = computer 
       return 
 
#4 Try to take the center

    if map[1][1] == " ":
      map[1][1] = computer
      return 
#5 Take the sides if available
  
    if map[0][1] == " ":
        map[0][1] = computer
        return
    elif map[1][0] == " ":
          map[1][0] = computer
          return 
    elif map[1][2] == " ":
          map[1][2] = computer
          return
    elif map [2][1] == " ":
          map[2][1] = computer
          return

#########################################################
## End function
#########################################################

map = [[" "," "," "], #this is a list of lists which holds the boards state
        [" "," "," "],
        [" "," "," "]]

done = False  #To check if the game is done or not    



while True:
       print " "
       map = [[" "," "," "], #reset the board. Required if uses chooses to play again
             [" "," "," "],
             [" "," "," "]]
       print " "
       player, computer  = playerChoice()
       turn  = goesFirst()
       print "The" + " " +  turn + " "  + "goes first"
       gameIsOn = True

       while gameIsOn:

             if turn == 'player':
                print " "
                print_board()
                print " "          
                print "Select a position for your next move. Choose a number for the position "
       	        print "7|8|9"
                print "4|5|6"
                print "1|2|3"
                print       
                
                try:
                  pos = input("Select : ")
                  
                  if pos <=9 and pos >=1:
                    Y = pos/3
                    X = pos%3
                    if X != 0:
                        X -= 1
                    else:  
                       X = 2
                       Y -= 1
      
                    if map[Y][X] == " " and map[Y][X] != "X" and map[Y][X] != "O":
                        map[Y][X] = player
                    else:
                        print " Wrong move. Position already taken"
                        break 
 
                        
                except:
                  print " "
                  print "You need to select a numeric value"

                done = check_done()
                if done == False:
                   gameIsOn = True
                   turn = 'computer'
                else: 
                   gameIsOn = False


             else:
                #Computers turn
                print " "
                computerMove(map , computer )
                done = check_done()
                if done == False:
                   gameIsOn = True
                   turn = 'player'
  
                else:
                   gameIsOn = False
     

       if not playAgain():
            break 

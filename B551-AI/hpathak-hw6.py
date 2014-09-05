"""
 B551 : Assignment 6 : Case Based Reasoning for 8 puzzle
 Harsh Pathak
 hpathak@indiana.edu

 I am using the base code provided as solution to HW3.  
""" 

import time
import os
from pydoc import deque
from heapq import heappush, heappop


goalState = []

case_base = []   #The Complete case base. This is a list of lists. Started out with dicts for better performance, but that got messy

case_base_element = () #Each tuple in our case base

path_list = [] #Append intermediate paths to this list

similarity_score = 0

uninformed_search_times = []

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

        
def testProcedure(queue):
    if (queue == goalState):
        return True
    else:
        return False
     
def outputProcedure(numRuns, path):

    #print path, "\n"
    path_list.append(path)
    #path_list = path_list + path

        
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
        if statelist[i] is None or not statelist[i] or statelist[i] == "blank" :
            statelist[i] = 0
        else:
            statelist[i] = int(statelist[i])    
    return statelist
    

def testUninformedSearch(initialState, goalState, limit):
    uninformedSearch ([initialState], limit, 0)
        

def createTestCaseBase(initialState, goalState):


    case_base_element = (initialState,path_list[0],goalState)
    case_base.append(case_base_element)


def printOutput(paths, path_g):
    
    
    row_1 = str(" |" + str(paths[0]) + "|" + str(paths[1]) + "|"+ str(paths[2]) + "|")
    row_2 = str("            |" + str(paths[3]) + "|" + str(paths[4]) + "|"+ str(paths[5]) + "|")
    row_3 = str ( "            |" + str(paths[6]) + "|" + str(paths[7]) + "|"+ str(paths[8]) + "|")
    
    print " START :   "+ row_1 + "    GOAL : " + "  |" + str(path_g[0]) + "|" + str(path_g[1]) + "|"+ str(path_g[2]) + "|"    
    print row_2 + "           " + "  |" + str(path_g[3]) + "|" + str(path_g[4]) + "|"+ str(path_g[5]) + "|"    
    print row_3 + "           " + "  |" + str(path_g[6]) + "|" + str(path_g[7]) + "|"+ str(path_g[8]) + "|"    

    print
    


    """
    for i in path_list:
        print (" " if i[0] == 0 else i[0]) , " " , (" " if i[1] == 0 else i[1]) , " " , (" " if i[2] == 0 else i[2]) 
        print (" " if i[3] == 0 else i[3]) , " " , (" " if i[4] == 0 else i[4]) , " " , (" " if i[5] == 0 else i[5]) 
        print (" " if i[6] == 0 else i[6]) , " " , (" " if i[7] == 0 else i[7]) , " " , (" " if i[8] == 0 else i[8]), "\n"
    """
    


def testCaseBasedSearch(START, GOAL):
    
    """Function to determine the similarity between any of the input goal states and goal states from the case base
    """ 

    noStartMismatch = 0
    noGoalMismatch = 0

    start_metric = []
    goal_metric = []

    final_metric = []
    count = 0

    final_metric_and_values = []

    for case in case_base:
        noStartMismatch=0
        if case[0] == START: 
            noStartMismatch = 0
            start_metric.append(noStartMismatch)
        else:
            for i in range(0,9):
                if START[i] != case[0][i]:
                    noStartMismatch += 1
            start_metric.append(noStartMismatch)       
          

    for case in case_base:
        noGoalMismatch = 0
        if case[2] == GOAL:
            noGoalMismatch = 0
            goal_metric.append(noGoalMismatch)
        else:
            for i in range(0,9):
                if GOAL[i] != case[2][i]:
                    noGoalMismatch += 1
            goal_metric.append(noGoalMismatch)
    

    final_metric = zip(start_metric, goal_metric)
    #Here we have the metrics as tuples. Each index corresponds to the position in the case base where it exists.
    
    

    for metric in range(0,len(final_metric)):
        count += 1
        print "------------------------------------------------"
        print "               CASE : " + str(metric+1)
        print "------------------------------------------------"
        printOutput(case_base[metric][0],case_base[metric][2])
        #print " PATH : " 
        #printPath(case_base[metric][1])
        print "------------------------------------------------"

        if final_metric[metric][0] == 0 and final_metric[metric][1] == 0 :
            similarity_score = "100"
            percent_similarity = (100- (float(final_metric[metric][0])/9)*100)
            print " It is 100% similar to the input problem."
            print "------------------------------------------------"
            print
            print
            #return "found",final_metric.index((final_metric[metric][0],final_metric[metric][1])),similarity_score,count
            final_metric_and_values.append(int(similarity_score))


        elif final_metric[metric][0] >= 0 and final_metric[metric][1] == 0 :
            similarity_score = "60"
            percent_similarity = (100- (float(final_metric[metric][0])/9)*100)
            print " Plan " + str(metric+1)+ " is " + str(round(percent_similarity,2)) + "% similar to the input problem."
            print "------------------------------------------------"
            print
            print
            #return "goal",final_metric.index((final_metric[metric][0],final_metric[metric][1])),similarity_score,count
            final_metric_and_values.append(int(similarity_score))

        elif final_metric[metric][0] == 0 and final_metric[metric][1] >= 0 :
            similarity_score = "50"
            percent_similarity = (100- (float(final_metric[metric][1])/9)*100)
            print " Plan " + str(metric+1)+ " is " + str(round(percent_similarity,2)) + "% similar to the input problem."
            print "------------------------------------------------"
            print
            print
            #return "start",final_metric.index((final_metric[metric][0],final_metric[metric][1])),similarity_score,count
            final_metric_and_values.append(int(similarity_score))

        elif final_metric[metric][0] <=5 and final_metric[metric][1] <=5 :
            similarity_score = "40"
            percent_similarity = (100- (float(final_metric[metric][0])/9)*100)
            print " Plan " + str(metric+1) + " is " + str(round(percent_similarity,2)) + "% similar to the input problem."
            print "------------------------------------------------"
            print
            print
            final_metric_and_values.append(int(similarity_score))
        
        else:
            similarity_score = "10"
            percent_similarity = (100- (float(final_metric[metric][0])/9)*100)
            print " Plan " + str(metric+1) + " is " + str(round(percent_similarity,2)) + "% similar to the input problem."
            print "------------------------------------------------"
            #return "scratch",0,similarity_score,count
            final_metric_and_values.append(int(similarity_score))




    max_percent = int(max(final_metric_and_values))
    max_index = int(final_metric_and_values.index(max(final_metric_and_values)))


    if max_percent == 100:
        return "found",max_index,0,count
    elif max_percent == 60:
        return "goal",max_index,0,count
    elif max_percent == 50:
        return "start",max_index,0,count
    elif max_percent == 40:
        return "similar",max_index,0,count
    elif max_percent == 10:
        return "scratch",max_index,0,count


def printPath(final_path):


    #final_path = removeDuplicates(final_path)
    
    for path in final_path:
        row_1 = str("      |" + str(path[0]) + "|" + str(path[1]) + "|"+ str(path[2]) + "|")
        row_2 = str("      |" + str(path[3]) + "|" + str(path[4]) + "|"+ str(path[5]) + "|")
        row_3 = str("      |" + str(path[6]) + "|" + str(path[7]) + "|"+ str(path[8]) + "|")
        
        print row_1
        print row_2
        print row_3
        print
    
    """
    This function for printing paths works only on my laptop . Output gets scrambled on different displays. It shows path as 

    |2|8|3|       |2|8|3|       |2|8|3|       |2|8|3|       |2|0|3|       |0|2|3|       |1|2|3|       |1|2|3|       |1|2|3|       |1|2|3|       |1|2|3|       |1|2|3|     
    |1|5|6| --->  |1|5|6| --->  |1|5|0| --->  |1|0|5| --->  |1|8|5| --->  |1|8|5| --->  |0|8|5| --->  |4|8|5| --->  |4|8|5| --->  |4|0|5| --->  |4|5|0| --->  |4|5|6|
    |4|0|7|       |4|7|0|       |4|7|6|       |4|7|6|       |4|7|6|       |4|7|6|       |4|7|6|       |0|7|6|       |7|0|6|       |7|8|6|       |7|8|6|       |7|8|0|  

    output_list = []
    temp_output_list1 = [[]]
    temp_output_list2 = [[]]
    temp_output_list3 = [[]]

    for i in range(0,len(final_path)):
        row_1 = str("|" + str(final_path[i][0]) + "|" + str(final_path[i][1]) + "|"+ str(final_path[i][2]) + "|")
        row_2 = str("|" + str(final_path[i][3]) + "|" + str(final_path[i][4]) + "|"+ str(final_path[i][5]) + "|")
        row_3 = str ("|" + str(final_path[i][6]) + "|" + str(final_path[i][7]) + "|"+ str(final_path[i][8]) + "|")
    
        temp_str = (row_1,row_2,row_3)
        output_list.append(temp_str)

       
    for i in output_list:
        temp_output_list1[0].append(i[0])
        temp_output_list2[0].append(i[1])
        temp_output_list3[0].append(i[2])

    for i in temp_output_list1[0]:
        print " " + i + "     ",
        

    print 
        
    count_l2=0    
    for i in temp_output_list2[0]:
        count_l2 += 1 
        if count_l2 != len(temp_output_list2[0]):
            print " " + i + " --->",
        else:
            print " " + i,    

    print    
    for i in temp_output_list3[0]:
        print  " " + i + "     ",

    """

    print "\n" 



def printCaseBase():

        for i in range(0,len(case_base)):
            print "------------------------------------------------"
            print "               CASE : " + str(i+1)
            print "------------------------------------------------"
            #print " START : ",printOutput(case_base[metric][0]) 
            #print
            #print " GOAL  : ",(printOutput(case_base[metric][2]))
            #print
            printOutput(case_base[i][0],case_base[i][2])
            print " PATH : " 
            printPath(case_base[i][1])
            print "------------------------------------------------"
            print
            print "------------------------------------------------"
            print "\n" + "\n"




def removeDuplicates(duplicate_list):

        old_dup = set(map(tuple,duplicate_list))
        new_dup = map(list,old_dup)

        new_dup.sort(key = lambda x: duplicate_list.index(x))
        return new_dup

# Main()
if __name__ == "__main__":

    os.system("clear")
    print "\n" + "\n"
    print " Initializing the case base. Please wait..."

    goalState = makeState(1,2,3,4,5,6,7,8,None)

    initialState = makeState(2, 8, 3, 1, 5, 6, 4, None, 7)
    testUninformedSearch(initialState, goalState, 200000)
    createTestCaseBase(initialState, goalState)
    #uninformed_search_times.append(abs(time.time() - t1))
    path_list = []

    
    initialState = makeState(1, 2, 3, None, 4, 6, 7, 5, 8)
    testUninformedSearch(initialState, goalState, 200000)
    createTestCaseBase(initialState, goalState)
    path_list = []
    

    initialState = makeState(1, 2, 3, 4, 5, 6, 7, "blank", 8)
    testUninformedSearch(initialState, goalState, 200000)
    createTestCaseBase(initialState, goalState)    
    path_list = []

    
    initialState = makeState(1, "blank", 3, 5, 2, 6, 4, 7, 8)
    testUninformedSearch(initialState, goalState, 200000)
    createTestCaseBase(initialState, goalState)
    path_list = []

    initialState = makeState(1, 2, 3, 4, 8, 5, 7, "blank", 6)
    testUninformedSearch(initialState, goalState, 200000)
    createTestCaseBase(initialState, goalState)
    path_list = []
    
    initialState = makeState(2, 8, 3, 1, "blank", 5, 4, 7, 6)
    testUninformedSearch(initialState, goalState, 200000)
    createTestCaseBase(initialState, goalState)
    path_list = []
    

    initialState = makeState(1, 2, 3, 4, 5, 6, "blank", 7, 8)
    testUninformedSearch(initialState, goalState, 200000)
    createTestCaseBase(initialState, goalState)
    
    initialState = makeState("blank", 2, 3, 1, 5, 6, 4, 7, 8)
    testUninformedSearch(initialState, goalState, 200000)
    createTestCaseBase(initialState, goalState)
    
    initialState = makeState(1, 3, "blank", 4, 2, 6, 7, 5, 8)
    testUninformedSearch(initialState, goalState, 200000)
    createTestCaseBase(initialState, goalState)

    initialState = makeState(1, 3, "blank", 4, 2, 5, 7, 8, 6)
    testUninformedSearch(initialState, goalState, 200000)
    createTestCaseBase(initialState, goalState)

    initialState = makeState("blank", 5, 3, 2, 1, 6, 4, 7, 8)
    testUninformedSearch(initialState, goalState, 200000)
    createTestCaseBase(initialState, goalState)

    initialState = makeState(5, 1, 3, 2, "blank", 6, 4, 7, 8)
    testUninformedSearch(initialState, goalState, 200000)
    createTestCaseBase(initialState, goalState)
    

    initialState = makeState(2, 3, 8, 1, 6, 5, 4, 7, "blank")
    testUninformedSearch(initialState, goalState, 200000)
    createTestCaseBase(initialState, goalState)
    

    initialState = makeState(1, 2, 3, 5, "blank", 6, 4, 7, 8)
    testUninformedSearch(initialState, goalState, 200000)
    createTestCaseBase(initialState, goalState)
    

    initialState = makeState("blank", 3, 6, 2, 1, 5, 4, 7, 8)
    testUninformedSearch(initialState, goalState, 200000)
    createTestCaseBase(initialState, goalState)
    

    initialState = makeState(2, 6, 5, 4, "blank", 3, 7, 1, 8)
    testUninformedSearch(initialState, goalState, 200000)
    createTestCaseBase(initialState, goalState)
    

    initialState = makeState(3, 6, "blank", 5, 7, 8, 2, 1, 4)
    testUninformedSearch(initialState, goalState, 200000)
    createTestCaseBase(initialState, goalState)


    initialState = makeState(1, 5, "blank", 2, 3, 8, 4, 6, 7)
    testUninformedSearch(initialState, goalState, 200000)
    createTestCaseBase(initialState, goalState)


    initialState = makeState(2, 5, 3, 4, "blank", 8, 6, 1, 7)
    testUninformedSearch(initialState, goalState, 200000)
    createTestCaseBase(initialState, goalState)


    initialState = makeState(3, 8, 5, 1, 6, 7, 4, 2, "blank")
    testUninformedSearch(initialState, goalState, 200000)
    createTestCaseBase(initialState, goalState)

    print
    print
    print " Case Base created. It has " + str(len(case_base)) + " elements \n"
 
    #loop = raw_input(" Press any key to continue. Enter STOP to terminate the program \n")
    #Accept User input for start and goal
    loop = "yes"

    while ( loop != "STOP" or loop != "stop"):
        
        print " The board layout is as follows : "
        print 
        print "   NW | N | NE "
        print "    W | C |  E "
        print "   SW | S | SE "
        print
        print " Enter numbers for the corresponding positions for the START state"
        print " Please enter the string blank for the empty spot"
        print
        print
        NW = raw_input(" Enter the number for position NW : ")
        N = raw_input(" Enter the number for position N : ")
        NE = raw_input(" Enter the number for position NE : ")
        W = raw_input(" Enter the number for position W : ")
        C = raw_input(" Enter the number for position C : ")
        E = raw_input(" Enter the number for position E : ")
        SW = raw_input(" Enter the number for position SW : ")
        S = raw_input(" Enter the number for position S : ")
        SE = raw_input(" Enter the number for position SE : ")
        START = makeState(NW,N,NE,W,C,E,SW,S,SE)

        print "\n" + "\n"
        print " Enter numbers for the corresponding positions for the GOAL state"
        print " Please enter the string blank for the empty spot"
        print
        print
        NW = raw_input(" Enter the number for position NW : ")
        N = raw_input(" Enter the number for position N : ")
        NE = raw_input(" Enter the number for position NE : ")
        W = raw_input(" Enter the number for position W : ")
        C = raw_input(" Enter the number for position C : ")
        E = raw_input(" Enter the number for position E : ")
        SW = raw_input(" Enter the number for position SW : ")
        S = raw_input(" Enter the number for position S : ")
        SE = raw_input(" Enter the number for position SE : ")
        GOAL = makeState(NW,N,NE,W,C,E,SW,S,SE)
        
        
        #START = makeState(2, 8, 3, 1, 5, 6, 4, None, 7)
        #GOAL = makeState(1,2,3,4,5,6,7,8,None)

        print
        print " Searching case base for similar problems.. \n"
        similarity = testCaseBasedSearch(START, GOAL)

        print " Performed  " + str(similarity[3]) + " comparisons on case base \n"

        loop = raw_input(" Press any key to continue. Enter STOP to terminate the program :  ")
        if loop == "STOP" or loop == "stop":
            break

        goalState = GOAL

        print 
        if similarity[0] != None and similarity [0] == "found":
            final_path=[]
            print " Exact problem found in plan " + str(similarity[2]+1)+ ". Reusing plan \n"
            print " The final path is "
            final_path = case_base[similarity[1]][1]
            printPath(final_path)


        if similarity[0] != None and similarity [0] == "start":
            final_path = []
            
            print " Plan " + str(similarity[2]+1)+ " with exact START state found. Adapting goal states.. \n"

            new_start = case_base[similarity[1]][2]
            path_to_new_start = case_base[similarity[1]][1]
            print " Calculating the final path... "
            time.sleep(5)
            os.system("clear")
            print "\n" + "\n"
            print " 1) We reuse the path from plan "+ str(similarity[2]+1)+" to reach an intermediate goal" + "\n"
            printPath(path_to_new_start)
            print " 2) And then we do an uninformed search from the above intermediate goal to our goal"
            path_list = []
            testUninformedSearch(new_start,goalState,200000)
            printPath(path_list[0])
            print "    The Final path will be a concatenation of the above to paths "
            printPath(path_to_new_start+path_list[0])
            print
            #print 
            #print path_list[0]


        if similarity[0] != None and similarity [0] == "goal":
            final_path = []
            
            print " Plan " + str(similarity[2]+1)+ " with EXACT goal state found. Adapting start states.. \n"
    
            new_goal = case_base[similarity[1]][0]
            path_to_goal = case_base[similarity[1]][1]
            goalState = new_goal
            print " Calculating the final path..."
            time.sleep(5)
            os.system("clear")
            print "\n" + "\n"
            print " 1) We do an uninformed search from the input START state to the START state of plan " + str(similarity[2]+1) + "\n"
            path_list = []

            testUninformedSearch(START,goalState,200000)

            printPath(path_list[0])
            print " 2) And then we reuse the path from plan " + str(similarity[2]+1) + " to reach the desired goal state" + "\n"
            printPath(path_to_goal)
            print "    The final path will be a concatenation of the above two paths \n"

            printPath(path_list[0]+path_to_goal)



        if similarity[0] != None and similarity [0] == "similar":
            final_path = []
            final_leg = []
            
            print " Sufficiently similar plans found in case base. Choosing plan " + str(similarity[2]+1)+ ". Adapting states.. \n"
    
            inter_goal = case_base[similarity[1]][0]
            inter_path = case_base[similarity[1]][1]
        
            goalState = inter_goal
            path_list = []
            testUninformedSearch(START, goalState,200000)
            first_path = path_list[0]

            #Now we have a 3 way path 

            goalState = GOAL
            inter_start = case_base[similarity[1]][2]
            path_list = []
            testUninformedSearch(inter_start, goalState,200000)

            final_leg = path_list[0]
            final_path = first_path + inter_path + final_leg
        
            print " Calculating the final path. Please wait... "
            time.sleep(5)
            os.system("clear")
            print "\n" + "\n"
            print " Since we do not have an exact match for either the START or the GOAL state, we calculate a total path of 3 individual path concatenations \n"
            print " 1) First we calculate a path from our START to the START state of plan " + str(similarity[3]) + "\n"
            printPath(first_path)
            print " 2) Then we reuse the path from the same plan to reach an intermediate goal state \n"
            printPath (inter_path)
            print " 3) Finally we calculate the path from the intermediate goal state to our goal state.\n"
            printPath(final_leg)
            print " The total path will be a concatenation of the above 3 paths \n"
            printPath(final_path)
            print " And finally we add this solution to our case base \n" 

            case_base.append((START,final_path,GOAL))
            print " Case added to the case base. It has " + str(len(case_base)) + " plans.\n"
            choice = raw_input(" Do you want to view the case base ? ")
            if choice == "yes" or choice == "YES" or choice == "y" or choice == "Y":
                os.system("clear")
                printCaseBase()


            path_list = []
        

        if similarity[0] != None and similarity [0] == "scratch":
            
            print " No sufficiently similar plans found. Starting from scratch. \n "
            path_list = []

            goalState = GOAL
            initialState = START

            testUninformedSearch(START, goalState, 200000)
            createTestCaseBase(initialState, goalState)
            print " Case added to our case base. It has " + str(len(case_base)) + " plans \n"
            choice = raw_input(" Do you want to view the case base ? ")
            if choice == "yes" or choice == "YES" or choice == "y" or choice == "Y":
                os.system("clear")
                printCaseBase()

        loop = raw_input (" Press any key to continue. Enter STOP to terminate the program. :")
        if loop == "STOP" or loop == "stop":
            break
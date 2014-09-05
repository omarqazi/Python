import sys
import heapq   # Used to maintain the data structure for tree
import copy
import time
import math
 

"""Almost most of the code is similar to the uninformed search file. Specifically, the code to get the start and goal states, code for displaying the board and the classes is 
the same. Only the methods for BFS have been replaced with informed search methods"""

limit = raw_input("Enter a limit on number of comparisons. Search will abandon beyond this point : ")
limit = int(limit) 
"""Limit is kept as a global variable and not passed directly to the function called since we use classes and methods"""

""" Get the start and goal states from the user. Since we need to take a blank as input , need to handle such cases and replace them with None in out board state
"""

def makeState(nw, n, ne, w, c, e, sw, s, se):
    if not nw:
        n = int(n)
        ne = int(ne)
        w = int(w)
        c = int(c)
        e = int(e)
        sw = int(sw)
        s = int(s)
        se = int(se)
        START = [None,n,ne,
                 w,c,e,
                 sw,s,se]
    if not n:
        nw = int(nw)
        ne = int(ne)
        w = int(w)
        c = int(c)
        e = int(e)
        sw = int(sw)
        s = int(s)
        se = int(se)
        START = [nw,None,ne,
                 w,c,e,
                 sw,s,se]
    if not ne:
        nw = int(nw)
        n = int(n)
        w = int(w)
        c = int(c)
        e = int(e)
        sw = int(sw)
        s = int(s)
        se = int(se)
        START = [nw,n,None,
                 w,c,e,
                 sw,s,se]
    if not w:
        nw = int(nw)
        n = int(n)
        ne = int(ne)
        c = int(c)
        e = int(e)
        sw = int(sw)
        s = int(s)
        se = int(se)
        START = [nw,n,ne,
                 None,c,e,
                 sw,s,se]
    if not c:
        nw = int(nw)
        n = int(n)
        w = int(w)
        ne = int(ne)
        e = int(e)
        sw = int(sw)
        s = int(s)
        se = int(se)
        START = [nw,n,ne,
                 w,None,e,
                 sw,s,se]

    if not e:
        nw = int(nw)
        n = int(n)
        w = int(w)
        c = int(c)
        ne = int(ne)
        sw = int(sw)
        s = int(s)
        se = int(se)
        START = [nw,n,ne,
                 w,c,None,
                 sw,s,se]

    if not sw:
        nw = int(nw)
        n = int(n)
        ne = int(ne)
        w = int(w)
        c = int(c)
        e = int(e)
        s = int(s)
        se = int(se)
        START = [nw,n,ne,
                 w,c,e,
                 None,s,se]
    if not s:
        nw = int(nw)
        n = int(n)
        ne = int(ne)
        w = int(w)
        c = int(c)
        e = int(e)
        sw = int(sw)
        se = int(se)
        START = [nw,n,ne,
                 w,c,e,
                 sw,None,se]
    if not se:
        nw = int(nw)
        n = int(n)
        ne = int(ne)
        w = int(w)
        c = int(c)
        e = int(e)
        sw = int(sw)
        s = int(s)
        
        START = [nw,n,ne,
                 w,c,e,
                 sw,s,None]

 
    return START 

"""The class for the vertex of our tree """
              
class Vertex(object):
    def __init__(self, weight):
        self.weight = weight
        self.cost = None
        self.total_cost = None
        self.parent = None

    """control the built in method repr to display our objects as strings """

    def __repr__(self):
        return str(self.weight)
 
    
    def __le__(self, other):
        return self.total_cost <= other.total_cost
 
 
class informedSearch(object):
 
    def __init__(self, start, goal):
        self.start = start
        self.goal = goal
        self.nodes = []
        self.max_count = 0
        self.elapsed = 0
        self.depth = 0
 
    def get_children(self, node):
        tmp_fringe = []
        fringe = []
        tmp_fringe.append(self.down(node))
        tmp_fringe.append(self.up(node))
        tmp_fringe.append(self.left(node))
        tmp_fringe.append(self.right(node))
        for new in tmp_fringe:
            if new:
                fringe.append(new)
        return fringe

 
    def get_position(self, node, weight):
        cells = int(math.sqrt(len(node)))
        row = node.index(weight) / cells
        col = node.index(weight) % cells
        return row, col
 
    def up(self, node):
        row, col = self.get_position(node, None)
        cells = int(math.sqrt(len(node)))
        if row != 0:
            newnode = copy.deepcopy(node)
            prev_pos = cells * row + col
            new_pos = cells * (row-1) + col
            new_val = node[new_pos]
            newnode[prev_pos] = new_val
            newnode[new_pos] = None
            return newnode
 
    def down(self, node):
        row, col = self.get_position(node, None)
        cells = int(math.sqrt(len(node)))
        max_row = cells-1
        if row != max_row:
            newnode = copy.deepcopy(node)
            prev_pos = cells * row + col
            new_pos = cells * (row+1) + col
            new_val = node[new_pos]
            newnode[prev_pos] = new_val
            newnode[new_pos] = None
            return newnode

    def left(self, node):
        row, col = self.get_position(node, None)
        cells = int(math.sqrt(len(node)))
        if col != 0:
            newnode = copy.deepcopy(node)
            prev_pos = cells * row + col
            new_pos = cells * row + col-1
            new_val = node[new_pos]
            newnode[prev_pos] = new_val
            newnode[new_pos] = None
            return newnode
 
    def right(self, node):
        row, col = self.get_position(node, None)
        cells = int(math.sqrt(len(node)))
        max_col = cells-1
        if col != max_col:
            newnode = copy.deepcopy(node)
            prev_pos = cells * row + col
            new_pos = cells * row + col+1
            new_val = node[new_pos]
            newnode[prev_pos] = new_val
            newnode[new_pos] = None
            return newnode


 
    def manhatten(self, node, goal):
        """
          The basic heuristic used with an informed search algorithm. This calcuates the square distance (instead of straight)  of how far a tile is from its correct position. 
        """
        distance = 0
        for i in node:
    
            if not i:
                continue
            row, col = self.get_position(node, i)
            row_goal, col_goal = self.get_position(goal, i)
            distance += abs(row_goal - row) + abs(col_goal - col)
        return distance

 
    def linear_conflict(self, node, goal):
        """
          This heuristic basically builds upon the manhatten distance. Two tiles are in a linear conflict if the tiles and their goal states are in the same line. Also one 
          is to the right of the other and has its goal location to the left of goal of the other tile.
        """

    def misplaced_tiles(self,node, goal):
        distance = 0
        for i in node:
                
            if not i:
                    continue
            row, col = self.get_position(node, i)
            row_goal, col_goal = self.get_position(goal, i)
            if not (row_goal == row and col_goal == col):
                distance+=1
        return distance
 


    def informedSearch1(self, node_list=None):
        """This one uses the manhattan distance heuristic. Makes lesses comparisons"""
        ret = None
        test_count = 0
        if not node_list:
            self.start.cost = self.manhatten(self.start.weight, 
                    self.goal.weight)
            self.start.total_cost  = 0
            node_list = []
            heapq.heapify(node_list)
            heapq.heappush(node_list, self.start)
            closed = []
        
        while node_list:
            node = heapq.heappop(node_list)
 
            if node.weight == self.goal.weight:
                print ("Total comparisons made are %s " % (self.max_count))
                print
                return node
            else:
                test_count += 1
                if test_count > limit:
                    print "Oops ! I am not intelligent enough to perform so many comparisons. Aborting.."
                    sys.exit()
            tmp = self.get_children(node.weight)
            for i in tmp:
                if i not in closed:
                    self.max_count += 1
                    closed.append(i)
                    child_node = Vertex(i)
                    child_node.parent = node
                    child_node.cost = self.manhatten(i, self.goal.weight)
                    child_node.total_cost = child_node.cost + node.total_cost
                    heapq.heappush(node_list, child_node)
        return ret


    def informedSearch2(self, node_list=None):
        """This one uses the misplace tile heuristic. For harder problems this takes more comparisons"""
        ret = None
        test_count = 0
        if not node_list:
            self.start.cost = self.misplaced_tiles(self.start.weight,
                                             self.goal.weight)
            self.start.total_cost  = 0
            node_list = []
            heapq.heapify(node_list)
            heapq.heappush(node_list, self.start)
            closed = []
        
        while node_list:
            node = heapq.heappop(node_list)
            
            if node.weight == self.goal.weight:
                print ("Total comparisons made are %s " % (self.max_count))
                print
                return node
            else:
                test_count += 1
                if test_count > limit:
                    print "Oops ! I am not intelligent enough to perform so many comparisons. Aborting.."
                    sys.exit()
            tmp = self.get_children(node.weight)
            for i in tmp:
                if i not in closed:
                    self.max_count += 1
                    closed.append(i)
                    child_node = Vertex(i)
                    child_node.parent = node
                    child_node.cost = self.misplaced_tiles(i, self.goal.weight)
                    child_node.total_cost = child_node.cost + node.total_cost
                    heapq.heappush(node_list, child_node)
        return ret
    
    

    def display(self, node):
        board_state = ""
        cells = int(math.sqrt(len(node)))
        for count, val in enumerate(node):
            if not val:
                val = ' '
            if (count + 1) % cells > 0:
                board_state += " %s |" % val 
            else:
                board_state += " %s |\n" % val 
        return board_state

if __name__ == "__main__":
 
    print "The board layout is as follows : "
    print 
    print " NW | N | NE "
    print "  W | C | E "
    print " SW | S | SE "
    print
    print "Enter numbers for the corresponding positions for the start state"
    print "Please enter blank for the empty spot"
    print 
    print
    NW = raw_input("Enter the number for position NW : ")
    N = raw_input("Enter the number for position N : ")
    NE = raw_input("Enter the number for position NE : ")
    W = raw_input("Enter the number for position W : ")
    C = raw_input("Enter the number for position C : ")
    E = raw_input("Enter the number for position E : ")
    SW = raw_input("Enter the number for position SW : ")
    S = raw_input("Enter the number for position S : ")
    SE = raw_input("Enter the number for position SE : ")
    START = makeState(NW,N,NE,W,C,E,SW,S,SE)


    print "Enter numbers for the corresponding positions for the GOAL state"
    print "Please enter blank for the empty spot"
    print
    print
    NW = raw_input("Enter the number for position NW : ")
    N = raw_input("Enter the number for position N : ")
    NE = raw_input("Enter the number for position NE : ")
    W = raw_input("Enter the number for position W : ")
    C = raw_input("Enter the number for position C : ")
    E = raw_input("Enter the number for position E : ")
    SW = raw_input("Enter the number for position SW : ")
    S = raw_input("Enter the number for position S : ")
    SE = raw_input("Enter the number for position SE : ")

    print "---------------------------------------------------------------------------------"
    print "           Informed search results using manhatten distance heuristic            "
    print "---------------------------------------------------------------------------------"

    GOAL = makeState(NW,N,NE,W,C,E,SW,S,SE) 
    puzzle = informedSearch(Vertex(START), Vertex(GOAL))
    start = time.time()
    result = puzzle.informedSearch1()
    end = (time.time() - start)
        
    node = result
    count = 0
    while True:
       count +=1
       if not node:
          break
       print puzzle.display(node.weight)
       
       node = node.parent
    print("%s Time taken %.2f seconds \n" % ("Manhattan heuristic", (end)))


    print "---------------------------------------------------------------------------------"
    print "           Informed search results using misplaced tiles heuristic            "
    print "---------------------------------------------------------------------------------"
    
    GOAL = makeState(NW,N,NE,W,C,E,SW,S,SE)
    puzzle = informedSearch(Vertex(START), Vertex(GOAL))
    start = time.time()
    result = puzzle.informedSearch2()
    end = (time.time() - start)
    
    node = result
    count = 0
    while True:
        count +=1
        if not node:
            break
        print puzzle.display(node.weight)
        
        node = node.parent
    print("%s Time taken %.2f seconds \n" % ("Misplaced Tiles heuristic", (end)))
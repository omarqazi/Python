import sys
import copy
import time
import math
 

limit = raw_input("Enter a limit on comparisons made. Search will abandon beyond this point : ")
limit = int(limit) 

"""Limit is kept as a global variable and not passed directly to the function called since we use classes and methods"""


""" Get the start and goal states from the user. Since we need to take a blank as input , need to handle such cases and replace them with None in our board state
    Function can be optimized using iterators and decorators. 
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
 
 
class uninformedSearch(object):
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
 
    def display(self, node):
        ret = ""
        cells = int(math.sqrt(len(node)))
        for count, val in enumerate(node):
            if not val:
                val = ' '
            if (count + 1) % cells > 0:
                ret += " %s |" % val 
            else:
                ret += " %s\n" % val 
        return ret


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
 
    def testUninformedSearch(self):
        closed = []
        ret = self._testUninformedSearch([self.start], closed)
        return ret
 
    def _testUninformedSearch(self, node_list, closed):
        fringe = []   
        test_count = 0
        for node in node_list:
            if node.weight == self.goal.weight:
                print ("Total comparisons made are %s " % (self.max_count))
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
                    fringe.append(child_node)
        if fringe:
            ret = self._testUninformedSearch(fringe, closed)
        return ret

 
if __name__ == "__main__":
 
    print "The board layout is as follows : "
    print 
    print " NW | N | NE "
    print "  W | C | E "
    print " SW | S | SE "
    print
    print "Enter numbers for the corresponding positions for the START state"
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

    GOAL = makeState(NW,N,NE,W,C,E,SW,S,SE)
    puzzle = uninformedSearch(Vertex(START), Vertex(GOAL))


    print "---------------------------------------------------------------"
    print "                 Uninformed Search using BFS                   "
    print "---------------------------------------------------------------"


    print " The start state is :" 
    print
    print
    print START
    print
    print " The Goal state is : " 
    print
    print GOAL

    start = time.time()
    result = puzzle.testUninformedSearch()
    end = (time.time() - start)
        
    node = result
    count = 0
    while True:
       count +=1
       if not node:
          break
       print puzzle.display(node.weight)
       
       node = node.parent
    print("%s Time taken %.2f seconds \n" % ("Uninformed Search", (end)))



    
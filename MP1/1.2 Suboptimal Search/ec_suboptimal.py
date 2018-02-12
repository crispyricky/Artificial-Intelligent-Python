
# coding: utf-8

# In[1]:


import numpy as np
import scipy.spatial.distance as sp
from heapq import heappush, heappop

result = []
with open('bigdots.txt') as maze:
    for line in maze:
        result.append(list(line.strip()))

c = 0
for m in range(len(result)):
    for n in range(len(result[m])):
        if result[m][n] == ".":
            c = c + 1
print ("There are a total of {} dots".format(c))

for n in range(len(result)):
    print("".join(result[n]))

result_0 = result[1:-1]
result_1 = []
for n in range(len(result_0)):
    result_1.append(result_0[n][1:-1])
# remove all walls

end = []

for m in range(len(result_1)):
    for n in range(len(result_1[m])):
        if result_1[m][n] == "%":
            result_1[m][n] = 1
            # convert to 1 if wall
        elif result_1[m][n] == ".":
            end.append((m,n))
            # print ending point
            result_1[m][n] = 0
            # convert to 0 if ending point
        elif result_1[m][n] == "P":
            start_x = m
            start_y = n
            # print starting point
            result_1[m][n]= 0
            # convert to 0 if starting point
        else: result_1[m][n] = 0
            # convert to 0 if vacant

result_2 = np.array(result_1)

global cs
global cn
cs = []             # step cost accumulator
cn = []             # expanded node accumulator

def subopt(maze, start, end):                               # pseudocode at http://web.mit.edu/eranki/www/tutorials/search/
        dist = []
        for i in end:
            dist.append(sp.cityblock(list(start), list(i)))
        goal = end.pop(dist.index(min(dist)))
        # get the nearest dot and set it as current goal

        open_list = []                                      # initialize the open list
        closed_list = []                                    # initialize the closed list
        f = {}                                              # recording fn of the nodes 
        f[start] = sp.cityblock(list(start),list(goal))     # f(start) = h(start)
        open_list.append((f[start], start))                 # put the starting node on the open list
        parent = {}                                         # recording the matching parent of a successor
        node = 0                                            # expanded node counter

        while (len(open_list) != 0):
            node += 1
            q = heappop(open_list)[1]
            # find the node with the least f on the open list, call it "q",  pop q off the open list

            for successor in [(q[0]+1, q[1]+0), (q[0]-1, q[1]+0), (q[0]+0, q[1]+1), (q[0]+0, q[1]-1)]:
            # loop through four successors in NSEW directions

                if successor == goal:
                    goal1 = goal
                    goal = (100000,0)
                    node += 1
                    data = []
                    while q in parent:
                        data.append(q)
                        q = parent[q]
                    data.append(start)
                    cs.append(len(data))
                    cn.append(node)
                    if (len(end) != 0):
                        subopt(maze, goal1, end)
                        # recursion: set the current goal as the new start

                if (0 <= successor[0] < maze.shape[0]) and (0 <= successor[1] < maze.shape[1]) and (maze[successor[0]][successor[1]]) == 1:
                    continue
                # successor in range but is wall (unreachable)

                if (not 0 <= successor[0] < maze.shape[0]) or (not 0 <= successor[1] < maze.shape[1]):
                    continue
                # successor out of range

                fvalue = f.get(q) + sp.cityblock(list(successor),list(goal)) + 1
                # f score equals (old f score) plus (the heuristic of the new node) plus (one)

                if (successor in closed_list) or ((successor in [i[1] for i in open_list]) and (fvalue >= f.get(successor))):
                    continue
                # (successor in the closed list) OR (successor in the open list AND has larger f value) 

                if  successor not in [i[1]for i in open_list]:
                    parent[successor] = q
                    f[successor] = fvalue
                    heappush(open_list, (f[successor], successor))

            closed_list.append(q)
            # push q on the closed list

        return None

subopt(result_2, (start_x, start_y), end)
print ("The path cost (# of steps): {}".format(sum(cs)))
print ("Number of nodes expanded: {}".format(sum(cn)))


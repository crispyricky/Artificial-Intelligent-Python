
# coding: utf-8

# In[1]:


import numpy as np
import heapq
import time


# In[2]:

#put file name in a variable

sokoban_name = 'sokoban1.txt'


# In[3]:

# This is a state class that contains Player's coordinate, boxes' coordinate, each step's cost(for A* which we have not implement yet)
# and its parent state.
class state(object):
    def heu_def(self):
        return 0
    
    def __init__(self,P_coor=[], box_coor=np.array([]), cost=0, heu=heu_def, parent=None,save=[]):
        self.P_coor = P_coor
        self.box_coor = box_coor  
        self.cost = cost  
        self.parent = parent
        self.heu = heu
        self.save = save
    def __str__(self):
        if (self.parent==None):
            return "\nPlayer's coordinate:%s,\nbox_coor:%s,\nparent:NONE" %(self.P_coor, self.box_coor)
        else:
            return "\nPlayer's coordinate:%s,\nbox_coor:%s,\nparent:%s,\ncost:%s" %(self.P_coor, self.box_coor, self.parent.P_coor,self.cost)
    def __lt__(self, other): 
        return self.heu(self) < other.heu(other)
    def __eq__(self, other):
        if other == None:
            return
        return (self.P_coor == other.P_coor)


# In[4]:

# This is the human decide parameters which would be useful for transformation from characters to numbers.
soko_number = {' ':0, 'P':1, '%':2, '.':3, 'b':4, 'B':5}
START_NUM = 1
WALL_NUM = 2
STORAGE_AVAL_NUM = 3
BOX_AVAL_NUM = 4
BOX_ON_STORAGE_NUM = 5
PATH_NUM = 0
MOVE = [[0,-1],[1,0],[0,1],[-1,0]]


# This is a funtion to read Sokoban map, it accepts a sokoban txt file and returns a map, a dictionary map, a numpy array box_coordinator
# a numpy array storage coordinator and the player's starting coordinator.
def read_sokoban(sokoban_name):
    open_Sokoban = open(sokoban_name, 'r')
    Sokoban_lines = open_Sokoban.readlines()
    Sokoban = np.array([list(i.strip()) for i in Sokoban_lines])
    box_coor = []
    storage_coor = []
#     start_coor = np.array([0, 0])
    Sokoban_Dict = np.zeros(Sokoban.shape, dtype='int')
    for i in range(Sokoban.shape[0]):
        for j in range(Sokoban.shape[1]):
            Sokoban_Dict[i][j] = soko_number[Sokoban[i][j]]
            if (Sokoban_Dict[i][j] == START_NUM): 
                start_coor = np.array([i, j])
            elif (Sokoban_Dict[i][j] == STORAGE_AVAL_NUM):
                storage_coor.append([i, j])
            elif (Sokoban_Dict[i][j] == BOX_AVAL_NUM):  
                box_coor.append([i, j])
            elif (Sokoban_Dict[i][j] == BOX_ON_STORAGE_NUM):
                box_coor.append([i, j])
                storage_coor.append([i, j])
    return Sokoban,Sokoban_Dict,np.array(box_coor),np.array(storage_coor),start_coor

#This is a function to check if input state is the last state.
def check_done(state,storage_coor):
    return(sorted(state.box_coor.tolist()) == sorted(storage_coor.tolist()))

#This is a function to check if input coordinate is wall.
def iswall(n_d,Sokoban_Dict):
    return (Sokoban_Dict[n_d[0]][n_d[1]]==WALL_NUM)

#This is a function to check if input coordinate is a box.
def isbox(n_d,state):
    return (n_d.tolist() in state.box_coor.tolist())

#This is a function to check if input box coordinate can move along the direction.
def canmove(n_d,di,state,Sokoban_Dict):
    status = (not isbox(n_d+di,state))and(Sokoban_Dict[n_d[0]+di[0]][n_d[1]+di[1]]!=WALL_NUM)
    status = status and to_corner(n_d,di,state,Sokoban_Dict)
    return status

#This is a function to check if input coordinate is a corner.
def to_corner(n_d,di,state,Sokoban_Dict):
    n_loc = n_d+di
    if (((Sokoban_Dict[n_loc[0]-1,n_loc[1]]==WALL_NUM and Sokoban_Dict[n_loc[0],n_loc[1]-1]==WALL_NUM) or         (Sokoban_Dict[n_loc[0]-1,n_loc[1]]==WALL_NUM and Sokoban_Dict[n_loc[0],n_loc[1]+1]==WALL_NUM) or         (Sokoban_Dict[n_loc[0]+1,n_loc[1]]==WALL_NUM and Sokoban_Dict[n_loc[0],n_loc[1]+1]==WALL_NUM) or         (Sokoban_Dict[n_loc[0]+1,n_loc[1]]==WALL_NUM and Sokoban_Dict[n_loc[0],n_loc[1]-1]==WALL_NUM)) and        (Sokoban_Dict[n_loc[0],n_loc[1]]!=STORAGE_AVAL_NUM)):
        return False
    return True

#This is a function to move the box.
def move_box(n_d,di,temp_box):
    for box in temp_box:
        if ((box[0] == n_d[0])and(box[1] == n_d[1])):
            box[0] = n_d[0]+di[0]
            box[1] = n_d[1]+di[1]
    return

#This is a function to get the final result from the last state.
def get_result(next_state):
    res = []
    parent = next_state.parent
    while (parent != None):
        res.append(next_state.P_coor.tolist())
        next_state = parent
        parent = next_state.parent
    return res

#This is a function to check if the state is already visited.
def in_visited(next_state,visited):
    return (next_state.save in visited)

#This is a function to draw a Sokoban state.
def draw_soko(Sokoban,Sokoban_Dict,storage_coor,cur_state):
    for i in range(len(Sokoban)):
        for j in range(len(Sokoban[i])):
            if (Sokoban_Dict[i][j] != WALL_NUM):
                Sokoban_Dict[i][j] = PATH_NUM

    for box in cur_state.box_coor:
        Sokoban_Dict[box[0]][box[1]] = BOX_AVAL_NUM
        for val in storage_coor:
            if (box==val).all():
                Sokoban_Dict[box[0]][box[1]] = BOX_ON_STORAGE_NUM

    for storage in storage_coor:
        if Sokoban_Dict[storage[0]][storage[1]] != BOX_ON_STORAGE_NUM:
            Sokoban_Dict[storage[0]][storage[1]] = STORAGE_AVAL_NUM
            
    Sokoban_Dict[cur_state.P_coor[0]][cur_state.P_coor[1]] = START_NUM

    for i in range(len(Sokoban)):
        for j in range(len(Sokoban[i])):
            if (Sokoban_Dict[i][j] == STORAGE_AVAL_NUM):
                Sokoban[i][j] = '.'
            if (Sokoban_Dict[i][j] == START_NUM):
                Sokoban[i][j] = 'P'
            if (Sokoban_Dict[i][j] == BOX_ON_STORAGE_NUM):
                Sokoban[i][j] = 'B'
            if (Sokoban_Dict[i][j] == BOX_AVAL_NUM):
                Sokoban[i][j] = 'b'
            if (Sokoban_Dict[i][j] == PATH_NUM):
                Sokoban[i][j] = ' '
    for n in range(len(Sokoban)):
        print("".join(Sokoban[n]))


# In[10]:

#This is the main function to solve the sokoban problem 
def bfs_solve_soko(sokoban_name):
    start_time=time.time()
    Sokoban,Sokoban_Dict,box_coor,storage_coor,start_coor = read_sokoban(sokoban_name)
    start_state = state(start_coor, box_coor, cost=0, save = [start_coor.tolist(),box_coor.tolist()])
    queue = []
    queue.append(start_state)
    visited = []
    visited.append(start_state.save)

    while (queue):

        cur_state = queue.pop(0)
    #     print(cur_state)
    #    draw_soko(Sokoban,Sokoban_Dict,storage_coor,cur_state)
        for di in MOVE:
    #         print("current move direction:",di)
            temp_box = cur_state.box_coor.copy()
            n_d = cur_state.P_coor + di # next_direction
            if(iswall(n_d,Sokoban_Dict)): 
                continue
            if(isbox(n_d,cur_state)):
                if (canmove(n_d,di,cur_state,Sokoban_Dict)):
                    move_box(n_d,di,temp_box)
    #                 print("move!,n_d:%s, di:%s"%(n_d,di))
                else: continue

            next_state = state(n_d, temp_box, parent=cur_state, save = [n_d.tolist(),temp_box.tolist()])
            if(check_done(next_state,storage_coor)):
                draw_soko(Sokoban,Sokoban_Dict,storage_coor,next_state)
                
    #             print(next_state)
    #             draw_soko(Sokoban,Sokoban_Dict,storage_coor,next_state)
                res = get_result(next_state)
                print(time.time()-start_time)
                print(len(res))
                print(len(visited))
                return res,len(visited)
            if (next_state.save in visited): continue
            queue.append(next_state)
            visited.append(next_state.save)



# In[11]:


res,lenvisit = bfs_solve_soko(sokoban_name)


# In[9]:


print(res)


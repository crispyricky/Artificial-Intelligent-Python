
# coding: utf-8

# In[30]:


import numpy as np
import heapq


# In[12]:


sokoban_name = 'sokoban1.txt'


# In[13]:


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


# In[27]:


soko_number = {' ':0, 'P':1, '%':2, '.':3, 'b':4, 'B':5}
START_NUM = 1
WALL_NUM = 2
STORAGE_AVAL_NUM = 3
BOX_AVAL_NUM = 4
BOX_ON_STORAGE_NUM = 5
PATH_NUM = 0
MOVE = [[0,-1],[1,0],[0,1],[-1,0]]

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

def check_done(state,storage_coor):
    return(sorted(state.box_coor.tolist()) == sorted(storage_coor.tolist()))

def iswall(n_d,Sokoban_Dict):
    return (Sokoban_Dict[n_d[0]][n_d[1]]==WALL_NUM)

def isbox(n_d,state):
    return (n_d.tolist() in state.box_coor.tolist())

def canmove(n_d,di,state,Sokoban_Dict):
    return (not isbox(n_d+di,state))and(Sokoban_Dict[n_d[0]+di[0]][n_d[1]+di[1]]!=WALL_NUM)

def move_box(n_d,di,temp_box):
    for box in temp_box:
        if ((box[0] == n_d[0])and(box[1] == n_d[1])):
            box[0] = n_d[0]+di[0]
            box[1] = n_d[1]+di[1]
    return

def get_result(Sokoban,Sokoban_Dict,storage_coor,next_state):
    res = []
    parent = next_state.parent
    
    while (parent != None):
        draw_soko(Sokoban,Sokoban_Dict,storage_coor,next_state)
        res.append(next_state.P_coor.tolist())
        next_state = parent
        parent = next_state.parent
    return res

def in_visited(next_state,visited):
    return (next_state.save in visited)

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


# In[28]:


def bfs_solve_soko(sokoban_name):
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
                res = get_result(Sokoban,Sokoban_Dict,storage_coor,next_state)
                return res, len(visited), 
            if (next_state.save in visited): continue
            queue.append(next_state)
            visited.append(next_state.save)


# In[29]:


a,b = bfs_solve_soko(sokoban_name)


# In[ ]:


Sokoban,Sokoban_Dict,box_coor,storage_coor,start_coor = read_sokoban(sokoban_name)
queue = []
bfs_start_state = state(start_coor, box_coor, box_coor)


# In[ ]:


def soko_Astar(sokoban_name):
    Sokoban,Sokoban_Dict,box_coor,storage_coor,start_coor = read_sokoban(sokoban_name)
    start_state = state(start_coor, box_coor, cost=0)
    queue = []
    heapq.heappush(queue, start_state)
    visited = set()
    visited.add(start_state)
    
    while (queue):

        cur_state = heapq.heappop(queue)
        visited.add(cur_state)
        
        for di in MOVE:
            n_d = np.array(cur_state.P_coor + di) # next_direction
            if(iswall(n_d,Sokoban_Dict)): 
                continue
            if(isbox(n_d,Sokoban_Dict)):
                if (canmove(n_d,di,Sokoban_Dict)):
                    move_box(n_d,di,box_coor)
                else: continue
            next_state = state(n_d, box_coor, cost=cur_state.cost+1, parent=cur_state)
            heapq.heappush(queue, next_state)
            visited.add(next_state)
            if(check_done(next_state,storage_coor)):
                res = get_resule(next_state)
                return res, next_state.cost
    return None


# In[ ]:


Sokoban,Sokoban_Dict,box_coor,storage_coor,start_coor = read_sokoban(sokoban_name)


# In[ ]:


box_coor[0][1]=1000


# In[ ]:


box_coor


# In[ ]:


box = [2,2]
n_d = [2,2]
di = [0,-1]


# In[ ]:


box[0] = n_d[0]+di[0]
box[1] = n_d[1]+di[1]


# In[ ]:


box[0] == n_d[0]


# In[ ]:


res, cost=soko_Astar(sokoban_name)


# In[ ]:


Sokoban,Sokoban_Dict,box_coor,storage_coor,start_coor = read_sokoban(sokoban_name)
start_state = state(start_coor, box_coor, cost=0)
queue = []
heapq.heappush(queue, start_state)
visited = set()
visited.add(start_state)

while (queue):

    cur_state = queue.pop(0)
    visited.add(cur_state)
    print(cur_state)
    draw_soko(Sokoban,Sokoban_Dict,storage_coor,cur_state)
    for di in MOVE:
        n_d = cur_state.P_coor + di # next_direction
        if(iswall(n_d,Sokoban_Dict)): 
            continue
        if(isbox(n_d,Sokoban_Dict)):
            if (canmove(n_d,di,Sokoban_Dict)):
                move_box(n_d,di,box_coor)
            else: continue
        next_state = state(n_d, box_coor, cost=cur_state.cost+1, parent=cur_state)
        if(check_done(next_state,storage_coor)):
            res = get_resule(next_state)
        if (next_state in visited):
            continue
        queue.append(next_state)
        visited.add(next_state)


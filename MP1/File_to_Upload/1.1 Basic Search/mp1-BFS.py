
# coding: utf-8

# In[33]:


import numpy as np
import queue
maze_name = "OpenMaze.txt"

f = open(maze_name)
maze_sol = []
with open(maze_name) as inputfile:
    for line in inputfile:
        maze_sol.append(list(line.strip()))

maze = f.readlines()


# In[34]:


maze_dict = {' ':0, 'P':1, '%':2, '.':3, '\n':2}
maze_height = len(maze)
maze_width = len(maze[0])
maze_visited = np.zeros((maze_height, maze_width))
maze_tree = {}
count = 0


# In[35]:


for h in range(len(maze)):
    for w in range(len(maze[h])):
        if maze_dict[maze[h][w]] == 2:
            maze_visited[h][w] = 1
        if maze_dict[maze[h][w]] == 1:
            maze_start_height = h
            maze_start_width = w
        if maze_dict[maze[h][w]] == 3:
            maze_end_height = h
            maze_end_width = w
        maze_tree[(h,w)] = [0,0,0,0,0] # up, right, down, left, parent[0:up,1:right,2:down,3:left]
        if maze_dict[maze[h][w]] == 2:
            continue
        if maze_dict[maze[h][w]] != 2:
            if maze_dict[maze[h+1][w]] != 2:
                maze_tree[(h,w)][2] = 1
            if maze_dict[maze[h-1][w]] != 2:
                maze_tree[(h,w)][0] = 1
            if maze_dict[maze[h][w+1]] != 2:
                maze_tree[(h,w)][1] = 1
            if maze_dict[maze[h][w-1]] != 2:   
                maze_tree[(h,w)][3] = 1


# In[36]:


def bfs(tree, start, end, visit):
    global count
    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    queue.append(start)
    print('my start is %s',start)
    print('my end is %s',end)
    print('bfs finding...')
    while queue:
        # get the first path from the queue
#         print('checking queue')
#         print(queue)
        node = queue.pop(0)
        # get the last node from the path

#         print('checking node')
#         print(node)
        
        # path found
        if node == end:
            return
        adjacent = tree.get(node)
#         print(adjacent)
#         print(visit[node[0]][node[1]])
# up, right, down, left, parent[0:up,1:right,2:down,3:left]
        if (adjacent[0] == 1) and (visit[node[0]-1][node[1]] == 0):      #UP
#             print('if1')
#             print(tree.get((1,24)))
            newnode = (node[0]-1,node[1])
            queue.append(newnode)
            maze_tree[newnode][4] = 2
            visit[newnode[0]][newnode[1]] = 1
            count = count + 1

        if (adjacent[1] == 1) and (visit[node[0]][node[1]+1] == 0):     #right
#             print('if2')
#             print(tree.get((1,24)))
            newnode = (node[0],node[1]+1)
            queue.append(newnode)
            maze_tree[newnode][4] = 3
            visit[newnode[0]][newnode[1]] = 1
            count = count + 1

        if (adjacent[2] == 1) and (visit[node[0]+1][node[1]]) == 0:     #down
#             print('if3')
#             print(tree.get((1,24)))
            newnode = (node[0]+1,node[1])
            queue.append(newnode)
            maze_tree[newnode][4] = 0
            visit[newnode[0]][newnode[1]] = 1
            count = count + 1

        if (adjacent[3] == 1) and (visit[node[0]][node[1]-1] == 0):     #left
#             print('if4')
#             print(tree.get((1,24)))
            newnode = (node[0],node[1]-1)
            queue.append(newnode)
            maze_tree[newnode][4] = 1
            visit[newnode[0]][newnode[1]] = 1
            count = count + 1

#             visit[newnode[0]][newnode[1]] = 1


# In[37]:


bfs(maze_tree, (maze_start_height, maze_start_width),(maze_end_height,maze_end_width),maze_visited)


# In[38]:


maze_tree[(maze_end_height,maze_end_width)]


# In[39]:


end = (maze_end_height, maze_end_width)
start = (maze_start_height,maze_start_width)
t = end
queue=[]
#parent[0:up,1:right,2:down,3:left]
while t != start:
    if maze_tree[t][4]==0:
        t = (t[0]-1,t[1])
        queue.append(t)
    if maze_tree[t][4]==1:
        t = (t[0],t[1]+1)
        queue.append(t)
    if maze_tree[t][4]==2:
        t = (t[0]+1,t[1])
        queue.append(t)
    if maze_tree[t][4]==3:
        t = (t[0],t[1]-1)
        queue.append(t)


# In[40]:


for node in queue:
    if maze_dict[maze_sol[node[0]][node[1]]] != 1:
        maze_sol[node[0]][node[1]] = "."


# In[41]:


for n in range(len(maze_sol)):
    print("".join(maze_sol[n]))


# In[42]:


len(queue)


# In[43]:


queue


# In[44]:


count


# In[45]:


maze


###################################
# Import libraries 
###################################
import numpy as np
import time

###################################
# import data
###################################
with open("mediumSearch.txt") as maze_file:
#with open("mediumSearch.txt") as f:
#with open("smallSearch.txt") as f:
    maze = []
    for line in maze_file:
        row =[]
        for elem in line:
            if(elem=="\n"):
                break
            row.append(elem)
        maze.append(row)
    maze = np.array(maze)
    
###################################
# Helper Functions
###################################
'''
use A* search for the least distance between points
'''
#use BFS to find the minimum distance between two points
def BFS(maze,startpoint,endpoint):
    if(startpoint==endpoint):
        return 0
    #set up a stack for points
    points_stack=[(startpoint,0)]
    #initial a visited recorder
    visted = np.zeros((len(maze),len(maze[0])),dtype=int)
    visted[startpoint[0]][startpoint[1]]=1
    curr_dis=0
    #do it until it is empty
    while len(points_stack)!=0:
        curr=points_stack.pop(0)
        curr_dis=curr[1]
        curr=curr[0]
        curr_x = curr[0]
        curr_y = curr[1]
        if(maze[curr_x-1][curr_y]!="%" and not visted[curr_x-1][curr_y]):
            points_stack.append(((curr_x-1,curr_y),curr_dis+1))
            visted[curr[0]-1][curr_y]=1 
        if(maze[curr_x+1][curr_y]!="%" and not visted[curr_x+1][curr_y]):
            points_stack.append(((curr_x+1,curr_y),curr_dis+1))
            visted[curr_x+1][curr_y]=1
        if(maze[curr_x][curr_y-1]!="%" and not visted[curr_x][curr_y-1]):
            points_stack.append(((curr_x,curr_y-1),curr_dis+1))
            visted[curr_x][curr_y-1]=1
        if(maze[curr_x][curr_y+1]!="%"and not visted[curr_x][curr_y+1]):
            points_stack.append(((curr_x,curr_y+1),curr_dis+1))
            visted[curr_x][curr_y+1]=1
        if(curr==endpoint): 
            break
    return curr_dis
    
#use the MST as the hurestic
def MST(length_table, points_remain):
    #avoid affect the original data
    table = length_table.copy()
    if(len(points_remain) <= 1):
        return 0; 
    dis = 0
    while len(points_remain) > 1:
        #find the nearest point from the star point
        nearest_point = np.argmin(table[points_remain[0],points_remain[1:]])+1
        #add the distance to the total distance
        dis += table[points_remain[0]][points_remain[nearest_point]]
        for i in list((set(points_remain))-set([points_remain[nearest_point],points_remain[0]])):
            table[points_remain[nearest_point]][i] = min(table[points_remain[nearest_point]][i], table[points_remain[0]][i])
        points_remain.pop(0)
    return dis
     
     
###################################
# Main part solving problem
###################################
start_time = time.time()
start_x = 0
start_y = 0
for x in range (0,len(maze)):
        for y in range (0,len(maze[0])):
            if (maze[x][y]=="P"):
                start_point = (x,y)
#set up a list to records all the points need to go
Points = []
Points.append(start_point)
for x in range (0,len(maze)):
        for y in range (0,len(maze[0])):
            if (maze[x][y]=="."):
                Points.append((x,y))
#set up a length_table to save the minimum length between each pair of points
points_num = len(Points)
path_len = np.zeros((points_num,points_num))
for x in range(0,points_num):
    for y in range(0,points_num):
        path_len[x][y]=BFS(maze,Points[x],Points[y])
        
#use a* search to get the shortest path


num = len(path_len)
all_dot = list(range(num))
other_points = [{0:{}}]
path = [0]
path_no = 0
all_path = []
expanded = 0
#append the best next point to the path until all the points are in the path
while len(path)<num: 
    if len(other_points) < len(path):
        other_points.append({})
    if len(path) > 1:
        other_points[len(path)-1][path_no] = {}
    distance = sum([path_len[path[j]][path[j+1]] for j in range(len(path)-1)])
    #calculate the minimum cost+heuristic
    for i in list(set(all_dot)-set(path)):
        heuristic = MST(path_len, list(set(all_dot)-set(path)-set([i])))
        cost = distance + path_len[path[-1]][i]
        f = cost+heuristic
        other_points[len(path)-1][path_no][i] = f 
    #find the minimum
    min_f = 9999999999
    for point in range(0,len(other_points)):
        for cor in other_points[point]:
            next_node = sorted(other_points[point][cor], key=other_points[point][cor].__getitem__)[0]
            pos_f = sorted(other_points[point][cor].values())[0]
            if pos_f <= min_f:
                key = next_node
                min_f = pos_f
                min_node = point
                min_pos = cor
    if min_pos == path_no and min_node == len(path)-1:
        path.append(key)
    else:
        if path_no < len(all_path):
            all_path[path_no] = path
        else:
            all_path.append(path)   
        if min_node < len(path)-1:
            path = all_path[min_pos][:min_node+1]
            path.append(key)
            path_no = len(all_path)
        else:
            path = all_path[min_pos]
            path_no = min_pos
    if len(other_points[min_node][min_pos]) == 1:
        other_points[min_node][min_pos] = {0:np.inf}
    else:
        other_points[min_node][min_pos].pop(key)
    expanded+=path_len[path[-1]][path[-2]]

end_time = time.time()

###################################
# Print out some parameters of result
###################################
print("running time = ", end_time - start_time, "s")
print(path, expanded)
print(sum([path_len[path[j]][path[j+1]] for j in range(len(path)-1)]))
maze_sol = maze.copy()
for i in range(1,len(path)):
    #convert the number greater than 10 to lower case letter
    if(i<10):
        maze_sol[Points[path[i]][0],Points[path[i]][1]] = i
    else:
        maze_sol[Points[path[i]][0],Points[path[i]][1]] = chr(i+97-10)[-1]
    print(Points[path[i]])
file = open('medium_solution.txt','w')
for i in range(len(maze_sol)):
    for j in range(len(maze_sol[0])):
        file.write(maze_sol[i][j])
    file.write('\n')
file.close()
print("running time = ", end_time - start_time, "s")
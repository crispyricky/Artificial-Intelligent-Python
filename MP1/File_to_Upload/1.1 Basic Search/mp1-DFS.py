###################################
# Import libraries 
###################################
import numpy as np

###################################
# import data
###################################
#read the data to a np_array and find the start point & the end point
with open('openMaze.txt') as f:
        maze = []
        for y, line in enumerate(f):
            row = []
            for x, char in enumerate(line):
                if(char=='.'):
                    end = (y,x)
                if(char=='P'):
                    start = (y,x)
                if(char=='\n'):
                    break
                row.append(char)
            maze.append(row)
        maze_data = np.array(maze)
height = len(maze_data)
width = len(maze_data[0])

###################################
# main part for solving problem
###################################    
# track visited points to avoid visiting a dot multiple points
visited = np.zeros((height, width))
# create the queue of points
points_queue = []
# create a path dic to track back
comefrom = {}
# track node expanded
i = 0

#push the first node in
points_queue.append(start)

while points_queue!=[]:
    curr_point = points_queue.pop()
    cur_y = curr_point[0]
    cur_x = curr_point[1]
    visited[cur_y][cur_x] = 1
    i+=1
        
    if curr_point==end:
        break
    else:
        if maze[cur_y+1][cur_x]!='%' and not visited[cur_y+1][cur_x]:
            points_queue.append((cur_y+1, cur_x))
            comefrom[(cur_y+1, cur_x)] = (cur_y, cur_x)
        if maze[cur_y-1][cur_x]!='%' and not visited[cur_y-1][cur_x]:
            points_queue.append((cur_y-1, cur_x))
            comefrom[(cur_y-1, cur_x)] = (cur_y, cur_x)
        if maze[cur_y][cur_x+1]!='%' and not visited[cur_y][cur_x+1]:
            points_queue.append((cur_y, cur_x+1))
            comefrom[(cur_y, cur_x+1)] = (cur_y, cur_x)
        if maze[cur_y][cur_x-1]!='%' and not visited[cur_y][cur_x-1]:
            points_queue.append((cur_y, cur_x-1))
            comefrom[(cur_y, cur_x-1)] = (cur_y, cur_x)
        
# track back from the end
# save the solution to the maze_data
cur = (end[0], end[1])
pathLen = 0
while cur != (start[0], start[1]):
    maze_data[cur[0]][cur[1]]='.'
    cur = comefrom[cur]
    pathLen+=1
#set the start point back to 'Pd'
maze_data[start[0]][start[1]] = 'P'

#print the expanded nodes and the path cost
print("Expanded Nodes: ",i)
print("Path Cost:",pathLen)

# output to txt files
output = ""
for rows in maze_data:
    for elem in rows:
        output += elem
    output+='\n'
with open("q1_dfs_open_solution.txt", "w") as text_file:
    print(output, file=text_file)
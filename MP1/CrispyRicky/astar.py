import numpy

result = []
with open('mediumMaze.txt') as inputfile:
    for line in inputfile:
        result.append(list(line.strip()))
result_0 = result[1:-1]
#Remove up and bottom wall
result_1 = []
for n in range(len(result_0)):
    result_1.append(result_0[n][1:-1])
    #Remove left and right wall
for m in range(len(result_1)):
    for n in range(len(result_1[m])):
        if result_1[m][n] == "%":
            result_1[m][n] = 1
            # convert to 1 if wall
        elif result_1[m][n] == ".":
            print ("Ending at ({},{})".format(m,n))
            # print ending point
            result_1[m][n] = 0
            # convert to 0 if ending point
        elif result_1[m][n] == "P":
            print ("Starting at ({},{})".format(m,n))
            # print starting point
            result_1[m][n]= 0
            # convert to 0 if starting point
        else: result_1[m][n] = 0
            # convert to 0 if vacant

result_2 = numpy.array(result_1)

print (result_2)

from heapq import *

def heuristic(a, b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1])

def astar(array, start, goal):

    neighbors = [(0,1),(0,-1),(1,0),(-1,0)]

    close_set = set()
    came_from = {}
    gscore = {start:0}
    fscore = {start:heuristic(start, goal)}
    oheap = []

    heappush(oheap, (fscore[start], start))

    while oheap:

        current = heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:
                    if array[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue

            if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heappush(oheap, (fscore[neighbor], neighbor))

    return False

path = (astar(result_2, (20,58), (0,0)))
print (path)

for n in path:
    result[n[0]+1][n[1]+1] = "."
for n in range(len(result)):
    print("".join(result[n]))

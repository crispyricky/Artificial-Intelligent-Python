###################################
# Import libraries 
###################################
import numpy as np

###################################
# import data
###################################
maze_file = open("mediumMaze.txt","r")
line = maze_file.read();
data = np.genfromtxt("mediumMaze.txt",delimiter=1,dtype = "|S10")
#if data[x][y] == b'%', it's a wall
#if data[x][y] == b'.', it's the goal
#if data[x][y] == b' ', it's the path
#if data[x][y] == b'P', it's the start point

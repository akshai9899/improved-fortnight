import sys
from api import *
import numpy as np
import cv2
import matplotlib.pyplot as plt


#######    YOUR CODE FROM HERE #######################
def level1(botId):
    moveType = 5
    botsPose = get_botPose_list()
    obstaclePose = get_obstacles_list()
    greenZone = get_greenZone_list()
    redZone = get_redZone_list()
    originalGreenZone = get_original_greenZone_list()

    matrix = np.zeros((200,200), dtype=np.int)

    
    for obstacle in obstaclePose:
        for x in range(obstacle[0][0] , obstacle[2][0]):
            for y in range(obstacle[0][1], obstacle[1][1]):
                matrix[x][y] = 1
    

    initial_pos = tuple(botsPose[0])
    path = djkstra(matrix, 200, 200, initial_pos, (199,199))
    moves = moves_from_path(path)
    
    print(path)
    print(moves)
    
    img = np.zeros((200,200,3), np.uint8)

    for obstacle in obstaclePose:
        cv2.rectangle(img, tuple(obstacle[0]), tuple(obstacle[2]), (255,255,255), -1)
    
    n = len(path) - 1
    for i,co in enumerate(path):
        if i == 0:
            continue
        if i == n:
            continue
        cv2.line(img, tuple(path[i-1]), tuple(co), (0,255,0), 2)

    # cv2.imshow('image', img)
    # cv2. waitKey(0)
    # cv2.destroyAllWindows()
    plt.imshow(img)
    plt.show()

    for move in moves:
        successful_move, mission_complete = send_command(botId, move)



    # while True:
    #     successful_move, mission_complete = send_command(botId, moveType)
    #     if not mission_complete:
    #         if not successful_move:
    #             moveType = 1 + (moveType+1)%8
    #     else:
    #         # The mission has been completed. You may now exit.
    #         # The final score will be displayed on the screen
    #         break

def level2(botId):
    pass

def level3(botId):
    pass

def level4(botId):
    pass

def level5(botId):
    pass

def level6(botId):
    pass


def djkstra(matrix, rows, cols, start, end):

    HIGH = 10000
    distances = np.zeros((rows,cols), np.int)
    distances.fill(1000)
    visited = matrix


    parents = [[(None,None) for j in range(cols)] for x in range(rows)]

   
    distances[start[0]][start[1]] = 0
    value_sum = rows*cols 

    while(np.sum(visited) !=  value_sum):
        tmp = distances.copy()
        tmp[visited == 1] = HIGH
        min_pos = np.where(tmp == tmp.min())
        x,y = min_pos[0][0], min_pos[1][0]
        visited[x][y] = 1

        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            pos_x, pos_y = x + new_position[0], y + new_position[1]

            if(pos_x < 0 or pos_x >= rows or pos_y < 0 or pos_y >= cols):
                continue

            if(visited[pos_x][pos_y] == 1):
                continue

            if(distances[pos_x][pos_y] > distances[x][y] + 1):
                distances[pos_x][pos_y] = distances[x][y] + 1
                parents[pos_x][pos_y] = x,y

            if((pos_x,pos_y) == end):
                break
        

    parent_x, parent_y = end[0], end[1]
    path = []

    while(parent_x != None or parent_y != None):
        path.append((parent_x, parent_y))
        parent_x, parent_y = parents[parent_x][parent_y]
    
    path.reverse()

    return path



    
def moves_from_path(path):
    moves = []
    current = None
    
    for point in path:

        if current == None:
            current = point
            continue
        else:
            x1,y1 = current
            x2, y2 = point
        
        if x2 > x1:
            if y1 == y2:
                moves.append(4)
                current = point
                continue
            elif y1 < y2:
                moves.append(5)
                current = point
                continue
            else:
                moves.append(3)
                current = point
                continue
        elif x1 == x2:
            if y2>y1:
                moves.append(6)
                current = point
                continue
            else:
                moves.append(2)
                current = point
                continue
        else:
            if y1 == y2:
                moves.append(8)
                current = point
                continue
            elif y1 < y2:
                moves.append(7)
                current = point
                continue
            else:
                moves.append(1)
                current = point
                continue
        
    return moves




#######    DON'T EDIT ANYTHING BELOW  #######################

if  __name__=="__main__":
    botId = int(sys.argv[1])
    level = get_level()
    if level == 1:
        level1(botId)
    elif level == 2:
        level2(botId)
    elif level == 3:
        level3(botId)
    elif level == 4:
        level4(botId)
    elif level == 5:
        level5(botId)
    elif level == 6:
        level6(botId)
    else:
        print("Wrong level! Please restart and select correct level")










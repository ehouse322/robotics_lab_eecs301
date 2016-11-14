import sys

class EECSMap():
    def __init__(self):
        self.horizontalWalls = [[0 for x in range(8)] for x in range(9)]
        self.verticalWalls = [[0 for x in range(9)] for x in range(8)]
        self.costMap = [[0 for x in range(8)] for x in range(8)]

        self.horizontalWalls[0][0] = 1
        self.horizontalWalls[0][1] = 1
        self.horizontalWalls[0][2] = 1
        self.horizontalWalls[0][3] = 1
        self.horizontalWalls[0][4] = 1
        self.horizontalWalls[0][5] = 1
        self.horizontalWalls[0][6] = 1
        self.horizontalWalls[0][7] = 1
        self.horizontalWalls[1][0] = 0
        self.horizontalWalls[1][1] = 1
        self.horizontalWalls[1][2] = 1
        self.horizontalWalls[1][3] = 1
        self.horizontalWalls[1][4] = 1
        self.horizontalWalls[1][5] = 1
        self.horizontalWalls[1][6] = 0
        self.horizontalWalls[1][7] = 1
        self.horizontalWalls[2][0] = 0
        self.horizontalWalls[2][1] = 1
        self.horizontalWalls[2][2] = 1
        self.horizontalWalls[2][3] = 1
        self.horizontalWalls[2][4] = 0
        self.horizontalWalls[2][5] = 0
        self.horizontalWalls[2][6] = 0
        self.horizontalWalls[2][7] = 0
        self.horizontalWalls[3][0] = 0
        self.horizontalWalls[3][1] = 1
        self.horizontalWalls[3][2] = 1
        self.horizontalWalls[3][3] = 0
        self.horizontalWalls[3][4] = 1
        self.horizontalWalls[3][5] = 0
        self.horizontalWalls[3][6] = 0
        self.horizontalWalls[3][7] = 0
        self.horizontalWalls[4][0] = 1
        self.horizontalWalls[4][1] = 1
        self.horizontalWalls[4][2] = 0
        self.horizontalWalls[4][3] = 0
        self.horizontalWalls[4][4] = 0
        self.horizontalWalls[4][5] = 0
        self.horizontalWalls[4][6] = 1
        self.horizontalWalls[4][7] = 1
        self.horizontalWalls[5][0] = 0
        self.horizontalWalls[5][1] = 0
        self.horizontalWalls[5][2] = 0
        self.horizontalWalls[5][3] = 0
        self.horizontalWalls[5][4] = 0
        self.horizontalWalls[5][5] = 0
        self.horizontalWalls[5][6] = 1
        self.horizontalWalls[5][7] = 1
        self.horizontalWalls[6][0] = 0
        self.horizontalWalls[6][1] = 0
        self.horizontalWalls[6][2] = 1
        self.horizontalWalls[6][3] = 0
        self.horizontalWalls[6][4] = 0
        self.horizontalWalls[6][5] = 1
        self.horizontalWalls[6][6] = 1
        self.horizontalWalls[6][7] = 1
        self.horizontalWalls[7][0] = 0
        self.horizontalWalls[7][1] = 1
        self.horizontalWalls[7][2] = 1
        self.horizontalWalls[7][3] = 0
        self.horizontalWalls[7][4] = 0
        self.horizontalWalls[7][5] = 1
        self.horizontalWalls[7][6] = 1
        self.horizontalWalls[7][7] = 0
        self.horizontalWalls[8][0] = 1
        self.horizontalWalls[8][1] = 1
        self.horizontalWalls[8][2] = 1
        self.horizontalWalls[8][3] = 1
        self.horizontalWalls[8][4] = 1
        self.horizontalWalls[8][5] = 1
        self.horizontalWalls[8][6] = 1
        self.horizontalWalls[8][7] = 1

        self.verticalWalls[0][0] = 1
        self.verticalWalls[0][1] = 0
        self.verticalWalls[0][2] = 0
        self.verticalWalls[0][3] = 0
        self.verticalWalls[0][4] = 0
        self.verticalWalls[0][5] = 0
        self.verticalWalls[0][6] = 0
        self.verticalWalls[0][7] = 0
        self.verticalWalls[0][8] = 1
        self.verticalWalls[1][0] = 1
        self.verticalWalls[1][1] = 1
        self.verticalWalls[1][2] = 0
        self.verticalWalls[1][3] = 0
        self.verticalWalls[1][4] = 0
        self.verticalWalls[1][5] = 0
        self.verticalWalls[1][6] = 1
        self.verticalWalls[1][7] = 1
        self.verticalWalls[1][8] = 1
        self.verticalWalls[2][0] = 1
        self.verticalWalls[2][1] = 0
        self.verticalWalls[2][2] = 0
        self.verticalWalls[2][3] = 0
        self.verticalWalls[2][4] = 0
        self.verticalWalls[2][5] = 1
        self.verticalWalls[2][6] = 1
        self.verticalWalls[2][7] = 1
        self.verticalWalls[2][8] = 1
        self.verticalWalls[3][0] = 1
        self.verticalWalls[3][1] = 0
        self.verticalWalls[3][2] = 0
        self.verticalWalls[3][3] = 1
        self.verticalWalls[3][4] = 1
        self.verticalWalls[3][5] = 1
        self.verticalWalls[3][6] = 0
        self.verticalWalls[3][7] = 0
        self.verticalWalls[3][8] = 1
        self.verticalWalls[4][0] = 1
        self.verticalWalls[4][1] = 0
        self.verticalWalls[4][2] = 0
        self.verticalWalls[4][3] = 1
        self.verticalWalls[4][4] = 1
        self.verticalWalls[4][5] = 1
        self.verticalWalls[4][6] = 1
        self.verticalWalls[4][7] = 0
        self.verticalWalls[4][8] = 1
        self.verticalWalls[5][0] = 1
        self.verticalWalls[5][1] = 1
        self.verticalWalls[5][2] = 1
        self.verticalWalls[5][3] = 0
        self.verticalWalls[5][4] = 1
        self.verticalWalls[5][5] = 0
        self.verticalWalls[5][6] = 0
        self.verticalWalls[5][7] = 0
        self.verticalWalls[5][8] = 1
        self.verticalWalls[6][0] = 1
        self.verticalWalls[6][1] = 1
        self.verticalWalls[6][2] = 0
        self.verticalWalls[6][3] = 1
        self.verticalWalls[6][4] = 0
        self.verticalWalls[6][5] = 0
        self.verticalWalls[6][6] = 0
        self.verticalWalls[6][7] = 1
        self.verticalWalls[6][8] = 1
        self.verticalWalls[7][0] = 1
        self.verticalWalls[7][1] = 0
        self.verticalWalls[7][2] = 0
        self.verticalWalls[7][3] = 0
        self.verticalWalls[7][4] = 1
        self.verticalWalls[7][5] = 0
        self.verticalWalls[7][6] = 0
        self.verticalWalls[7][7] = 0
        self.verticalWalls[7][8] = 1

        for i in range(8):
            for j in range(8):
                self.costMap[i][j] = 0

        self.obstacle_size_x = 8
        self.obstacle_size_y = 8
        self.costmap_size_x = 8
        self.costmap_size_y = 8


    def printObstacleMap(self):
        print("Obstacle Map: ")
        for i in range(8):
            for j in range(8):
                if (self.horizontalWalls[i][j] == 0):
                    if i == 0:
                        sys.stdout.write(" ---")
                    else:
                        sys.stdout.write("    ")
                else:
                    sys.stdout.write(" ---")

            print(" ")
            for j in range(8):
                if (self.verticalWalls[i][j] == 0):
                    if j == 7:
                        sys.stdout.write("  O |")
                    elif j == 0:
                        sys.stdout.write("| O ")
                    else:
                        sys.stdout.write("  O ")
                else:
                    if j == 7:
                        sys.stdout.write("| O |")
                    else:
                        sys.stdout.write("| O ")
            print(" ")
        for j in range(8):
                sys.stdout.write(" ---")
        print(" ")

our_map = EECSMap()
our_map.printObstacleMap()
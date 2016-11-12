#!/usr/bin/env python
import roslib
import rospy
import signal
import sys
import time
import random
from fw_wrapper.srv import *
from map_empty import *
import pickle

# -----------SERVICE DEFINITION-----------
# allcmd REQUEST DATA
# ---------
# string command_type
# int8 device_id
# int16 target_val
# int8 n_dev
# int8[] dev_ids
# int16[] target_vals

# allcmd RESPONSE DATA
# ---------
# int16 val
# --------END SERVICE DEFINITION----------

# ----------COMMAND TYPE LIST-------------
# GetMotorTargetPosition
# GetMotorCurrentPosition
# GetIsMotorMoving
# GetSensorValue
# GetMotorWheelSpeed
# SetMotorTargetPosition
# SetMotorTargetSpeed
# SetMotorTargetPositionsSync
# SetMotorMode
# SetMotorWheelSpeed

# wrapper function to call service to set a motor mode
# 0 = set target positions, 1 = set wheel moving
def setMotorMode(motor_id, target_val):
    rospy.wait_for_service('allcmd')
    try:
        send_command = rospy.ServiceProxy('allcmd', allcmd)
        resp1 = send_command('SetMotorMode', motor_id, target_val, 0, [0], [0])
        return resp1.val
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

# wrapper function to call service to get motor wheel speed
def getMotorWheelSpeed(motor_id):
    rospy.wait_for_service('allcmd')
    try:
        send_command = rospy.ServiceProxy('allcmd', allcmd)
        resp1 = send_command('GetMotorWheelSpeed', motor_id, 0, 0, [0], [0])
        return resp1.val
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

# wrapper function to call service to set motor wheel speed
def setMotorWheelSpeed(motor_id, target_val):
    rospy.wait_for_service('allcmd')
    try:
        send_command = rospy.ServiceProxy('allcmd', allcmd)
        resp1 = send_command('SetMotorWheelSpeed', motor_id, target_val, 0, [0], [0])
        return resp1.val
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

# wrapper function to call service to set motor target speed
def setMotorTargetSpeed(motor_id, target_val):
    rospy.wait_for_service('allcmd')
    try:
        send_command = rospy.ServiceProxy('allcmd', allcmd)
        resp1 = send_command('SetMotorTargetSpeed', motor_id, target_val, 0, [0], [0])
        return resp1.val
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

# wrapper function to call service to get sensor value
def getSensorValue(port):
    rospy.wait_for_service('allcmd')
    try:
        send_command = rospy.ServiceProxy('allcmd', allcmd)
        resp1 = send_command('GetSensorValue', port, 0, 0, [0], [0])
        return resp1.val
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

# wrapper function to call service to set a motor target position
def setMotorTargetPositionCommand(motor_id, target_val):
    rospy.wait_for_service('allcmd')
    try:
        send_command = rospy.ServiceProxy('allcmd', allcmd)
        resp1 = send_command('SetMotorTargetPosition', motor_id, target_val, 0, [0], [0])
        return resp1.val
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

# wrapper function to call service to get a motor's current position
def getMotorPositionCommand(motor_id):
    rospy.wait_for_service('allcmd')
    try:
        send_command = rospy.ServiceProxy('allcmd', allcmd)
        resp1 = send_command('GetMotorCurrentPosition', motor_id, 0, 0, [0], [0])
        return resp1.val
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

# wrapper function to call service to check if a motor is currently moving
def getIsMotorMovingCommand(motor_id):
    rospy.wait_for_service('allcmd')
    try:
        send_command = rospy.ServiceProxy('allcmd', allcmd)
        resp1 = send_command('GetIsMotorMoving', motor_id, 0, 0, [0], [0])
        return resp1.val
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e
        
#direction lists
#this was made to keep track of directions. the idea was that every time it turned right we would subtract 90 degrees and every time it turned left we would add 90 degrees and that way we would always know the direction the robot was facing. it is not working yet because when we tried to add 90 degrees after using the turn function, it would add continuosly
def generateDirections():
    south = []
    for i in range(20):
        add_pos = i * 360
        add_neg = i * -360
        south.append(add_pos)
        south.append(add_neg)
    
    north = []
    for i in range(1, 20, 2):
        add_pos = i * 180
        add_neg = i * -180
        north.append(add_pos)
        north.append(add_neg)
        
    west = []
    for i in range(1, 30, 4):
        add_pos = i * 90
        add_neg = i *-270
        west.append(add_pos)
        west.append(add_neg)

    east = []
    for i in range(1, 30, 4):
        add_pos = i * -90
        add_neg = i * 270
        east.append(add_pos)
        east.append(add_neg)

#check the direction

def checkDirection():
    if direction in south:
        print "I am facing south"
    elif direction in north:
        print "I am facing north"
    elif direction in east:
        print "I am facing east"
    elif direction in west:
        print "I am facing west"   

# practice function to to get wheels moving
def moveForwardOne(count=0):
    #if time.clock() < 0.4400:
    print "I am moving"
    while count < 5:
        setMotorWheelSpeed(5, 1430)
        setMotorWheelSpeed(6, 1430)
        setMotorWheelSpeed(15, 450)
        setMotorWheelSpeed(16, 450)
        rospy.sleep(0.65)
        count += 1
    setMotorWheelSpeed(5, 0)
    setMotorWheelSpeed(6, 0)
    setMotorWheelSpeed(15, 0)
    setMotorWheelSpeed(16, 0)
        
def moveBackOne(count=0):
    print "I am moving"
    while count < 4:
        setMotorWheelSpeed(5, 450)
        setMotorWheelSpeed(6, 450)
        setMotorWheelSpeed(15, 1545)
        setMotorWheelSpeed(16, 1545)
        rospy.sleep(0.7)
        count += 1
    setMotorWheelSpeed(15, 0)
    setMotorWheelSpeed(16, 0)
    setMotorWheelSpeed(5, 0)
    setMotorWheelSpeed(6, 0)

def moveForward():
    setMotorWheelSpeed(5, 1692)
    setMotorWheelSpeed(6, 1692)
    setMotorWheelSpeed(15, 750)
    setMotorWheelSpeed(16, 750)

def turnRightHelper():
    setMotorWheelSpeed(5, 190)
    setMotorWheelSpeed(6, 190)
    setMotorWheelSpeed(15, 190)
    setMotorWheelSpeed(16, 190)
            
def turnLeftHelper():
    setMotorWheelSpeed(5, 1190)
    setMotorWheelSpeed(6, 1190)
    setMotorWheelSpeed(15, 1190)
    setMotorWheelSpeed(16, 1190)    
    
def turnRight(count=0):
    global direction
    #if time.clock() < 0.36899:
    print "I should turn right"
    while count < 5:
        turnRightHelper()
        rospy.sleep(0.54)
        count += 1
        #print count
    setMotorWheelSpeed(5, 0)
    setMotorWheelSpeed(6, 0)
    setMotorWheelSpeed(15, 0)
    setMotorWheelSpeed(16, 0)
        
def turnLeft(count=0):
    global direction
    print "I should turn left"
    while count < 5:
    #if time.clock() < 0.391:
        turnLeftHelper()
        rospy.sleep(0.65)
        count += 1
        #print count
    setMotorWheelSpeed(5, 0)
    setMotorWheelSpeed(6, 0)
    setMotorWheelSpeed(15, 0)
    setMotorWheelSpeed(16, 0)    

global our_map
our_map = EECSMap()

def getDirection(i,j, heading):
    global our_map
    directions = [DIRECTION.South, DIRECTION.East, DIRECTION.West]
    
    turnLeftDict = {DIRECTION.South: DIRECTION.East, DIRECTION.East: DIRECTION.North, DIRECTION.North: DIRECTION.West, DIRECTION.West: DIRECTION.South}
    
    turnRightDict = {DIRECTION.South: DIRECTION.West, DIRECTION.East: DIRECTION.South, DIRECTION.North: DIRECTION.East, DIRECTION.West: DIRECTION.North}

    for direction in directions:
        if our_map.getNeighborObstacle(i,j,direction) == 0:
            if direction == DIRECTION.South:
                if heading == DIRECTION.South:
                    if frontBlocked() == 0:
                        return direction        
                if heading == DIRECTION.East:
                    if rightBlocked() == 0:
                        return direction
                if heading == DIRECTION.West:
                    if leftBlocked() == 0:
                        return direction
            if direction == DIRECTION.West:
                if heading == DIRECTION.South:
                    if rightBlocked() == 0:
                        return direction
                if heading == DIRECTION.North:
                    if leftBlocked() == 0:
                        return direction
                if heading == DIRECTION.West:
                    if frontBlocked() == 0:
                        return direction
            if direction == DIRECTION.East:
                if heading == DIRECTION.South:
                    if leftBlocked() == 0:
                        return direction
                if heading == DIRECTION.North:
                    if rightBlocked() == 0:
                        return direction
                if heading == DIRECTION.East:
                    if frontBlocked() == 0:
                        return direction
                        
#    if heading == DIRECTION.South: 
#        choice_direction = DIRECTION.North
#        return choice_direction
#    if heading == DIRECTION.North:
#        choice_direction = DIRECTION.South
#        return choice_direction
#    if heading == DIRECTION.East:
#        choice_direction = DIRECTION.West
#        return choice_direction
#    if heading == DIRECTION.West:
#        choice_direction = DIRECTION.East
#        return choice_direction

def wander(i, j, heading):
    '''
    Prints out the appropriate direction the robot should walk in
    Can likely be hooked up to travel() in order to perform the correct movement
    This replaces the previous random.choice logic
    '''
    global our_map
    directions = [DIRECTION.South, DIRECTION.East, DIRECTION.West, DIRECTION.North]
    turnLeftDict = {DIRECTION.South: DIRECTION.East, DIRECTION.East: DIRECTION.North, DIRECTION.North: DIRECTION.West, DIRECTION.West: DIRECTION.South}
    turnRightDict = {DIRECTION.South: DIRECTION.West, DIRECTION.East: DIRECTION.South, DIRECTION.North: DIRECTION.East, DIRECTION.West: DIRECTION.North}
    dirSet = set()
    for val in directions:
        dirSet.add(val)
    visited = set()
    visited.add((i,j))
    #pick a direction to travel that is not blocked or previously visited
    blockedDir = recordWalls(heading, i, j)
    if rightBlocked() == 1:
        blockedDir.add(DIRECTION.West)
    if leftBlocked() == 1:
        blockedDir.add(DIRECTION.East)
    if frontBlocked() == 1:
        blockedDir.add(DIRECTION.South)
    possibleDirections = dirSet - blockedDir
    notVisitedDirections = list(possibleDirections)
    if len(possibleDirections) == 1:
        return list(possibleDirections)[0]
    for direction in possibleDirections:
        if direction == directions[0]: # south
            if (i+1,j) in visited:
                notVisitedDirections.remove(directions[0])
        elif direction == directions[1]: # east
            if (i,j+1) in visited:
                notVisitedDirections.remove(directions[1])
        elif direction == directions[2]: # west
            if (i,j-1) in visited:
                notVisitedDirections.remove(directions[2])
        elif direction == directions[3]: # north
            if (i-1,j) in visited:
                notVisitedDirections.remove(directions[3])
    if len(notVisitedDirections) == 0:
        return random.choice(list(possibleDirections))
    else:
        return random.choice(notVisitedDirections)
    
def travel2():
    directions = [DIRECTION.South, DIRECTION.East, DIRECTION.West, DIRECTION.North]
    
    turnLeftDict = {DIRECTION.South: DIRECTION.East, DIRECTION.East: DIRECTION.North, DIRECTION.North: DIRECTION.West, DIRECTION.West: DIRECTION.South}
    
    turnRightDict = {DIRECTION.South: DIRECTION.West, DIRECTION.East: DIRECTION.South, DIRECTION.North: DIRECTION.East, DIRECTION.West: DIRECTION.North}
    global our_map
    i = 0
    j = 0
    heading = DIRECTION.South
    wanderingVisited = set()
    wanderingVisited.add((i, j))
    while len(wanderingVisited) < 64:
        #recordWalls(heading, i, j)
        choice_direction = wander(i, j, heading)
        #choice_direction = random.choice(directions)
        if choice_direction == DIRECTION.South:
            if heading == DIRECTION.South:
                if j == 7:
                    continue
                else:
                    j += 1                                        
            elif heading == DIRECTION.East:
                if i == 7:
                    continue
                else:
                    i += 1                                
            elif heading == DIRECTION.North:
                if j == 0: 
                    continue
                else:
                    j -= 1
            else: #west
                if i == 0:
                    continue
                else:
                    i -= 1
            moveForwardOne()
            print "moving forward"
            rospy.sleep(1)
        if choice_direction == DIRECTION.East:
            heading = turnLeftDict[heading] 
            if heading == DIRECTION.South:
                if j == 7:
                    heading = turnRightDict[heading]
                    continue
                else:
                    j += 1
            elif heading == DIRECTION.East:
                if i == 7:
                    heading = turnRightDict[heading]
                    continue
                else:
                    i += 1
            elif heading == DIRECTION.North:
                if j == 0:
                    heading = turnRightDict[heading]
                    continue
                else:
                    j -= 1
            else: #west
                if i == 0:
                    heading = turnRightDict[heading]
                    continue
                else:
                    i -= 1
            turnLeft()
            rospy.sleep(1)
            moveForwardOne()
            print "moving left"
            rospy.sleep(1)
        if choice_direction == DIRECTION.West:
            heading = turnRightDict[heading]
            if heading == DIRECTION.South:
                if j == 7:
                    heading = turnLeftDict[heading]
                    continue
                else:
                    j += 1
            elif heading == DIRECTION.East:
                if i == 7:
                    heading = turnLeftDict[heading]
                    continue
                else:
                    i += 1
            elif heading == DIRECTION.North:
                if j == 0:
                    heading = turnLeftDict[heading]
                    continue
                else:
                    j -= 1
            else: #west
                if i == 0:
                    heading = turnLeftDict[heading]
                    continue
                else:
                    i -= 1
            turnRight()
            rospy.sleep(1)
            moveForwardOne()
            print "moving right"
            rospy.sleep(1)
        if choice_direction == DIRECTION.North:
            if heading == DIRECTION.South:
                if j == 0:
                    continue
                else:
                    j -= 1                                        
            elif heading == DIRECTION.East:
                if i == 0:
                    continue
                else:
                    i -= 1                                
            elif heading == DIRECTION.North:
                if j == 7: 
                    continue
                else:
                    j += 1
            else: #west
                if i == 7:
                    continue
                else:
                    i += 1
            moveBackOne()
            print "moving backward"
            rospy.sleep(1)
        print (i, j)
        print heading
        wanderingVisited.add((i, j))
        print wanderingVisited
        

#traveling
#this was a function to try out using the map and obstacles. it would pick a direction randomly then travel in that one if it was not blocked. i dont know if this was particularly useful lol. 
def travel():
    directions = [DIRECTION.South, DIRECTION.East, DIRECTION.West, DIRECTION.North]
    
    turnLeftDict = {DIRECTION.South: DIRECTION.East, DIRECTION.East: DIRECTION.North, DIRECTION.North: DIRECTION.West, DIRECTION.West: DIRECTION.South}
    
    turnRightDict = {DIRECTION.South: DIRECTION.West, DIRECTION.East: DIRECTION.South, DIRECTION.North: DIRECTION.East, DIRECTION.West: DIRECTION.North}
    
    moveBackDict = {DIRECTION.South: DIRECTION.North, DIRECTION.East: DIRECTION.West, DIRECTION.North: DIRECTION.South, DIRECTION.West: DIRECTION.East}
    
    global our_map
    #our_map = EECSMap()
    i = 0
    j = 0
    heading = DIRECTION.South
    wanderingVisited = set()
    wanderingVisited.add((i,j))
    while len(wanderingVisited) < 64: #TODO: while there is still stuff to visit
        recordWalls(heading, i, j)
        choice_direction = random.choice(directions)
        if directions.index(choice_direction) == 0:
            print "moving forward"
            if frontBlocked() == 0:
                if our_map.getNeighborObstacle(i, j, heading) == 0:
                    print "front is clear"
                    if heading == DIRECTION.South:
                        if j == 7:
                            continue
                        else:
                            if (i,j+1) in wanderingVisited:
                                if rightBlocked() == 0 or leftBlocked() == 0:
                                    if (i-1, j) not in wanderingVisited or (i+1,j) not in wanderingVisited: 
                                        continue
                                    else:
                                        j += 1
                                else: j += 1
                            else:
                                j += 1
                                        
                    elif heading == DIRECTION.East:
                        if i == 7:
                            continue
                        else:
                            i += 1
                                
                    elif heading == DIRECTION.North:
                        if j == 0: 
                            continue
                        else:
                            j -= 1
                    else: #west
                        if i == 0:
                            continue
                        else:
                            i -= 1
                    moveForwardOne()
                    print "moving forward"
                    rospy.sleep(1)
            elif frontBlocked() == 1:
                print "oops, front is blocked."
        elif directions.index(choice_direction) == 1:
            print "moving left"
            print getSensorValue(5)
            print leftBlocked()
            print heading
            if leftBlocked() == 0:
                print leftBlocked()
                print "there is no wall to my left"
                heading = turnLeftDict[heading]
                print heading
                if our_map.getNeighborObstacle(i, j, heading) == 0:
                    print "left side is clear"
                    #heading = turnLeftDict[heading] 
                    if heading == DIRECTION.South:
                        if j == 7:
                            heading = turnRightDict[heading]
                            continue
                        else:
                            j += 1
                    elif heading == DIRECTION.East:
                        if i == 7:
                            heading = turnRightDict[heading]
                            continue
                        else:
                            i += 1
                    elif heading == DIRECTION.North:
                        if j == 0:
                            heading = turnRightDict[heading]
                            continue
                        else:
                            j -= 1
                    else: #west
                        if i == 0:
                            heading = turnRightDict[heading]
                            continue
                        else:
                            i -= 1
                    turnLeft()
                    rospy.sleep(1)
                    moveForwardOne()
                    print "moving left"
                    rospy.sleep(1)
                else:
                    heading = turnRightDict[heading]    
            elif leftBlocked() == 1:
                print "oops left is blocked"
        elif directions.index(choice_direction) == 2:
            print "moving right"
            if rightBlocked() == 0:
                heading = turnRightDict[heading]
                if our_map.getNeighborObstacle(i, j, heading) == 0:
                    print "right side is clear"
                    #heading = turnRightDict[heading]
                    if heading == DIRECTION.South:
                        if j == 7:
                            heading = turnLeftDict[heading]
                            continue
                        else:
                            j += 1
                    elif heading == DIRECTION.East:
                        if i == 7:
                            heading = turnLeftDict[heading]
                            continue
                        else:
                            i += 1
                    elif heading == DIRECTION.North:
                        if j == 0:
                            heading = turnLeftDict[heading]
                            continue
                        else:
                            j -= 1
                    else: #west
                        if i == 0:
                            heading = turnLeftDict[heading]
                            continue
                        else:
                            i -= 1
                    turnRight()
                    rospy.sleep(1)
                    moveForwardOne()
                    print "moving right"
                    rospy.sleep(1)
                else:
                    print our_map.getNeighborObstacle(i, j, choice_direction)
                    print "ello"
                    heading = turnLeftDict[heading]
            elif rightBlocked() == 1:
                print "oops, right is blocked"
        elif directions.index(choice_direction) == 3:
            print "moving back"
            heading = moveBackDict[heading]
            if our_map.getNeighborObstacle(i, j, choice_direction) == 0:
                "back is clear"
                if rightBlocked() == 1 and leftBlocked() == 1 and frontBlocked() == 1:
                    print "all other directions blocked"
                    if heading == DIRECTION.South:
                        if j == 0:
                            continue
                        else:
                            j -= 1
                    elif heading == DIRECTION.East:
                        if i == 0:
                            continue
                        else:
                            i -= 1
                    elif heading == DIRECTION.North:
                        if j == 7:
                            continue
                        else:
                            j += 1
                    else: #west
                        if i == 7:
                            continue
                        else:
                            i += 1
                    print "moving back"
                    moveBackOne()
                    rospy.sleep(1)
                else:
                    continue
            else:
                heading = moveBackDict[heading]
        print (i, j)
        print heading
        wanderingVisited.add((i, j))
        print wanderingVisited

#right sensor = 1
#left sensor = 5
#front sensor = 3        
def recordWalls(heading, i, j):
    #TODO: return directions that are blocked so we can remove them from the travel iteration
    global our_map
    blocked = set()
    #print (i, j, heading)
    if heading == DIRECTION.South:
        if getSensorValue(1) > 6:
            our_map.setObstacle(j, i, 1, DIRECTION.West)
            blocked.add(DIRECTION.West)
        if getSensorValue(5) > 10:
            our_map.setObstacle(j, i, 1, DIRECTION.East)
            blocked.add(DIRECTION.East)
        if getSensorValue(3) > 600:
            our_map.setObstacle(j, i, 1, heading)
            blocked.add(heading) 
    elif heading == DIRECTION.North:
        if getSensorValue(1) > 6:
            our_map.setObstacle(j, i, 1, DIRECTION.East)
            blocked.add(DIRECTION.East)
        if getSensorValue(5) > 10:
            our_map.setObstacle(j, i, 1, DIRECTION.West)
            blocked.add(DIRECTION.West)
        if getSensorValue(3) > 600:
            our_map.setObstacle(j, i, 1, heading)
            blocked.add(heading)
    elif heading == DIRECTION.East:
        if getSensorValue(1) > 6:
            our_map.setObstacle(j, i, 1, DIRECTION.South)
            blocked.add(DIRECTION.South)
        if getSensorValue(5) > 10:
            our_map.setObstacle(j, i, 1, DIRECTION.North)
            blocked.add(DIRECTION.North)
        if getSensorValue(3) > 600:
            our_map.setObstacle(j, i, 1, heading)
            blocked.add(heading)
    elif heading == DIRECTION.West:
        if getSensorValue(1) > 6:
            our_map.setObstacle(j, i, 1, DIRECTION.North)
            blocked.add(DIRECTION.North)
        if getSensorValue(5) > 10:
            our_map.setObstacle(j, i, 1, DIRECTION.South)
            blocked.add(DIRECTION.South)
        if getSensorValue(3) > 600:
            our_map.setObstacle(j, i, 1, heading)
            blocked.add(heading)
    our_map.printObstacleMap()
    return blocked
    

def frontBlocked():
    front = getSensorValue(3)
    if front > 600: 
        print front
        return 1
    else:
        return 0
        
def leftBlocked():
    left_side = getSensorValue(5)
    if left_side > 20:
        print left_side
        return 1
    else:
        return 0

def rightBlocked():        
    right_side = getSensorValue(1)
    print right_side
    if right_side > 5:
        print "right side is blocked"
        return 1
    else:
        print "right side is not blocked"
        return 0

def buildMap2(i_end, j_end, counter=0):
    # building wave propagation
    directions = [DIRECTION.South, DIRECTION.East, DIRECTION.West, DIRECTION.North]
    directory = []
    mustSet = False
    if i_end > 7 or i_end <= 0 or j_end > 7 or j_end <= 0:
        our_map.printCostMap()
        our_map.printObstacleMap()
        return
    else:
        print "have not reached goal"
        for direction in directions:
            isBlocked = our_map.getNeighborObstacle(i_end, j_end, direction)
            if isBlocked == 0:
                directory.append(direction)
                print "the path to the " + str(direction) + " is not blocked"
                if (i_end, j_end) not in visited:
                    visited.append((i_end, j_end))
        if 1 in directory and (i_end, j_end-1) not in visited: #north
            our_map.setNeighborCost(i_end, j_end, 1, counter)
            buildMap(i_end, j_end-1, counter+1)
        if 2 in directory and (i_end+1, j_end) not in visited: #east
            our_map.setNeighborCost(i_end, j_end, 2, counter)
            buildMap(i_end+1, j_end, counter+1)
        if 3 in directory and (i_end, j_end+1) not in visited: #south
            our_map.setNeighborCost(i_end, j_end, 3, counter)
            buildMap(i_end, j_end+1, counter+1)  
        if 4 in directory and (i_end-1, j_end) not in visited: #west 
            our_map.setNeighborCost(i_end, j_end, 4, counter)       
            buildMap(i_end-1, j_end, counter+1)

def buildMap(i, j):
    global our_map
    our_map = pickle.load(open('/home/rosuser/Desktop/mapfile.pkl'))
    # initialize cost map to all 1000
    for x in range(8):
        for y in range(8):
            our_map.setCost(x,y,1000)
            #our_map.printCostMap()
    our_map.setCost(i,j,0)
    buildMapHelper(i, j)
    our_map.printCostMap()
    our_map.printObstacleMap()
    
def buildMapHelper(i, j, counter=1):
    global our_map
    #print "hello"
    #our_map.printCostMap()
    directions = [DIRECTION.South, DIRECTION.East, DIRECTION.West, DIRECTION.North]
    if counter > 5:
        return
    for direction in directions:
        print direction
        print our_map.getNeighborObstacle(i, j, direction)
        if our_map.getNeighborObstacle(i, j, direction) == 0:
            print "no obstacle on map"
            print our_map.getNeighborCost(i, j, direction)
            if our_map.getNeighborCost(i, j, direction) > counter:
                print "surrounding cost is higher"
                our_map.setNeighborCost(i, j, direction, counter)
                our_map.printCostMap()
    for x in range(8):
        for y in range(8):
            if our_map.getCost(x,y) == counter:
                buildMapHelper(x,y,counter+1)

#def buildMapHelper2(i, j, counter=1):
#    directions = [DIRECTION.South, DIRECTION.East, DIRECTION.West, DIRECTION.North]
#    if counter > 18:
#        return
#    for direction in directions:
#        if our_map.getNeighborObstacle(i, j, direction) == 0:
#            if our_map.getNeighborCost(i, j, direction) > counter:
#                our_map.setNeighborCost(i, j, direction, counter)
#    buildMapHelper2(i,j,counter+1)
    #for x in range(8):
    #    for y in range(8):
    #        if our_map.getCost(x,y) == counter:
    #            buildMapHelper(x,y,counter+1)    

def genPath(i_start, j_start, i_end, j_end):
    #buildMap(i_end, j_end)
    # map build occurs in main function
    path = [(i_start, j_start)]
    directions = [DIRECTION.South, DIRECTION.East, DIRECTION.West, DIRECTION.North]
    i, j = i_start, j_start
    best_dir =  directions[0]
    while (i != i_end or j != j_end):
        # pick direction with lowest cost
        print path
        print i, j
        curr_cost = our_map.getCost(i, j)
        print curr_cost
        if i < 7 and j < 7:
            for direction in directions:
                if our_map.getNeighborObstacle(i, j, direction) == 0:
                    next_cost = our_map.getNeighborCost(i, j, direction)
                    if next_cost < curr_cost:
                        print next_cost
                        best_dir = direction
            if best_dir == directions[0]:
                i += 1
            if best_dir == directions[1]:
                j += 1
            if best_dir == directions[2]:
                j -= 1
            if best_dir == directions[3]:
                i -= 1
            path.append((i,j))
    print path
    return path
           
# planning fxn
def walkPath2(i_start, j_start, heading_start, i_end, j_end, heading_end):
    buildMap(i_end, j_end)
    path = genPath(i_start, j_start, i_end, j_end)
    past_dir = [heading_start]
    for i in range(len(path)-1):
        i_curr = path[i][0]
        j_curr = path[i][1]
        i_next = path[i+1][0]
        j_next = path[i+1][1]
        if i_curr != i_next:
            if i_curr > i_next:
                # head west
                if past_dir[-1] == DIRECTION.South:
                    turnRight()
                    rospy.sleep(5)
                if past_dir[-1] == DIRECTION.North:
                    turnLeft()
                    rospy.sleep(5)
                if past_dir[-1] == DIRECTION.East:
                    turnLeft()
                    turnLeft()
                    rospy.sleep(5)
                moveForwardOne()
                rospy.sleep(5)
                past_dir.append(DIRECTION.West)
            else:
                # head east
                if past_dir[-1] == DIRECTION.South:
                    turnLeft()
                    rospy.sleep(5)
                if past_dir[-1] == DIRECTION.North:
                    turnRight()
                    rospy.sleep(5)
                if past_dir[-1] == DIRECTION.West:
                    turnLeft()
                    turnLeft()
                    rospy.sleep(5)
                moveForwardOne()
                rospy.sleep(5)
                past_dir.append(DIRECTION.East)
        elif j_curr != j_next:
            if j_curr > j_next:
                # head north
                if past_dir[-1] == DIRECTION.East:
                    turnLeft()
                    rospy.sleep(5)
                if past_dir[-1] == DIRECTION.West:
                    turnRight()
                    rospy.sleep(5)
                if past_dir[-1] == DIRECTION.South:
                    turnLeft()
                    turnLeft()
                    rospy.sleep(5)
                moveForwardOne()
                rospy.sleep(5)
                past_dir.append(DIRECTION.North)
            else:
                # head south
                if past_dir[-1] == DIRECTION.East:
                    turnRight()
                    rospy.sleep(5)
                if past_dir[-1] == DIRECTION.West:
                    turnLeft()
                    rospy.sleep(5)
                if past_dir[-1] == DIRECTION.North:
                    turnLeft()
                    turnLeft()
                    rospy.sleep(5)
                moveForwardOne()
                rospy.sleep(5)
                past_dir.append(DIRECTION.South)
    print "end"
    return

# planning fxn
def walkPath(i_start, j_start, heading_start, i_end, j_end, heading_end):
    buildMap(i_end, j_end)
    path = genPath(i_start, j_start, i_end, j_end)
    past_dir = [heading_start]
    for i in range(len(path)-1):
        i_curr = path[i][0]
        j_curr = path[i][1]
        i_next = path[i+1][0]
        j_next = path[i+1][1]
        if j_curr != j_next:
            print "moving along j axis"
            if j_curr > j_next:
                # head west
                if past_dir[-1] == DIRECTION.South:
                    turnRight()
                    rospy.sleep(5)
                if past_dir[-1] == DIRECTION.North:
                    turnLeft()
                    rospy.sleep(5)
                if past_dir[-1] == DIRECTION.East:
                    turnLeft()
                    turnLeft()
                    rospy.sleep(5)
                moveForwardOne()
                rospy.sleep(5)
                past_dir.append(DIRECTION.West)
            else:
                print "I am moving East"
                # head east
                if past_dir[-1] == DIRECTION.South:
                    turnLeft()
                    rospy.sleep(5)
                if past_dir[-1] == DIRECTION.North:
                    turnRight()
                    rospy.sleep(5)
                if past_dir[-1] == DIRECTION.West:
                    turnLeft()
                    turnLeft()
                    rospy.sleep(5)
                moveForwardOne()
                rospy.sleep(5)
                past_dir.append(DIRECTION.East)
        elif i_curr != i_next:
            print "moving along i axis"
            if i_curr > i_next:
                print "I am moving North"
                # head north
                if past_dir[-1] == DIRECTION.East:
                    turnLeft()
                    rospy.sleep(5)
                if past_dir[-1] == DIRECTION.West:
                    turnRight()
                    rospy.sleep(5)
                if past_dir[-1] == DIRECTION.South:
                    turnLeft()
                    turnLeft()
                    rospy.sleep(5)
                moveForwardOne()
                rospy.sleep(5)
                past_dir.append(DIRECTION.North)
            else:
                # head south
                print "I am moving South"
                if past_dir[-1] == DIRECTION.East:
                    turnRight()
                    rospy.sleep(5)
                if past_dir[-1] == DIRECTION.West:
                    turnLeft()
                    rospy.sleep(5)
                if past_dir[-1] == DIRECTION.North:
                    turnLeft()
                    turnLeft()
                    rospy.sleep(5)
                moveForwardOne()
                rospy.sleep(5)
                past_dir.append(DIRECTION.South)
    print "end"
    return   

        
#shutdown function
def shutdown(sig, stackframe):
    print("caught ctrl-c!")
    with open('/home/rosuser/Desktop/mapfile.pkl', 'w') as f:
        pickle.dump(our_map, f)
    setMotorWheelSpeed(5, 0)
    setMotorWheelSpeed(6, 0)
    setMotorWheelSpeed(15, 0)
    setMotorWheelSpeed(16, 0)
    sys.exit(0)

# Main function
if __name__ == "__main__":
    rospy.init_node('example_node', anonymous=True)
    signal.signal(signal.SIGINT, shutdown)
    rospy.loginfo("Starting Group K Control Node...")
    setMotorMode(5, 1)
    setMotorMode(6, 1)
    setMotorMode(15, 1)
    setMotorMode(16, 1)
    #generateDirections()
    #buildMap(7,7)
    #direction = 0
    # control loop running at 10hz
    r = rospy.Rate(10) # 10hz
    keepGoing = True
    # read from command line
    if len(sys.argv) > 1:
        fxnToRun = sys.argv[1]
    else:
        fxnToRun = None
    while not rospy.is_shutdown():
        # call function to get sensor value
        # port = 5
        # sensor_reading = getSensorValue(port)
        # rospy.loginfo("Sensor value at port %d: %f", 5, sensor_reading)

        # call function to set motor position
        # motor_id = 1
        # target_val = 450
        # response = setMotorTargetPositionCommand(motor_id, target_val)
        
        # set_map = EECSMap()
        # set_map.printObstacleMap()
        #print getSensorValue(5)
        # practice moving wheels
        print getSensorValue(5)
        print getSensorValue(3)
        print getSensorValue(1)
        rospy.sleep(1)
        
        if fxnToRun == "wander":
             choice_direction = wander(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
             print choice_direction
        
        if fxnToRun == "moveForwardOne":
            if keepGoing == True:
                moveForwardOne()
                keepGoing = False
            
        if fxnToRun == "turnRight":
            if keepGoing == True:
                turnRight()
                keepGoing = False
            
        if fxnToRun == "turnLeft":
            if keepGoing == True:
                turnLeft()
                keepGoing = False
            
        if fxnToRun == "doNothing":
            pass
            
        if fxnToRun == "travel":
            travel()
            
        if fxnToRun == "moveBackOne":
            if keepGoing == True:
                moveBackOne()
                keepGoing = False
            
        if fxnToRun == "walkPath":
            walkPath(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]))
        
        if fxnToRun == "genPath":
            genPath(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
            print "finished"
            
        if fxnToRun == "buildMap":
            buildMap(int(sys.argv[2]), int(sys.argv[3]))
            
        # sleep to enforce loop rate
        r.sleep()

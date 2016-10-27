#!/usr/bin/env python
import roslib
import rospy
import signal
import sys
import time
import random
from fw_wrapper.srv import *
from map import *

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
def moveForwardOne():
    if time.clock() < 0.4400:
        print time.clock()
        print "I am moving"
        setMotorWheelSpeed(5, 1420)
        setMotorWheelSpeed(6, 1420)
        setMotorWheelSpeed(15, 450)
        setMotorWheelSpeed(16, 450)
    else:
        setMotorWheelSpeed(5, 0)
        setMotorWheelSpeed(6, 0)
        setMotorWheelSpeed(15, 0)
        setMotorWheelSpeed(16, 0)
        
def moveBackOne():
    if time.clock() < 0.4400:
        print time.clock()
        print "I am moving"
        setMotorWheelSpeed(15, 1460)
        setMotorWheelSpeed(16, 1460)
        setMotorWheelSpeed(5, 420)
        setMotorWheelSpeed(6, 420)
    else:
        setMotorWheelSpeed(5, 0)
        setMotorWheelSpeed(6, 0)
        setMotorWheelSpeed(15, 0)
        setMotorWheelSpeed(16, 0)

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
    
def turnRight():
    global direction
    if time.clock() < 0.36899:
        print time.clock()
        print "I should turn right"
        turnRightHelper()
    else:
        setMotorWheelSpeed(5, 0)
        setMotorWheelSpeed(6, 0)
        setMotorWheelSpeed(15, 0)
        setMotorWheelSpeed(16, 0)
        
def turnLeft():
    global direction
    if time.clock() < 0.391:
        print time.clock()
        print "I should turn left"
        turnLeftHelper()
    else:
        setMotorWheelSpeed(5, 0)
        setMotorWheelSpeed(6, 0)
        setMotorWheelSpeed(15, 0)
        setMotorWheelSpeed(16, 0)    

directions = [DIRECTION.South, DIRECTION.East, DIRECTION.West, DIRECTION.North]

#traveling
#this was a function to try out using the map and obstacles. it would pick a direction randomly then travel in that one if it was not blocked. i dont know if this was particularly useful lol. 
def travel():
    directions = [DIRECTION.South, DIRECTION.East, DIRECTION.West, DIRECTION.North]
    our_map = EECSMap()
    i = 0
    j = 0
    while time.clock() < 5:
        choice_direction = random.choice(directions)
        if directions.index(choice_direction) == 0:
            if our_map.getNeighborObstacle(i, j, choice_direction) == 0:
                print "moving south"
                moveForwardOne()
                i += 1
                rospy.sleep(5)
        elif directions.index(choice_direction) == 1:
            if our_map.getNeighborObstacle(i, j, choice_direction) == 0:
                print "moving east"
                turnLeft()
                rospy.sleep(8)
                moveForwardOne()
                j += 1
                rospy.sleep(5)
        elif directions.index(choice_direction) == 2:
            if our_map.getNeighborObstacle(i, j, choice_direction) == 0:
                print "moving west"
                turnRight()
                rospy.sleep(8)
                moveForwardOne()
                j -= 1
                rospy.sleep(5)
        elif directions.index(choice_direction) == 3:
            if our_map.getNeighborObstacle(i, j, choice_direction) == 0:
                print "moving north"
                moveBackOne()
                i -= 1
                rospy.sleep(5)
        print (i, j)       

our_map = EECSMap()
visited = []

def buildMap(i_end, j_end, counter=0):
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

def genPath(i_start, j_start, i_end, j_end):
    # map build occurs in main function
    path = [(i_start, j_start)]
    directions = [DIRECTION.South, DIRECTION.East, DIRECTION.West, DIRECTION.North]
    i, j = i_start, j_start
    counter = 0
    while i_start != i_end and j_start != j_end or counter < 15:
        # pick direction with lowest cost
        print path
        curr_cost = our_map.getCost(i, j)
        best_cost = 1000
        best_dir =  directions[0]
        for direction in directions:
            next_cost = our_map.getNeighborCost(i, j, direction)
            if next_cost < best_cost:
                best_cost = next_cost
                best_dir = direction
        if best_dir == directions[0]:
            j += 1
        if best_dir == directions[1]:
            i += 1
        if best_dir == directions[2]:
            i -= 1
        if best_dir == directions[3]:
            j -= 1
        path.append((i,j))
        counter += 1
        if (i,j) == (i_end, j_end):
            return path
    return path
           
# planning fxn
def walkPath(i_start, j_start, heading_start, i_end, j_end, heading_end):
    buildMap(i_end, j_end)
    path = genPath(i_start, j_start, i_end, j_end)
    curr = path.pop()
    print curr
    past_dir = [heading_start]
    for next in path:
        i_curr = curr[0]
        j_curr = curr[1]
        i_next = next[0]
        j_next = next[1]
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
    return
            
        
#shutdown function
def shutdown(sig, stackframe):
    print("caught ctrl-c!")
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
    generateDirections()
    direction = 0
    # control loop running at 10hz
    r = rospy.Rate(10) # 10hz
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
        
        # practice moving wheels
        if fxnToRun == "moveForwardOne":
            moveForwardOne()
            
        if fxnToRun == "turnRight":
            turnRight()
            
        if fxnToRun == "turnLeft":
            turnLeft()
            
        if fxnToRun == "doNothing":
            pass
            
        if fxnToRun == "travel":
            travel()
            
        if fxnToRun == "moveBackOne":
            moveBackOne()
            
        if fxnToRun == "walkPath":
            walkPath(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]))
            
        # sleep to enforce loop rate
        r.sleep()

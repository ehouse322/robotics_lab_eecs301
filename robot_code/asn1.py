#!/usr/bin/env python
import roslib
import rospy
from fw_wrapper.srv import *
import sys

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

def disco(motor_id=8, other_motor_id=7):
    ''' Makes the robot do the disco if nothing is near it -- optimized for motors 7 & 8 '''
    if getMotorPositionCommand(motor_id) in range(0, 10):
        up = True
        down = False
    else:
        up = False
        down = True
    print getMotorPositionCommand(motor_id)
    
    if getSensorValue(1) == 0:    
        if up == True:
            print "up is true"
            if getMotorPositionCommand(motor_id) in range(0, 10):
                print "done going up"
                up, down = False, True
                response = setMotorTargetPositionCommand(motor_id, 400)
                response2 = setMotorTargetPositionCommand(other_motor_id, 600) 
        if down == True:
            print "down is true"
            if getMotorPositionCommand(motor_id) in range(390,410):
                print "done going down"
                up, down = True, False
                response = setMotorTargetPositionCommand(motor_id, 0)
                response2 = setMotorTargetPositionCommand(other_motor_id, 700)

def readyPosition():
    ''' Initializes positions of several robot motors '''
    response = setMotorTargetPositionCommand(8, 400)
    response = setMotorTargetPositionCommand(7, 600)
    response = setMotorTargetPositionCommand(3, 500)
    response = setMotorTargetPositionCommand(4, 500)
    response = setMotorTargetPositionCommand(1, 500)
    response = setMotorTargetPositionCommand(2, 500)

def ballet():
    ''' Makes the robot go into pointe form to show off if an object is nearby '''
    if getSensorValue(1) > 50:
        response = setMotorTargetPositionCommand(3, 600)  
        response = setMotorTargetPositionCommand(4, 400)
        response = setMotorTargetPositionCommand(8, 0)
        response = setMotorTargetPositionCommand(7, 1010)   
    else:
        response = setMotorTargetPositionCommand(3, 500)  
        response = setMotorTargetPositionCommand(4, 500)
        response = setMotorTargetPositionCommand(8, 300)
        response = setMotorTargetPositionCommand(7, 700) 

def walkSetup():
    ''' Puts the robot in a starting position before it walks '''
    response = setMotorTargetPositionCommand(1, 674)
    response = setMotorTargetPositionCommand(2, 674)
    response = setMotorTargetPositionCommand(7, 900)
    response = setMotorTargetPositionCommand(8, 100)

def walk():
    ''' Walking logic split into three steps '''
    response = setMotorTargetSpeed(1, 250)
    response = setMotorTargetSpeed(2, 250)
    response = setMotorTargetSpeed(3, 150)
    response = setMotorTargetSpeed(4, 150)
    
    stage = 1
      
    while stage == 1:
        print "Stage 1"
        response = setMotorTargetPositionCommand(3, 460)
        response = setMotorTargetPositionCommand(4, 350)
        rospy.sleep(.35)
        response = setMotorTargetPositionCommand(1, 350)
        response = setMotorTargetPositionCommand(2, 350)
        rospy.sleep(.35)
        response = setMotorTargetPositionCommand(3, 512)
        response = setMotorTargetPositionCommand(4, 512)
        stage = 2
        
    while stage == 2:
        print "Stage 2"
        rospy.sleep(.35)
        response = setMotorTargetPositionCommand(3, 664)
        response = setMotorTargetPositionCommand(4, 574)
        rospy.sleep(.35)    
        response = setMotorTargetPositionCommand(1, 694)
        response = setMotorTargetPositionCommand(2, 674)
        stage = 3
    
    while stage == 3:
        print "Stage 3"
        rospy.sleep(.35)
        response = setMotorTargetPositionCommand(3, 512)
        response = setMotorTargetPositionCommand(4, 512)
        stage = 1
        
def turnRight(count):
    ''' Turns the robot 90 degrees to the right '''   
    print count   
    if count <= 6:
        response = setMotorTargetPositionCommand(3, 512)
        response = setMotorTargetPositionCommand(4, 400)
        rospy.sleep(.5)
        response = setMotorTargetPositionCommand(1, 320)
        response = setMotorTargetPositionCommand(2, 350)
        rospy.sleep(.5)
        response = setMotorTargetPositionCommand(3, 512)
        response = setMotorTargetPositionCommand(4, 512)
        rospy.sleep(.5)
        response = setMotorTargetPositionCommand(1, 512)
        response = setMotorTargetPositionCommand(2, 512)
        rospy.sleep(.5)
        turnRight(count + 1)
        
def turnLeft(count):
    ''' Turns the robot 90 degrees to the left '''   
    print count   
    if count <= 7:
        response = setMotorTargetPositionCommand(3, 512)
        response = setMotorTargetPositionCommand(4, 400)
        rospy.sleep(.5)
        response = setMotorTargetPositionCommand(1, 704)
        response = setMotorTargetPositionCommand(2, 674)
        rospy.sleep(.5)
        response = setMotorTargetPositionCommand(3, 512)
        response = setMotorTargetPositionCommand(4, 512)
        rospy.sleep(.5)
        response = setMotorTargetPositionCommand(1, 512)
        response = setMotorTargetPositionCommand(2, 512)
        rospy.sleep(.5)
        turnLeft(count + 1)
        
def turnAround(count):
    ''' Turns the robot around 180 degrees '''   
    print count   
    if count <= 15:
        response = setMotorTargetPositionCommand(3, 512)
        response = setMotorTargetPositionCommand(4, 400)
        rospy.sleep(.5)
        response = setMotorTargetPositionCommand(1, 320)
        response = setMotorTargetPositionCommand(2, 350)
        rospy.sleep(.5)
        response = setMotorTargetPositionCommand(3, 512)
        response = setMotorTargetPositionCommand(4, 512)
        rospy.sleep(.5)
        response = setMotorTargetPositionCommand(1, 512)
        response = setMotorTargetPositionCommand(2, 512)
        rospy.sleep(.5)
        turnAround(count + 1)

def walkStraightHelper():
    ''' Helps the robot walk straight by pausing & reinitializing before taking sensor readings '''
    response = setMotorTargetSpeed(1, 250)
    response = setMotorTargetSpeed(2, 250)
    response = setMotorTargetSpeed(3, 150)
    response = setMotorTargetSpeed(4, 150)
    
    stage = 1
      
    while stage == 1:
        #left foot forward
        print "Stage 1"
        response = setMotorTargetPositionCommand(3, 460)
        response = setMotorTargetPositionCommand(4, 350)
        rospy.sleep(.35)
        response = setMotorTargetPositionCommand(1, 350)
        response = setMotorTargetPositionCommand(2, 350)
        rospy.sleep(.35)
        response = setMotorTargetPositionCommand(3, 512)
        response = setMotorTargetPositionCommand(4, 512)
        rospy.sleep(1)
        stage = 2
        
    while stage == 2:
        #right foot forward
        print "Stage 2"
        rospy.sleep(.35)
        response = setMotorTargetPositionCommand(3, 664)
        response = setMotorTargetPositionCommand(4, 574)
        rospy.sleep(.35)    
        response = setMotorTargetPositionCommand(1, 694)
        response = setMotorTargetPositionCommand(2, 674)
        rospy.sleep(.35)
        response = setMotorTargetPositionCommand(3, 512)
        response = setMotorTargetPositionCommand(4, 512)
        stage = 3
    
    while stage == 3: #reinitialize
        print "Stage 3"
        rospy.sleep(.35)
        walkSetup()
        stage = 1
        
def walkStraightRight():
    ''' Makes the robot walk straight along the wall by keeping it within a certain right sensor range'''
    if getSensorValue(2) < 400:
        turnRight(-1)
    elif getSensorValue(2) > 1600:
        turnLeft(0)
    else:
        walkStraightHelper()

def checkSensorPosition():
    response = setMotorTargetPositionCommand(7, 900)
    response = setMotorTargetPositionCommand(8, 100)
    response = setMotorTargetPositionCommand(3, 500)
    response = setMotorTargetPositionCommand(4, 500)
    response = setMotorTargetPositionCommand(1, 500)
    response = setMotorTargetPositionCommand(2, 500)
 
def walkStraightLeft():
    ''' Helps the robot walk straight by pausing & reinitializing before taking sensor readings '''
    response = setMotorTargetSpeed(1, 250)
    response = setMotorTargetSpeed(2, 250)
    response = setMotorTargetSpeed(3, 150)
    response = setMotorTargetSpeed(4, 150)
    
    stage = 1
      
    while stage == 1:
        #left foot forward
        print "Stage 1"
        response = setMotorTargetPositionCommand(3, 460)
        response = setMotorTargetPositionCommand(4, 350)
        rospy.sleep(.35)
        response = setMotorTargetPositionCommand(1, 350)
        response = setMotorTargetPositionCommand(2, 350)
        rospy.sleep(.35)
        response = setMotorTargetPositionCommand(3, 512)
        response = setMotorTargetPositionCommand(4, 512)
        stage = 2
        
    while stage == 2:
        #right foot forward
        print "Stage 2"
        rospy.sleep(.35)
        response = setMotorTargetPositionCommand(3, 664)
        response = setMotorTargetPositionCommand(4, 574)
        rospy.sleep(.35)    
        response = setMotorTargetPositionCommand(1, 694)
        response = setMotorTargetPositionCommand(2, 674)
        rospy.sleep(.35)
        response = setMotorTargetPositionCommand(3, 512)
        response = setMotorTargetPositionCommand(4, 512)
        stage = 3
    
    while stage == 3: #reinitialize
        print "Stage 3"
        rospy.sleep(.35)
        checkSensorPosition()
        print "The sensor value is: " + str(getSensorValue(5))
        if getSensorValue(5) < 5:
            turnLeft(2)
        elif getSensorValue(5) > 130:
            turnRight(1)
        stage = 1
        rospy.sleep(1)
        
        
        
def isBlocked():
    if getSensorValue(1) > 30:
        if getSensorValue(2) > 1350:
            if getSensorValue(5) > 120:
                print "I should turn around"
                turnAround(0)
            else:
                print "I should turn left"
                turnLeft(0)
        else:
            if getSensorValue(5) > 120:
                print "I should turn right"
                turnRight(0)
        
# Main function
if __name__ == "__main__":
    rospy.init_node('example_node', anonymous=True)
    rospy.loginfo("Starting Group X Control Node...")
    # initialize robot motor positions
    fxnToRun = ""
    readyPosition()
    walkSetup()
    # control loop running at 10hz
    r = rospy.Rate(10) # 10hz
    # read from command line
    if len(sys.argv) > 1:
        fxnToRun = sys.argv[1]
    keepGoing = True
    while not rospy.is_shutdown():
        # get sensor value
        port = 1
        sensor_reading = getSensorValue(port)
        rospy.loginfo("Sensor value at port %d: %f", port, sensor_reading)
        left_sensor_reading = getSensorValue(5)
        rospy.loginfo("Left Sensor value at port %d: %f", 5, left_sensor_reading)
        right_sensor_reading = getSensorValue(2)
        rospy.loginfo("Right Sensor value at port %d: %f", 2, right_sensor_reading)
        rospy.sleep(0.5)
        # make the robot disco
        if fxnToRun == "disco":
            disco()
        # make the robot do ballet
        if fxnToRun == "ballet":
            ballet()
        # make the robot walk
        if fxnToRun == "walk":
            walk()
        # make the robot turn right
        if fxnToRun =="turnRight":
            count = 0
            if keepGoing:
                turnRight(count)
                keepGoing = False
        # make the robot turn left
        if fxnToRun == "turnLeft":
            count = 0
            if keepGoing:
                turnLeft(count)
                keepGoing = False
        # make the robot turn around
        if fxnToRun == "turnAround":
            count = 0
            if keepGoing:
                turnAround(count)
                keepGoing = False
                
        # make the robot walk straight (right side)
        if fxnToRun == "walkStraightRight":
            walkStraightRight()
        
        # make the robot walk straight (left side)    
        if fxnToRun == "walkStraightLeft":
            walkStraightLeft()    
        
        # check if path is blocked; if so, turn
        if fxnToRun == "isBlocked":
            isBlocked()
            
        if fxnToRun == "walkStraightRight1":
            walkStraightRight1()
            
        # sleep to enforce loop rate
        r.sleep()

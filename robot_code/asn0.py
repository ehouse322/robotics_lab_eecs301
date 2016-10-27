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


# Main function
if __name__ == "__main__":
    rospy.init_node('example_node', anonymous=True)
    rospy.loginfo("Starting Group X Control Node...")
    # initialize robot motor positions
    fxnToRun = ""
    readyPosition()
    # control loop running at 10hz
    r = rospy.Rate(10) # 10hz
    # read from command line
    if len(sys.argv) > 1:
        if sys.argv[1] == "disco":
            fxnToRun = "disco"
        if sys.argv[1] == "ballet":
            fxnToRun = "ballet"
    while not rospy.is_shutdown():
        # get sensor value
        port = 1
        sensor_reading = getSensorValue(port)
        rospy.loginfo("Sensor value at port %d: %f", port, sensor_reading)
 
        # make the robot disco
        if fxnToRun == "disco":
            disco()
        # make the robot do ballet
        if fxnToRun == "ballet":
            ballet()
        
        # sleep to enforce loop rate
        r.sleep()

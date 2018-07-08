#! /usr/bin/env python 
import sys
import rospy
from turtlebot3_waffle_app.srv import *
def drive_to_target_client(goal_distance,goal_angle):
	rospy.wait_for_service('drivetotarget')
	try:
	 	drive_to_target=rospy.ServiceProxy('drivetotarget',DriveToTarget)
		respl=drive_to_target(goal_distance,goal_angle)
	except rospy.ServiceException,e:
		print "Service call failed:%s"%e
if __name__=="__main__":
    if len(sys.argv)==3:
	goal_distance=float(sys.argv[1])
	goal_angle=float(sys.argv[2])
    else:
	sys.exit(1)
    print "Drive to target  (%lf,%lf)"%(goal_distance,goal_angle)
    drive_to_target_client(goal_distance,goal_angle)	

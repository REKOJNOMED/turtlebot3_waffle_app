#! /usr/bin/env python 
import sys
import rospy
from turtlebot3_waffle_app.srv import *
def drive_to_target_client(goal_x,goal_y):
	rospy.wait_for_service('drivetotarget')
	try:
	 	drive_to_target=rospy.ServiceProxy('drivetotarget',DriveToTarget)
		respl=drive_to_target(goal_x,goal_y)
	except rospy.ServiceException,e:
		print "Service call failed:%s"%e
if __name__=="__main__":
    if len(sys.argv)==3:
	goal_x=float(sys.argv[1])
	goal_y=float(sys.argv[2])
    else:
	sys.exit(1)
    print "Drive to target  (%lf,%lf)"%(goal_x,goal_y)
    drive_to_target_client(goal_x,goal_y)	

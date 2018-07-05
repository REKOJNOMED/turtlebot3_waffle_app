#! /usr/bin/env python 
import sys
import rospy
from turtlebot3_waffle_app.srv import *
def drive_to_target_client(x,y,angle):
	rospy.wait_for_service('drivetotarget')
	try:
	 	drive_to_target=rospy.ServiceProxy('drivetotarget',DriveToTarget)
		respl=drive_to_target(x,y,angle)
	except rospy.ServiceException,e:
		print "Service call failed:%s"%e
if __name__=="__main__":
    if len(sys.argv)==4:
	x=float(sys.argv[1])
	y=float(sys.argv[2])
	angle=float(sys.argv[3])
    else:
	sys.exit(1)
    print "Drive to target  (%lf,%lf,%lf)"%(x,y,angle)
    drive_to_target_client(x,y,angle)	

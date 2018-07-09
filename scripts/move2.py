#! /usr/bin/env python
import rospy
from geometry_msgs.msg import Twist, Point, Quaternion
from math import radians
import tf
from rbx1_nav.transform_utils import quat_to_angle, normalize_angle
from turtlebot3_waffle_app.srv import *
from math import radians, copysign, sqrt, pow, pi
class MoveToTarget():
    def targetcallback(self,req):
	rate=100
	r=rospy.Rate(rate)

	#angular_tolerance=radians(rospy.get_param("~angular_tolerance",2))
	self.cmd_vel=rospy.Publisher('/cmd_vel', Twist, queue_size=1000)
	move_cmd=Twist()
	self.cmd_vel.publish(move_cmd)
	rospy.sleep(1.0)
	if req.goal_angle<0:
		move_cmd.angular.z=-radians(45)
	else:
		move_cmd.angular.z=radians(45)
	#count=int((abs(req.goal_angle)/radians(45))*rate+0.5)
	#for x in range(0,count):
                #self.cmd_vel.publish(move_cmd)
                #r.sleep()
	self.cmd_vel.publish(move_cmd)
	rospy.sleep((abs(req.goal_angle)/radians(45)))
	move_cmd=Twist()
	move_cmd.linear.x=0.1
	#count=int((abs(req.goal_distance)/0.4)*rate+0.5)
	#for x in range(0,count):
                #self.cmd_vel.publish(move_cmd)
                #r.sleep()
	self.cmd_vel.publish(move_cmd)
	rospy.sleep((abs(req.goal_distance)/0.1))
	#rospy.sleep(10)
	self.cmd_vel.publish(Twist())
	return DriveToTargetResponse(True)

    def __init__(self):
	rospy.init_node('drivetotarget_server',anonymous=False)
	rospy.on_shutdown(self.shutdown)
	s=rospy.Service('drivetotarget',DriveToTarget,self.targetcallback)
	print "Ready to drive to target"
        rospy.spin()


    def shutdown(self):

        rospy.loginfo("Stop ")
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)
 
	
	
if __name__=='__main__':
    MoveToTarget()
	
	

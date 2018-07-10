#! /usr/bin/env python
import rospy
from geometry_msgs.msg import Twist, Point, Quaternion
from math import radians
import tf
from rbx1_nav.transform_utils import quat_to_angle, normalize_angle
from turtlebot3_waffle_app.srv import *
from math import radians, copysign, sqrt, pow, pi,atan,sin,cos,acos
from sensor_msgs.msg import LaserScan
import edit_theta
import Odom
class MoveToTarget():
    def scancallback(self,scan):
	self.scan=scan
    def targetcallback(self,req):
	self.goal_x=req.goal_x
	self.goal_y=req.goal_y
	rate=100
	r=rospy.Rate(rate)

	rospy.Subscriber('scan', LaserScan,self.scancallback)

	#angular_tolerance=radians(rospy.get_param("~angular_tolerance",2))
	self.cmd_vel=rospy.Publisher('/cmd_vel', Twist, queue_size=1000)

	self.cmd_vel.publish(Twist())
	rospy.sleep(1.0)
	distance=sqrt(pow((req.goal_x - self.odom.x), 2) + 
                                pow((req.goal_y - self.odom.y), 2))
	rotate_speed=radians(45)
	linear_speed=0.1

	move_cmd = Twist()
        move_cmd.linear.x = linear_speed

        turn_cmd = Twist()
        turn_cmd.linear.x = 0
        turn_cmd.angular.z = rotate_speed 

	anti_turn_cmd = Twist()
        anti_turn_cmd.linear.x = 0
        anti_turn_cmd.angular.z = -rotate_speed 

	delta_distance=0.1
	while distance>1e-1:
		#print self.scan
		[x1,y1]=[sin(self.odom.rotation),cos(self.odom.rotation)]
		[x2,y2]=[self.goal_y-self.odom.y,self.goal_x-self.odom.x]
		cos_theta=(x1*x2+y1*y2)/(sqrt(pow(x1,2)+pow(y1,2))*sqrt(pow(x2,2)+pow(y2,2)))
		theta=acos(cos_theta)
		if x1*x2>0:
			goal_theta=theta
		else:
			goal_theta=-theta
		self.angle_range=edit_theta.edit_theta(goal_theta,self.scan.ranges)
		print 'Odom %lf %lf %lf'%(self.odom.x,self.odom.y,self.odom.rotation)
		print self.goal_theta
		print 'angle %lf'%self.angle_range
		if self.angle_range<0:
			self.cmd_vel.publish(anti_turn_cmd)
		else:
			self.cmd_vel.publish(turn_cmd)
		self.odom.rotation-=self.angle_range
		if self.odom.rotation>radians(180)
			self.odom.rotation-=radians(360)
		if self.odom.rotation<radians(-180)
			self.odom.rotation+=radians(360)
		rospy.sleep(abs(self.angle_range)/rotate_speed)
		self.cmd_vel.publish(move_cmd)
		rospy.sleep(delta_distance/linear_speed)
		self.odom.x+=delta_distance*sin(self.odom.rotation)
		self.odom.y+=delta_distance*cos(self.odom.rotation)
		distance=sqrt(pow((req.goal_x - self.odom.x), 2) + 
		                pow((req.goal_y - self.odom.y), 2))
		self.cmd_vel.publish(Twist())
		rospy.sleep(1)
		print 'distance:%lf'%distance

	rospy.loginfo("Stop ")
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)

	return DriveToTargetResponse(True)

    def __init__(self):
	rospy.init_node('drivetotarget_server',anonymous=False)
	rospy.on_shutdown(self.shutdown)
	self.odom=Odom.Odom()
	s=rospy.Service('drivetotarget',DriveToTarget,self.targetcallback)
	print "Ready to drive to target"
        rospy.spin()


    def shutdown(self):
	rospy.loginfo("Stop ")
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)
 
	
	
if __name__=='__main__':
    MoveToTarget()
	
	

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
	rate=20
	r=rospy.Rate(rate)
	self.targetpos_x=req.x
	self.targetpos_y=req.y
	self.target_angle=req.angle
	linear_speed=rospy.get_param("~linear_speed",0.2)
	angular_speed=rospy.get_param("~angular_speed",0.7)
	angular_tolerance=radians(rospy.get_param("~angular_tolerance",2))
	self.cmd_vel=rospy.Publisher('/cmd_vel', Twist, queue_size=5)
	self.base_frame = rospy.get_param('~base_frame', '/base_link')
	self.odom_frame = rospy.get_param('~odom_frame', '/odom')
	self.tf_listener = tf.TransformListener()
	rospy.sleep(2)
	self.odom_frame = '/odom'
	try:
            self.tf_listener.waitForTransform(self.odom_frame, '/base_footprint', rospy.Time(), rospy.Duration(1.0))
            self.base_frame = '/base_footprint'
        except (tf.Exception, tf.ConnectivityException, tf.LookupException):
            try:
                self.tf_listener.waitForTransform(self.odom_frame, '/base_link', rospy.Time(), rospy.Duration(1.0))
                self.base_frame = '/base_link'
            except (tf.Exception, tf.ConnectivityException, tf.LookupException):
                rospy.loginfo("Cannot find transform between /odom and /base_link or /base_footprint")
                rospy.signal_shutdown("tf Exception")  

	move_cmd=Twist()
	self.cmd_vel.publish(move_cmd)
	rospy.sleep(1.0)
	move_cmd.angular.z=angular_speed
	(position,rotation)=self.get_odom()
	last_angle=rotation
	turn_angle=0
	while abs(turn_angle+angular_tolerance)<abs(self.target_angle) and not rospy.is_shutdown():
		self.cmd_vel.publish(move_cmd)
		r.sleep()
		(position,rotation)=self.get_odom()
		delta_angle=normalize_angle(rotation - last_angle)
		turn_angle+=delta_angle
		last_angle=rotation
	position = Point()
	move_cmd=Twist()
	move_cmd.linear.x=linear_speed
	(position,rotation)=self.get_odom()
	x_start=position.x
	y_start=position.y
	distance=0;
	goal_distance=sqrt(pow((self.targetpos_x - x_start), 2) + 
                                pow((self.targetpos_y - y_start), 2))
	while distance<goal_distance and not rospy.is_shutdown():
		print "%lf %lf %lf %lf"%(position.x,position.y,self.targetpos_x,self.targetpos_y)
		self.cmd_vel.publish(move_cmd)
		r.sleep()	
		(position,rotation)=self.get_odom()
		distance=sqrt(pow((position.x - x_start), 2) + 
                                pow((position.y - y_start), 2))

	self.cmd_vel.publish(Twist())
	return DriveToTargetResponse(True)
    def __init__(self):
	rospy.init_node('drivetotarget_server',anonymous=False)
	rospy.on_shutdown(self.shutdown)
	s=rospy.Service('drivetotarget',DriveToTarget,self.targetcallback)
	print "Ready to drive to target"
        rospy.spin()
    def get_odom(self):

        try:
            (trans, rot)  = self.tf_listener.lookupTransform(self.odom_frame, self.base_frame, rospy.Time(0))
        except (tf.Exception, tf.ConnectivityException, tf.LookupException):
            rospy.loginfo("TF Exception")
            return

        return (Point(*trans), quat_to_angle(Quaternion(*rot)))

    def shutdown(self):

        rospy.loginfo("Stop ")
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)
 
	
	
if __name__=='__main__':
    MoveToTarget()
	
	

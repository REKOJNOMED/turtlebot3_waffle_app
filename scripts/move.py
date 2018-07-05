#!/usr/bin/env python



import rospy
from geometry_msgs.msg import Twist
from math import radians

class DrawASquare():
    def __init__(self):

        rospy.init_node('drawasquare', anonymous=False)

     
        rospy.on_shutdown(self.shutdown)
        
        self.cmd_vel = rospy.Publisher('cmd_vel', Twist, queue_size=10)

        r = rospy.Rate(5);

        move_cmd = Twist()
        move_cmd.linear.x = -0.2
        turn_cmd = Twist()
        turn_cmd.linear.x = 0
        turn_cmd.angular.z = radians(45); #45 deg/s in radians/s

	count = 0
        while not rospy.is_shutdown():

	    rospy.loginfo("Going Straight")
            for x in range(0,10):
                self.cmd_vel.publish(move_cmd)
                r.sleep()
	    rospy.loginfo("Turning")
            for x in range(0,10):
                self.cmd_vel.publish(turn_cmd)
                r.sleep()            
	    count = count + 1
	    if(count == 4): 
                count = 0
	    if(count == 0): 
                rospy.loginfo("TurtleBot should be close to the original starting position (but it's probably way off)")
        
    def shutdown(self):

        rospy.loginfo("Stop Drawing Squares")
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)
 
if __name__ == '__main__':
    try:
        DrawASquare()
    except:
        rospy.loginfo("node terminated.")

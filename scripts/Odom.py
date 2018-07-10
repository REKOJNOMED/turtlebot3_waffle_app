#! /usr/bin/env python 
import sys
import rospy
class Odom():
	def __init__(self):
		self.x=0
		self.y=0
		self.rotation=0
	def update(self,x,y,rotation):
		self.x=x
		self.y=y
		self.rotation=rotation

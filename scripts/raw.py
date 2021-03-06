#!/usr/bin/env python

import rospy

from tf.transformations import euler_from_quaternion
from sensor_msgs.msg import Imu
from std_msgs.msg import Float64

class Y3SpaceRaw:
	PI = 3.14159265359

	def __init__(self):
		self.rollPub = rospy.Publisher('~/raw/roll', Float64, queue_size=1)
		self.pitchPub = rospy.Publisher('~/raw/pitch', Float64, queue_size=1)
		self.yawPub = rospy.Publisher('~/raw/yaw', Float64, queue_size=1)

		self.degrees = True # TODO: change to rosparam
		self.verbose = True # TODO: change to rosparam

	def callback(self, data):
		quat = [data.orientation.x,
				data.orientation.y,
				data.orientation.z,
				data.orientation.w]

		(roll, pitch, yaw) = euler_from_quaternion(quat)
		
		if (self.degrees):
			roll = (roll / self.PI) * 180
			pitch = (pitch / self.PI) * 180
			yaw = (yaw / self.PI) * 180

		self.rollPub.publish(roll)
		self.pitchPub.publish(pitch)
		self.yawPub.publish(yaw)

		if (self.verbose):
			rospy.loginfo('\n\tYaw: {}\n'.format(yaw) +
						  '\tPitch: {}\n'.format(pitch) +
						  '\tRoll: {}\n'.format(roll) +
				  		  '-------------------------------')


if __name__ == '__main__':
	rospy.init_node('Y3SpaceRaw')
	raw = Y3SpaceRaw()

	sub = rospy.Subscriber('/imu/filtered', Imu, raw.callback)
	rospy.spin()
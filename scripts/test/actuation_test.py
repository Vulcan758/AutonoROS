#!/usr/bin/env python3 

import rospy
from geometry_msgs.msg import Twist

forward = Twist()
forward.linear.x = 0.3

stop = Twist()
stop.linear.x = 0
stop.linear.y = 0
stop.linear.z = 0
stop.angular.x = 0
stop.angular.y = 0
stop.angular.z = 0

rospy.init_node("actuation_test")
rate = rospy.Rate(7)

cmd_vel = rospy.Publisher("cmd_vel", Twist, queue_size=10)

for i in range(20):
    cmd_vel.publish(forward)
    print("going forward")
    rate.sleep()
    cmd_vel.publish(stop)
    #rate.sleep()
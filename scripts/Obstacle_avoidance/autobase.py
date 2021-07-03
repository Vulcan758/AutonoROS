#! /usr/bin/env python3 

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


def laser_callback(msg):
    front = msg.ranges[0]
    if front < 0.5:
        cmd_vel.publish(turn)
        rate_turn.sleep()
        print("changing course")
    else:
        cmd_vel.publish(forward)
        print("going forward")
        rate_forward.sleep()


rospy.init_node("autobase")

rate_forward = rospy.Rate(7)

rate_turn = rospy.Rate(3)

forward = Twist()
forward.linear.x = 0.3

turn = Twist()
turn.angular.z = 0.3

stop = Twist()
stop.linear.x = 0
stop.linear.y = 0
stop.linear.z = 0
stop.angular.x = 0
stop.angular.y = 0
stop.angular.z = 0


scan = rospy.Subscriber("/scan", LaserScan, laser_callback)
cmd_vel = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

#0th/360th is front facing, 90th is left, 180th is back, 270th is right.



rospy.spin()
cmd_vel.publish(stop)

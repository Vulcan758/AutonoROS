#! /usr/bin/env python3 

import rospy
from sensor_msgs.msg import LaserScan

rospy.init_node("scan_test")

def callback(msg):
    tlq = msg.ranges[330]
    trq = msg.ranges[30]
    str8 = msg.ranges[0]
    last_state = None
    

sub = rospy.Subscriber("/scan", LaserScan, callback)

rospy.spin()

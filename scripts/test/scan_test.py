#! /usr/bin/env python3 

import rospy
from sensor_msgs.msg import LaserScan

rospy.init_node("scan_test")

def callback(msg):
    print("0th " + str(msg.ranges[0]))
    print("360 " + str(msg.ranges[359]))
    print("30 "+ str(msg.ranges[29]))
    print("60 "+ str(msg.ranges[59]))
    print("330 "+ str(msg.ranges[329]))
    print("300 "+ str(msg.ranges[299]))
    

sub = rospy.Subscriber("/scan", LaserScan, callback)

rospy.spin()

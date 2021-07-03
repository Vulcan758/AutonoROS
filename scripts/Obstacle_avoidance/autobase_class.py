#!/usr/bin/env python3 

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class Autobase():
    def __init__(self):
        rospy.init_node("autobase")

        self.rate_forward = rospy.Rate(7)

        self.rate_turn = rospy.Rate(5)

        self.forward = Twist()
        self.forward.linear.x = 0.3

        self.turn = Twist()
        self.turn.angular.z = 0.3

        self.stop = Twist()

        self.scan = rospy.Subscriber("/scan", LaserScan, self.callback)
        self.cmd_vel = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

    def callback(self, msg):
        front = msg.ranges[0]
        if front < 0.5:
            self.cmd_vel.publish(self.turn)
            self.rate_turn.sleep()
            print("changing course")
        else:
            self.cmd_vel.publish(self.forward)
            print("going forward")
            self.rate_forward.sleep()

if __name__ == "__main__":
    autono = Autobase()
    rospy.spin()
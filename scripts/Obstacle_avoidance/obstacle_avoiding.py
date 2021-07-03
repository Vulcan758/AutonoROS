#!/usr/bin/env python3 
from numpy.core.arrayprint import LongComplexFormat
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from numpy import inf

class ObstacleAvoiding():
    def __init__(self, distance_threshold=0.4):
        rospy.init_node("ObstacleAvoider")

        self.dt = distance_threshold

        self.rate_forward = rospy.Rate(7)

        self.rate_turn = rospy.Rate(5)

        self.rate_hard = rospy.Rate(1)

        self.forward = Twist()
        self.forward.linear.x = 0.2

        self.backward = Twist()
        self.backward.linear.x = -0.5

        self.turn_left = Twist()
        self.turn_left.angular.z = 0.3

        self.turn_right = Twist()
        self.turn_right.angular.z = -0.3

        self.stop = Twist()

        self.scan = rospy.Subscriber("/scan", LaserScan, self.callback)
        self.cmd_vel = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    
    def callback(self, msg):
        tlq = msg.ranges[315]
        trq = msg.ranges[45]
        llq = msg.ranges[75]
        lrq = msg.ranges[285]
        str8 = msg.ranges[0]
        last_state = None
        
        if (str8 < self.dt or tlq < self.dt or llq < self.dt) and (trq < self.dt or lrq < self.dt):
            if last_state == None:
                last_state = self.turn_right
            self.locomotion(self.backward, self.rate_hard)
            print('going back')
            self.cmd_vel.publish(self.stop)
            self.locomotion(last_state, self.rate_hard)
            if last_state == self.turn_right:
                dir = "right"
            elif last_state == self.turn_left:
                dir = "left"
            print(f"turning hard {dir}")
        
        elif str8 < self.dt or tlq < self.dt or llq < self.dt:
            self.locomotion(self.turn_right, self.rate_turn)
            print("turning right")
            last_state = self.turn_right   

        elif trq < self.dt or lrq < self.dt:
            self.locomotion(self.turn_left, self.rate_turn)
            print("turning left")
            last_state = self.turn_left

        else:
            self.move(self.forward, self.rate_forward)
            print("going forward")

    def locomotion(self, direction, rate):
        try:
            self.cmd_vel.publish(self.stop)
            self.rate_turn.sleep()
            self.scan.unregister()
            self.move(direction, rate)
            self.__init__()
        except AssertionError:
            self.cmd_vel.publish(self.stop)
            self.rate_turn.sleep()
            self.move(direction, rate)
            self.__init__()

    def stop_(self):
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)

    def move(self, direction, rate):
        self.cmd_vel.publish(direction)
        rate.sleep()


if __name__ == "__main__":
    try:
        autono = ObstacleAvoiding(0.4) 
        rospy.spin()
    finally:
        autono.stop_()
        print("Stopping bot")
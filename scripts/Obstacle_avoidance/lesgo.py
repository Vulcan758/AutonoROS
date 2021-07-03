#!/usr/bin/env python3 

from numpy.core.arrayprint import LongComplexFormat
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from numpy import inf

class Lestgo():
    def __init__(self, distance_threshold):
        rospy.init_node("autobase")

        self.dt = distance_threshold

        self.rate_forward = rospy.Rate(7)

        self.rate_turn = rospy.Rate(5)

        self.rate_hard = rospy.Rate(2.5)

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
        tlq = msg.ranges[330]
        trq = msg.ranges[30]
        llq = msg.ranges[60]
        lrq = msg.ranges[300]
        str8 = msg.ranges[0]
        last_state = None
        
        if (str8 < self.dt or tlq < self.dt or llq < self.dt) and (trq < self.dt or lrq < self.dt):
            self.cmd_vel.publish(self.stop)
            self.rate_forward.sleep()
            self.scan.unregister()          
            if last_state == None:
                last_state = self.turn_right
            self.cmd_vel.publish(self.backward)
            self.rate_hard.sleep()
            print('going back')
            self.cmd_vel.publish(self.stop)
            self.cmd_vel.publish(last_state)
            self.rate_turn.sleep()
            if last_state == self.turn_right:
                dir = "right"
            else:
                dir = "left"
            print(f"turning hard {dir}")
            self.__init__()

        
        elif str8 < self.dt or tlq < self.dt or llq < self.dt:
            self.cmd_vel.publish(self.turn_right)
            self.rate_turn.sleep()
            print("turning right")
            last_state = self.turn_right        

        elif trq < self.dt or lrq < self.dt:
            self.cmd_vel.publish(self.turn_left)
            self.rate_turn.sleep()
            print("turning left")
            last_state = self.turn_left

        else:
            self.cmd_vel.publish(self.forward)
            self.rate_forward.sleep()
            print("going forward")

'''
    def average(self, lst):
        return sum(lst) / len(lst)

    def inf_filter(self, lst):
        new_lst = [3.6 if x==inf else x for x in lst]
        return new_lst

    def list_maker(self, lst, low, up):
        new_lst = []
        for i in range(low, up):
            element = lst[i]
            new_lst.append(element)
        
        return new_lst
'''

if __name__ == "__main__":
    autono = Lestgo(0.4) 
    rospy.spin()
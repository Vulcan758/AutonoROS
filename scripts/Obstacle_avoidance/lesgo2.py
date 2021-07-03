#!/usr/bin/env python3 

from numpy.core.arrayprint import LongComplexFormat
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from numpy import inf

class Lestgo():
    def __init__(self, distance_threshold=0.4):
        rospy.init_node("LESSGOO")

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
        tlq = msg.ranges[330]
        trq = msg.ranges[30]
        llq = msg.ranges[45]
        lrq = msg.ranges[315]
        str8 = msg.ranges[0]
        last_state = None
        
        if (str8 < self.dt or tlq < self.dt or llq < self.dt) and (trq < self.dt or lrq < self.dt):
            self.wait()          
            if last_state == None:
                last_state = self.turn_right
            self.move(self.backward, self.rate_hard)
            #self.cmd_vel.publish(self.backward)
            #self.rate_hard.sleep()
            print('going back')
            self.cmd_vel.publish(self.stop)
            self.move(last_state, self.rate_hard)
            #self.cmd_vel.publish(last_state)
            #self.rate_hard.sleep()
            if last_state == self.turn_right:
                dir = "right"
            elif last_state == self.turn_left:
                dir = "left"
            print(f"turning hard {dir}")
            self.__init__()

        
        elif str8 < self.dt or tlq < self.dt or llq < self.dt:
            self.wait()
            self.move(self.turn_right, self.rate_turn)
            #self.cmd_vel.publish(self.turn_right)
            #self.rate_turn.sleep()
            print("turning right")
            last_state = self.turn_right   
            self.__init__()

        elif trq < self.dt or lrq < self.dt:
            self.wait()
            self.move(self.turn_left, self.rate_turn)
            #self.cmd_vel.publish(self.turn_left)
            #self.rate_turn.sleep()
            print("turning left")
            last_state = self.turn_left
            self.__init__()
        else:
            self.move(self.forward, self.rate_forward)
            #self.cmd_vel.publish(self.forward)
            #self.rate_forward.sleep()
            print("going forward")

    def wait(self):
        self.cmd_vel.publish(self.stop)
        self.rate_turn.sleep()
        self.scan.unregister()

    def stop_(self):
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)

    def move(self, direction, rate):
        self.cmd_vel.publish(direction)
        rate.sleep()



#NOTE: I THINK YOU CAN MAKE THE CODE EVEN MORE EFFICIENT BY PUTTING THE MOVE METHOD
#INSIDE THE WAIT METHOD AND THEN CALLING THE INIT METHOD INSIDE THE WAIT METHOD.

if __name__ == "__main__":
    try:
        autono = Lestgo(0.4) 
        rospy.spin()
    finally:
        autono.stop_()
        print("Stopping bot")
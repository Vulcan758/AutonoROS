# AutonoROS

This is my first ROS project. It will run a script where I tell a robot (TurtleBot3 in my case) to move autonomously around a space while avoiding obstacles. My goal is to make it so that I can select a location in a map and make it move there autonomously while avoiding obstacles. I am aware that this is already been made but I would like to make one myself so that I can learn ROS. 

July 3rd 2021: As of today, I finished building the script a few days ago that makes TurtleBot3 run move where ever while avoiding collisions. I am going to begin trying to make a script that allows me to select a coordinate and make the robot go there, later implementing the obstacle avoiding feature. I think I might have to do some research on more sensor data and action servers. If you want to use the current obstacle avoiding script, you can run the following commands

<code> $ roscore </code>
<br>
<code> $ roslaunch turtlebot4_gazebo turtlebot3_house.launch </code>
<br>
<code> $ rosrun AutonoROS obstacle_avoiding.py </code>
<br>

You need to have TurtleBot3 installed if you wanna run the simulation but you can also run the script as long as the robot you have simulated is subscribed to the /cmd_vel topic and publishes to the /scan topic. Hopefully I'm not wrong about all that.


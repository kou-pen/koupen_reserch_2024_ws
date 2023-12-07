import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from std_msgs.msg import Int16MultiArray, Float32MultiArray

import numpy as np

from module.UsbCan import *
from module.JoyCalcTools import *

class CalcMotor(Node):
    node_name = "calc_motor"
    
    joy_sub_topic = "joy"
    max_speed_sub_topic = "speed" #m/s
    
    motor_command_pub_topic = "motor_command" #-10000~10000
    
    CONTROLLER = 0 # 0=Portable-PC 1=F310
    
    speed = None
    
    def __init__(self):
        super().__init__(self.node_name)
        self.get_logger().info("Start init")
        
        self.get_logger().info("Start applying")
        self.joy_sub = self.create_subscription(Joy, self.joy_sub_topic, self.joy_callback, 10)
        self.max_speed_sub = self.create_subscription(Float32MultiArray, self.max_speed_sub_topic, self.max_speed_callback, 10)
        
        self.motor_command_pub = self.create_publisher(Int16MultiArray, self.motor_command_pub_topic, 10)
        
        self.joy_calc_tool = JoyCalcTools(0)
        return
    
    def joy_callback(self, data):
        self.calc_motor(data)
        return
    
    def max_speed_callback(self, data):
        self.speed = data.data[0]
        return
        
    def calc_motor(self, data):
        joy_raw_data = data.data
        joy_data = self.joy_calc_tool.recalculate_joy(joy_raw_data)
        
        
        return
    
    
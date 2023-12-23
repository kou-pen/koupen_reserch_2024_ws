import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from std_msgs.msg import Int16MultiArray

import time

from module.JoyCalcTools import JoyCalcTools
from enum_conf import ControllerType
from Wheels import *



class JoyCommander(Node):
    node_name = "joy_commander"
    
    joy_linux_sub_topic = "joy"
    
    max_meter_per_sec = 0.1
    CONTROLLER_MODE = ControllerType.F310.value
    
    def __init__(self):
        super().__init__(self.node_name)
        
        self.get_logger().info("Start init")
        
        self.joy_sub = self.create_subscription(Joy, self.joy_linux_sub_topic, self.sub_joy_callback, 10)
        
        self.joy_tools = JoyCalcTools(self.CONTROLLER_MODE)
        
        gain_dict_list = [ #TODO: ゲイン調整
            {'p_gain': 0.005, 'i_gain': 0.000, 'd_gain': 0.000},
            {'p_gain': 0.005, 'i_gain': 0.000, 'd_gain': 0.000},
            {'p_gain': 0.005, 'i_gain': 0.000, 'd_gain': 0.000}
        ]
        
        self.three_omni = Omni_3_Wheels(wheel_radius_meter=0.05 ,robot_radius_meter=0.3, gain_dict=gain_dict_list)
        return
    
    def sub_joy_callback(self, data):
        joy_data = [0] * 8
        joy_data = self.joy_tools.recalculate_joy(data)
        x = joy_data[0] * (self.max_meter_per_sec / 128)
        y = joy_data[1] * (self.max_meter_per_sec / 128)
        r = joy_data[2] * (self.max_meter_per_sec / 128 )
        # print(joy_data)
        self.three_omni.calc_and_send_motor_power(x=x, y=y, r=r) # command
        print("joy", x, y, r)
        
        
    
def main(args=None):
    rclpy.init(args=args)
    rosmain = JoyCommander()
    try:
        rclpy.spin(rosmain)
    except KeyboardInterrupt:
        rosmain.destroy_node()

if __name__ == '__main__':
    main()
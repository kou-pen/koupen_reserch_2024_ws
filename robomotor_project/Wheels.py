from enum_conf import *
from module.UsbCan import *
from module.RobomusTools import *
import numpy as np
import math
import itertools
import time

class Wheels:
    def __init__(self, type_of_wheel: int, num_of_wheel: int, gain_dict) -> None:
        self.wheel_mat = None
        
        self._type_of_wheel = type_of_wheel
        self._num_of_wheel = num_of_wheel
        
        self.__wheels_object = [] * self._num_of_wheel
        self.__feedback_object = [] * self._num_of_wheel
        self.__pid_gain_dict = gain_dict
        print("I am type " + str(type_of_wheel))
        return
    
    def genelate_wheel(self):
        for i in range(self._num_of_wheel):
            self.__wheels_object.append(Wheel(i, 0x200, 1000000)) #TODO: 別IDでも対応できるようにする
            # self.__feedback_object.append(FeedBack(**(self.__pid_gain_dict[i])))
        return
    
    def calc_and_send_motor_power(self, x, y, r):
        result_mat = self.wheel_mat * np.matrix([[x],[y],[r]])
        result_2d_list = result_mat.tolist()
        fixed_list = list(itertools.chain.from_iterable(result_2d_list)) # tire 1, 2, 3, (4)
        
        # print(fixed_list)
        converted_to_rpm_list = list(map(rad_per_sec_2_rpm, fixed_list))
        pid_proccessed_list = [] * self._num_of_wheel
        print(converted_to_rpm_list)
        
        # for i in range(self._num_of_wheel):
        #     pid_proccessed_list[i] = (self.__feedback_object[i].pid_controll(converted_to_rpm_list[i], None)) #TODO: CANから取得するコード書け
            
                
        recalcued_to_robomas_command_list = list(map(lambda rpm: rpm_2_robomas_command(rpm), converted_to_rpm_list)) #TODO: lambda式を修正
        # recalcued_to_robomas_command_list = list(map(lambda rps: rpm_2_robomas_command(rad_per_sec_2_rpm(rps)), converted_to_rpm_list)) #TODO: lambda式を修正
        print(recalcued_to_robomas_command_list)
        
        # print(recalcued_to_robomas_command_list)
        
        for i in range(self._num_of_wheel):
            self.__wheels_object[i].split_and_memory_can_command(int(recalcued_to_robomas_command_list[i]))
        self.__wheels_object[-1].send_can_command()
        
    # def 


class Omni_3_Wheels(Wheels):
    def __init__(self, wheel_radius_meter: float, robot_radius_meter: float, gain_dict):
        super().__init__(type_of_wheel= WheelType.OMNI_3, num_of_wheel= 3, gain_dict=gain_dict)
        super().genelate_wheel()
        mat1 = np.matrix([  [-math.sin(math.radians(30)), math.cos(math.radians(30)), robot_radius_meter],
                            [-math.sin(math.radians(30 + 120)), math.cos(math.radians(30 + 120)), robot_radius_meter],
                            [-math.sin(math.radians(30 + 120 + 120)), math.cos(math.radians(30 + 120 + 120)), robot_radius_meter]])
        mat2 = np.matrix([[math.cos(30), 0, 0],
                          [0, math.cos(30), 0],
                          [0, 0, 1]])
        
        self.wheel_mat = (1 / wheel_radius_meter) * mat1 * mat2
        return


class Omni_4_Wheels(Wheels):
    def __init__(self, wheel_radius_meter: float, robot_radius_meter: float):
        super().__init__(type_of_wheel= WheelType.OMNI_4, num_of_wheel= 4)
        super().genelate_wheel()
        mat1 = np.matrix([  [-math.sin(math.radians(45)), math.cos(math.radians(45)), robot_radius_meter],
                            [-math.sin(math.radians(45 + 90)), math.cos(math.radians(45 + 90)), robot_radius_meter],
                            [-math.sin(math.radians(45 + 90 + 90)), math.cos(math.radians(45 + 90 + 90)), robot_radius_meter],
                            [-math.sin(math.radians(45 + 90 + 90 + 90)), math.cos(math.radians(45 + 90 + 90 + 90)), robot_radius_meter]])
        mat2 = np.matrix([[math.cos(45), 0, 0],
                          [0, math.cos(45), 0],
                          [0, 0, 1]])
        
        self.wheel_mat = (1 / wheel_radius_meter) * mat1 * mat2
        return 

class Mechanum_Wheels(Wheels):
    pass

class Wheel:
    command_memory_array = [0] * 8
    def __init__(self, motor_id: int, can_id: int, bitrate: int) -> None:
        self.__robomotor_id = motor_id
        self.__can_id = can_id
        self.__bitrate = bitrate
        
        self.usb_can = UsbCan(bitrate=self.__bitrate, buffer=100000)
        self.usb_can.open()
        self.can_m = CanMessage()
        print("I am wheel No " + str(motor_id))
        return
    
    def split_and_memory_can_command(self, data):
        data_h, data_l = split_highlow_bit(data)
        self.command_memory_array[self.__robomotor_id * 2] = data_h
        self.command_memory_array[self.__robomotor_id * 2 + 1] = data_l
    
    def send_can_command(self):
        print(self.command_memory_array)
        self.usb_can.send(
            self.can_m.msg_return(
                can_id=self.__can_id,
                is_extended=False,
                data_array=self.command_memory_array)
            )
        
    
class FeedBack:
    def __init__(self, p_gain: float, i_gain: float, d_gain: float) -> None:
        self.__p_gain = p_gain
        self.__i_gain = i_gain
        self.__d_gain = d_gain
        
        self.__thistime_diff_rpm = 0.0
        self.__error_sum = 0.0
        self.__error_diff = 0.0
        self.__result_rpm = 0.0
        
        self.__lasttime_error_sum = 0.0
        self.__lasttime_result_rpm = 0.0
    
    def pid_controll(self,target_rpm: float, feedback_rpm: float):
        self.__thistime_diff_rpm = target_rpm - feedback_rpm
        self.__error_sum += (self.__thistime_diff_rpm) * 0.001
        self.__error_diff = self.__lasttime_error_sum - self.__error_sum
        self.__result_rpm = self.__lasttime_result_rpm + (self.__p_gain * self.__thistime_diff_rpm) + (self.__i_gain * self.__error_sum) + (self.__d_gain * self.__error_diff)
        
        self.__lasttime_error_sum = self.__error_sum
        self.__lasttime_result_rpm = self.__result_rpm
        
        return self.__result_rpm
    
    def accelerate_controll(self):
        pass
    
    
def test():
    gain_dict_list = [
        {'p_gain': 0.0, 'i_gain': 0.0, 'd_gain': 0.0},
        {'p_gain': 0.0, 'i_gain': 0.0, 'd_gain': 0.0},
        {'p_gain': 0.0, 'i_gain': 0.0, 'd_gain': 0.0}
    ]
    three_omni = Omni_3_Wheels(wheel_radius_meter=0.01 ,robot_radius_meter=0.5, gain_dict=gain_dict_list)
    three_omni.calc_and_send_motor_power(x=0, y=0, r=1 * 0.01) # command
        
    
if __name__ == '__main__':
    test()
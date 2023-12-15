from enum_conf import *
from module.UsbCan import *
from module.RobomusTools import *
import numpy as np
import math
import itertools


class Wheels:
    def __init__(self, type_of_wheel: int, num_of_wheel: int) -> None:
        self.wheel_mat = None
        
        self._type_of_wheel = type_of_wheel
        self._num_of_wheel = num_of_wheel
        
        self.__wheels_object = [] * self._num_of_wheel
        print("I am type " + str(type_of_wheel))
        return
    
    def genelate_wheel(self):
        for i in range(self._num_of_wheel):
            self.__wheels_object.append(Wheel(i, 0x200, 1000000))
        return
    
    def calc_motor_power(self, x, y, r):
        return_mat = self.wheel_mat * np.matrix([[x],[y],[r]])
        return_list = return_mat.tolist()
        fixed_list = list(itertools.chain.from_iterable(return_list)) # tire 1, 2, 3, (4)
        print(fixed_list)
        
        for i in range(self._num_of_wheel):
            self.__wheels_object[i].calc_can_command(int(fixed_list[i]))
        self.__wheels_object[-1].send_can_command()
        
    # def 


class Omni_3_Wheels(Wheels):
    def __init__(self, wheel_radius_meter: float, robot_radius_meter: float):
        super().__init__(type_of_wheel= WheelType.OMNI_3, num_of_wheel= 3)
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
        
        # self.usb_can = UsbCan(bitrate=self.__bitrate, buffer=10000000)
        # self.usb_can.open()
        print("I am wheel No " + str(motor_id))
        return
    
    def calc_can_command(self, data):
        data_h, data_l = split_highlow_bit(data)
        self.command_memory_array[self.__robomotor_id * 2] = data_h
        self.command_memory_array[self.__robomotor_id * 2 + 1] = data_l
    
    def send_can_command(self):
        print(self.command_memory_array)
        # self.usb_can.send(
        #     CanMessage(
        #         can_id=self.__can_id,
        #         is_extended=False,
        #         data_array=self.command_memory_array)
        #     )
        
    
class FeedBack:
    def __init__(self, p_gain: float, i_gain: float, d_gain: float) -> None:
        pass
    
    def pid_controll(self):
        pass
    
    def accelerate_controll(self):
        pass
    
    
def test():
    three_omni = Omni_3_Wheels(wheel_radius_meter=0.01, robot_radius_meter=0.5)
    three_omni.calc_motor_power(0, 0, 1)
    
if __name__ == '__main__':
    test()
from enum_conf import *
from module.UsbCan import *
import numpy as np
import math
import itertools


class Wheels:
    def __init__(self, type_of_wheel: int, num_of_wheel: int) -> None:
        self.wheel_mat = None
        
        self._type_of_wheel = type_of_wheel
        self._num_of_wheel = num_of_wheel
        
        self.__wheels_object = [] * self._num_of_wheel
        return
    
    def genelate_wheel(self):
        for i in range(self._num_of_wheel):
            self.__wheels_object[i] = Wheel(hex(i))
        return
    
    def calc_motor_power(self, x, y, r):
        if self.wheel_mat == None:
            return
        return_mat = self.wheel_mat * np.matrix([[x],[y],[r]])
        return_list = return_mat.tolist()
        fixed_list = list(itertools.chain.from_iterable(return_list)) # tire 1, 2, 3, (4)
        for i in range(self._num_of_wheel):
            # self.__wheels_object[i]
            return
        


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
    def __init__(self, robomotor_id: int, bitrate: int) -> None:
        self.__robomotor_id = robomotor_id
        self.__bitrate = bitrate
        
        self.usb_can = UsbCan(bitrate=self.__bitrate, buffer=10000000)
        self.usb_can.open()
        return
    
    def send_can_command(self,data_array):
        self.usb_can.send(
            CanMessage(
                can_id=self.__robomotor_id,
                is_extended=False,
                data_array=data_array)
            )
        
    
class FeedBack:
    def __init__(self, p_gain: float, i_gain: float, d_gain: float) -> None:
        pass
    
    def pid_controll(self):
        pass
    
    def accelerate_controll(self):
        pass
    
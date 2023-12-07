from enum_conf import *
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
            self.__wheels_object[i] = Wheel()
        return
    
    def calc_motor_power(self, x, y, r):
        if self.wheel_mat == None:
            return
        return_mat = self.wheel_mat * np.matrix([[x],[y],[r]])
        return_list = return_mat.tolist()
        list(itertools.chain.from_iterable(return_list))
        for i in range(self._num_of_wheel):
            self.__wheels_object[i]


class Omni_3_Wheels(Wheels):
    def __init__(self, wheel_radius_meter: float, robot_radius_meter: float):
        super().__init__(type_of_wheel= WheelType.OMNI_3, num_of_wheel= 3)
        super().genelate_wheel()
        mat1 = np.matrix([  [-math.sin(math.radians(45)), math.cos(math.radians(45)), robot_radius_meter],
                            [-math.sin(math.radians(45 + 120)), math.cos(math.radians(45 + 120)), robot_radius_meter],
                            [-math.sin(math.radians(45 + 120 + 120)), math.cos(math.radians(45 + 120 + 120)), robot_radius_meter]])
        mat2 = np.matrix([[math.cos(45), 0, 0],
                          [0, math.cos(45), 0],
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
    pass
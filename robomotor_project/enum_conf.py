from enum import IntEnum

class WheelType(IntEnum):
    OMNI_3 = 0
    OMNI_4 = 1
    MECHANUM = 2
    
class ControllerType(IntEnum):
    F310 = 1
    POTABLE = 0
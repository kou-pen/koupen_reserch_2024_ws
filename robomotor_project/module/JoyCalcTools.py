class JoyCalcTools:
    def __init__(self, MODE):
        self.__MODE = MODE
        return
    
    def recalculate_joy(self, joy):
        recalc_joy = [0] * 8
        if self.__MODE == 0:
            recalc_joy[0] = joy.axes[0] * 127 + 128 #left-horizontal
            recalc_joy[1] = joy.axes[1] * 127 + 128 #left-vertical
            recalc_joy[2] = joy.axes[4] * 127 + 128 #right-horizontal
            recalc_joy[3] = joy.axes[3] * -127 + 128 #right-vertical
            recalc_joy[4] = joy.axes[2] * 127 + 128 #left-trigger
            recalc_joy[5] = joy.axes[5] * 127 + 128 #right-trigger
            recalc_joy[6] = 0 #none
            recalc_joy[7] = 0 #none
        else:
            recalc_joy[0] = joy.axes[0] * 127 + 128 #left-horizontal
            recalc_joy[1] = joy.axes[1] * 127 + 128 #left-vertical
            recalc_joy[2] = joy.axes[2] * 127 + 128 #right-horizontal
            recalc_joy[3] = joy.axes[3] * 127 + 128 #right-vertical
            recalc_joy[4] = 0 #none
            recalc_joy[5] = 0 #none
            recalc_joy[6] = 0 #none
            recalc_joy[7] = 0 #none
            
        recalc_joy = list(map(int, recalc_joy))
        return recalc_joy
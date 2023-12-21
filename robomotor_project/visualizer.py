from module.UsbCan import UsbCan
from module.RobomusTools import *

import can
import time
import numpy as np
import matplotlib.pyplot as plt

Ucan = UsbCan()
Ucan.open()

fig = plt.figure()
ax1 = fig.add_subplot(2, 2, 1)
ax1.set_title("motor1")

ax2 = fig.add_subplot(2, 2, 2)
ax2.set_title("motor2")

ax3 = fig.add_subplot(2, 2, 3)
ax3.set_title("motor3")

t = []

y1_cmd = []
y1_feed = []

y2_cmd = []
y2_feed = []

y3_cmd = []
y3_feed = []

cmd, feed = "blue", "green"

def main():
    count = 0
    while True:
        count += 1
        rcv_msg = Ucan.receive()
        t.append(count)
        if rcv_msg.arbitration_id == 0x200:
            data_h_1 = rcv_msg.data[0]
            data_l_1 = rcv_msg.data[1]
            data_1 = joint_highlow_bit(data_h_1, data_l_1)
            motor1_command_data = raw_rpm2rpm(data_1, 36)
            data_h_2 = rcv_msg.data[2]
            data_l_2 = rcv_msg.data[3]
            data_2 = joint_highlow_bit(data_h_2, data_l_2)
            motor2_command_data = raw_rpm2rpm(data_2, 36)
            data_h_3 = rcv_msg.data[4]
            data_l_3 = rcv_msg.data[5]
            data_3 = joint_highlow_bit(data_h_3, data_l_3)
            motor3_command_data = raw_rpm2rpm(data_3, 36)
            
        
        elif rcv_msg.arbitration_id == 0x201:
            data_h = rcv_msg.data[0]
            data_l = rcv_msg.data[1]
            data = joint_highlow_bit(data_h, data_l)
            if data > 32768:
                data -= 65535
            motor1_feedback_data = raw_rpm2rpm(data, 36)
            
        elif rcv_msg.arbitration_id == 0x202:
            data_h = rcv_msg.data[2]
            data_l = rcv_msg.data[3]
            data = joint_highlow_bit(data_h, data_l)
            if data > 32768:
                data -= 65535
            motor2_feedback_data = raw_rpm2rpm(data, 36)
            
        elif rcv_msg.arbitration_id == 0x203:
            data_h = rcv_msg.data[4]
            data_l = rcv_msg.data[5]
            data = joint_highlow_bit(data_h, data_l)
            if data > 32768:
                data -= 65535
            motor3_feedback_data = raw_rpm2rpm(data, 36)
            
        else:
            pass
        
        y1_feed.append(motor1_feedback_data)
        y2_feed.append(motor2_feedback_data)
        y3_feed.append(motor3_feedback_data)
        y1_cmd.append(motor1_command_data)
        y2_cmd.append(motor2_command_data)
        y3_cmd.append(motor3_command_data)
        
        motor1_feed_line, = ax1.plot(t, y1_feed, color=feed, linestyle='-')
        motor2_feed_line, = ax2.plot(t, y2_feed, color=feed, linestyle='-')
        motor3_feed_line, = ax3.plot(t, y3_feed, color=feed, linestyle='-')
        motor1_command_line, = ax1.plot(t, y1_cmd, color=cmd, linestyle='--')
        motor2_command_line, = ax2.plot(t, y2_cmd, color=cmd, linestyle='--')
        motor3_command_line, = ax3.plot(t, y3_cmd, color=cmd, linestyle='--')
        
        fig.tight_layout()
        plt.pause(0.001)
        
        motor1_feed_line.remove()
        motor2_feed_line.remove()
        motor3_feed_line.remove()
        motor1_command_line.remove()
        motor2_command_line.remove()
        motor3_command_line.remove()
        
    
main()
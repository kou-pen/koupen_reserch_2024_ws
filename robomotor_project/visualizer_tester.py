from module.UsbCan import UsbCan
from module.RobomusTools import *

import can
import time
import numpy as np
import matplotlib.pyplot as plt

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
        t.append(count)
        
        y1_feed.append(count)
        y2_feed.append(count ** 2)
        y3_feed.append(1 / count)
        y1_cmd.append(count ** 2)
        y2_cmd.append(1 / count)
        y3_cmd.append(count)
        
        motor1_feed_line, = ax1.plot(t, y1_feed, color=feed, linestyle='-')
        motor2_feed_line, = ax2.plot(t, y2_feed, color=feed, linestyle='-')
        motor3_feed_line, = ax3.plot(t, y3_feed, color=feed, linestyle='-')
        motor1_cmd_line, = ax1.plot(t, y1_cmd, color=cmd, linestyle='--')
        motor2_cmd_line, = ax2.plot(t, y2_cmd, color=cmd, linestyle='--')
        motor3_cmd_line, = ax3.plot(t, y3_cmd, color=cmd, linestyle='--')
        
        fig.tight_layout()
        plt.pause(0.001)
        
        motor1_feed_line.remove()
        motor2_feed_line.remove()
        motor3_feed_line.remove()
        motor1_cmd_line.remove()
        motor2_cmd_line.remove()
        motor3_cmd_line.remove()
        
        
main()
        
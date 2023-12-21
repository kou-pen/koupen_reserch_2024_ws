import math

def split_highlow_bit(int_data: int):
    high = int(bin((int(int_data)>> 8) & 0b11111111), 2)
    low = int(bin((int(int_data) & 0x00FF) & 0b11111111), 2)
    return high, low

def joint_highlow_bit(high, low):
    return int(bin((high << 8) | low), 2)

def rad_per_sec_2_rpm(rps):
    return rps *  9.549 #(30 / math.pi)
 
def rpm_2_robomas_command(rpm):
    return rpm * 20

def raw_rpm2rpm(raw,gear):
    return raw/gear
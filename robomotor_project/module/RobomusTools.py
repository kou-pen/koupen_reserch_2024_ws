import math

def split_highlow_bit(int_data: int):
    out_h = int(bin((int_data >> 8) & 0b11111111), 2)
    out_l = int(bin((int_data & 0x00FF) & 0b11111111), 2)
    return out_h, out_l

def rad_per_sec_2_rpm(rps):
    return rps * (30 / math.pi)

def rpm_2_robomas_command(rpm):
    return rpm * 20
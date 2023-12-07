import os
import can

class UsbCan:
    def __init__(self,bitrate: int,buffer: int):
        self.__state = False
        self.__bitrate = bitrate
        self.__buffer = buffer
        return
    
    def __del__(self):
        if self.__state == True:
            os.system('sudo ifconfig can0 down')
        return
    
    def open(self):
        self.__state = True
        try:
            os.system('sudo ip link set can0 type can bitrate ' + str(self.__bitrate))
            os.system('sudo ifconfig can0 up')
            os.system('sudo ifconfig can0 txqueuelen ' + str(self.__buffer)) 
            self.__can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')
        except OSError:
            print('OS Error')
        return
    
    def close(self):
        self.__state = False
        os.system('sudo ifconfig can0 down')
        return
    
    
    def send(self,message):
        if self.__state == True:
            self.__can0.send(msg=message)
        return
    
class CanMessage:
    def __init__(self, can_id: int, is_extended: bool) :
        self.__id = can_id
        self.__is_extended = is_extended
        return
    
    def to_message_object(self,data):
        msg = can.Message(
            arbitration_id = self.__id,
            is_extended_id = self.__is_extended,
            dlc = len(data),
            data = bytearray(data)
        )
        return msg
    
        
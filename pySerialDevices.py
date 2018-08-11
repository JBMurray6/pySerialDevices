import abc 
import sys
import glob
import serial
import time


class abcSerialDevice(abc.ABC):
    __port__=serial.Serial()
    openPorts=[]

    def findAllPorts(self):
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass

        self.openPorts.clear()
        self.openPorts.append(result)
        return result

    def connect(self):
        findAllPorts(self)
        for port in self.openPorts:
            try:
                s=serial.Serial(port)
                dictSets=self.__port__.get_settings()
                s.apply_settings(dictSets)
                s.open()
                s.flush()
                s.write(self.callStr)
                returnStr=""
                timerStart=time.time()
                responseTimeout=500
                while(responseTimeoutt>(time.time()-timerStart)):
                    returnStr.append(s.read_all())
                    if (not returnStr==""):
                        if (not self.responseStr.startswith(returnStr)): 
                            break
                        else:
                            pass
                        
            except:
                self.openPorts.remove(port)

    # def __init__(self):
    #     self.__port__=serial.Serial()
    #     self.__port__.timeout=500
    #     self.Start()
    @abc.abstractmethod
    def Start(self):         
        if self.connect():
            self.initialized=True  
        else:
            Warning("Could not connect to ",self.deviceName )
            self.initialized=False  


    def __init__(self,device_name,call_str="\n",resp_str="",read_str="\n",write_prefix=""):
        self.deviceName=device_name
        self.callStr=call_str
        self.respStr=resp_str
        self.readStr=read_str
        self.writePrefix=write_prefix
        self.__port__=serial.Serial()
        self.__port__.timeout=500
        # self.Start()

    @abc.abstractmethod
    def kickOffRead(self,obj=None):
        if self.initialized:
            self.__port__.write(self.readStr)  
        else:
            Warning("This device was never initialized")

    @abc.abstractmethod
    def readResult(self,obj=None):
        if self.initialized:
            return float(self.__port__.read_all())
        else:
            Warning("This device was never initialized")


print("run")


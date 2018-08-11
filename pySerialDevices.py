import abc 
import sys
import glob
import serial
import time


class abcSerialDevice(abc.ABC):
    callStr="\n"
    responseStr=""


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

    def __init__(self):
        self.__port__=serial.Serial()
        self.__port__.timeout=500
        self.Start()
        

    @abstractmethod
    def Start(self):
    



import abc 
import sys
import glob
import serial
import time

class serialDeviceGroup:
    def __init__(self,deviceArray):
        pass

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
        self.findAllPorts()
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
                while(responseTimeout>(time.time()-timerStart)):
                    returnStr.append(s.read_all())
                    if (not returnStr==""):
                        if (not self.responseStr.startswith(returnStr)): 
                            break
                        else:
                            pass
                        
            except:
                self.openPorts.remove(port)

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
        self.Start()
        super().__init__()

    @abc.abstractmethod
    def write(self):
        """Just a wrapper for serial write

            This may corrupt the kickOffRead/Read result sequence 
            if the result hasn't been read the device responds 
        """
        if self.initialized:
            self.__port__.write(self.readStr)  
        else:
            Warning("This device was never initialized")

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

class readResultStruct:
    def __init__(self, name_type_combos=None):
        """Expects a dictionary or array of tuples with result name and its type"""
        if type(name_type_combos)==type({"name":type(float)}):
            for k,v in name_type_combos.items():
                if (v)==(float or int or str or list):
                    self.nameTypeCombos[k]=v
                else:
                    Warning("Not a recognized type")
        elif name_type_combos==None:
            self.nameTypeCombos={"result":type(float)}
            

class test(abcSerialDevice):
    def __init__(self,device_name):
        super().__init__(device_name)

    def readResult(self,obj=None):
        super().readResult()

    def kickOffRead(self,obj=None):
        super().kickOffRead()

    def write(self):
        super().write()

    def Start(self):   
        super().Start()

a=test("asdf")

str("asdf")

print(a.findAllPorts())
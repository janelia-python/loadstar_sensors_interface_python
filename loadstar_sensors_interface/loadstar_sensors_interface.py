from serial_interface import SerialInterface


DEBUG = False

class LoadstarSensorsInterface():
    '''
    Python interface to Loadstar Sensors USB devices.
    '''
    def __init__(self,*args,**kwargs):
        if 'debug' in kwargs:
            self.debug = kwargs['debug']
        else:
            kwargs.update({'debug': DEBUG})
            self.debug = DEBUG
        self._serial_interface = SerialInterface(*args,**kwargs)

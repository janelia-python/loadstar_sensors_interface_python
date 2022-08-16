from serial_inteface import SerialInterface


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

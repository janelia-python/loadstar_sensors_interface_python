import time
import serial
from serial_interface import SerialInterface, ReadError


DEBUG = False

class LoadstarSensorsInterface():
    '''
    Python interface to Loadstar Sensors USB devices.
    '''
    _REQUEST_EOL = '\r'
    _RESPONSE_EOL = b'\r\n'
    _READ_ATTEMPTS = 100
    _DURATION_BETWEEN_ATTEMPTS = 0.01
    _GOOD_RESPONSE = b'A'
    _WINDOW_MIN = 1
    _WINDOW_MAX = 1024

    def __init__(self,*args,**kwargs):
        if 'debug' in kwargs:
            self.debug = kwargs['debug']
        else:
            kwargs.update({'debug': DEBUG})
            self.debug = DEBUG
        kwargs.update({'baudrate': 9600,
                       'bytesize': serial.EIGHTBITS,
                       'parity': serial.PARITY_NONE,
                       'stopbits': serial.STOPBITS_ONE,
                       'xonxoff': False,
                       'rtscts': False,
                       'dsrdtr': False
                       })
        self._serial_interface = SerialInterface(*args,**kwargs)

    def tare(self):
        for x in range(self._READ_ATTEMPTS):
            response = self._write_read('tare')
            if response == self._GOOD_RESPONSE:
                return True
        return False

    def get_sensor_value(self):
        for x in range(self._READ_ATTEMPTS):
            try:
                response = self._write_read('w')
                sensor_value = float(response)
                return sensor_value
            except ValueError:
                self._sleep()
        return None

    def get_model(self):
        response = self._write_read('model')
        return response

    def get_id(self):
        response = self._write_read('id')
        return response

    def get_units(self):
        response = self._write_read('unit')
        return response

    def get_load_capacity(self):
        response = self._write_read('lc')
        return response

    def get_gain(self):
        response = self._write_read('gain')
        return response

    def get_settings(self):
        response = self._write_read('settings',use_readline=False)
        settings = response.split(self._RESPONSE_EOL)
        return settings

    def get_window(self):
        response = self._write_read('CSS' + self._REQUEST_EOL)
        return response

    def set_window(self, count):
        if count < self._WINDOW_MIN:
            count = self._WINDOW_MIN
        if count > self._WINDOW_MAX:
            count = self._WINDOW_MAX
        for x in range(self._READ_ATTEMPTS):
            response = self._write_read('CSS ' + str(count))
            if response == self._GOOD_RESPONSE:
                return True
        return False

    def _write_read(self,request,use_readline=True):
        for x in range(self._READ_ATTEMPTS):
            try:
                response = self._serial_interface.write_read(request + self._REQUEST_EOL,use_readline=use_readline)
                if response:
                    return response.strip()
            except ReadError:
                self._sleep()
        return None

    def _sleep(self):
        time.sleep(self._DURATION_BETWEEN_ATTEMPTS)

    def _test_response(self):
        response = self._write_read('',use_readline=False)
        return response

    def _clear(self):
        for x in range(self._READ_ATTEMPTS):
            response = self._test_response()
            if response.strip() == self._GOOD_RESPONSE:
                return True
            else:
                self._sleep()
        return False


import time
import serial
from serial_interface import SerialInterface, ReadError


DEBUG = False

class LoadstarSensorsInterface():
    '''
    Python interface to Loadstar Sensors USB devices.
    '''
    _TIMEOUT = 0.05
    _WRITE_TIMEOUT = 0.05
    _WRITE_READ_DELAY = 0.010
    _WRITE_WRITE_DELAY = 0.010
    _REQUEST_EOL = '\r'
    _RESPONSE_EOL = b'\r\n'
    _READ_ATTEMPTS = 100
    _DURATION_BETWEEN_ATTEMPTS = 0.01
    _GOOD_RESPONSE = b'A'
    _AVERAGING_WINDOW_MIN = 1
    _AVERAGING_WINDOW_MAX = 1024
    _AVERAGING_THRESHOLD_MIN = 1
    _AVERAGING_THRESHOLD_MAX = 100

    def __init__(self,*args,**kwargs):
        if 'debug' in kwargs:
            self._debug = kwargs['debug']
        else:
            kwargs.update({'debug': DEBUG})
            self._debug = DEBUG
        if 'timeout' not in kwargs:
            kwargs.update({'timeout': self._TIMEOUT})
        if 'write_timeout' not in kwargs:
            kwargs.update({'write_timeout': self._WRITE_TIMEOUT})
        if 'write_read_delay' not in kwargs:
            kwargs.update({'write_read_delay': self._WRITE_READ_DELAY})
        if 'write_write_delay' not in kwargs:
            kwargs.update({'write_write_delay': self._WRITE_WRITE_DELAY})
        kwargs.update({'baudrate': 9600,
                       'bytesize': serial.EIGHTBITS,
                       'parity': serial.PARITY_NONE,
                       'stopbits': serial.STOPBITS_ONE,
                       'xonxoff': False,
                       'rtscts': False,
                       'dsrdtr': False
                       })
        self._scale_factor = 1.0
        self._serial_interface = SerialInterface(*args,**kwargs)

    def tare(self):
        for x in range(self._READ_ATTEMPTS):
            response = self._send_request_get_response('tare')
            if response == self._GOOD_RESPONSE:
                return True
            else:
                self._debug_print('bad response')
                self._sleep()
        return False

    def get_sensor_value(self):
        for x in range(self._READ_ATTEMPTS):
            try:
                response = self._send_request_get_response('w')
                sensor_value = float(response) * self._scale_factor
                return sensor_value
            except ValueError:
                self._debug_print('ValueError')
                self._sleep()
        return None

    def get_model(self):
        response = self._send_request_get_response('model')
        return response

    def get_device_id(self):
        response = self._send_request_get_response('id')
        return response

    def get_units(self):
        response = self._send_request_get_response('unit')
        return response

    def get_load_capacity(self):
        response = self._send_request_get_response('lc')
        load_capacity = float(response) * self._scale_factor
        return load_capacity

    def set_averaging_window(self, averaging_window):
        if averaging_window < self._AVERAGING_WINDOW_MIN:
            averaging_window = self._AVERAGING_WINDOW_MIN
        if averaging_window > self._AVERAGING_WINDOW_MAX:
            averaging_window = self._AVERAGING_WINDOW_MAX
        response = self._send_request_get_response('CSS ' + str(averaging_window))

    def set_averaging_threshold(self, averaging_threshold):
        if averaging_threshold < self._AVERAGING_THRESHOLD_MIN:
            averaging_threshold = self._AVERAGING_THRESHOLD_MIN
        if averaging_threshold > self._AVERAGING_THRESHOLD_MAX:
            averaging_threshold = self._AVERAGING_THRESHOLD_MAX
        averaging_threshold = averaging_threshold/self._AVERAGING_THRESHOLD_MAX
        response = self._send_request_get_response('CLA ' + str(averaging_threshold))

    def get_scale_factor(self):
        return self._scale_factor

    def set_scale_factor(self, scale_factor):
        self._scale_factor = float(scale_factor)

    def get_settings(self):
        response = self._send_request_get_response('settings')
        settings = []
        for x in range(self._READ_ATTEMPTS):
            response = self._serial_interface.readline()
            if response == b'' or response == self._GOOD_RESPONSE:
                break
            else:
                settings.append(response.strip())
        return settings

    def _send_request_get_response(self,request,use_readline=True):
        self._send_test_requests_until_response_is_valid()
        return self._write_read(request,use_readline)

    def _write_read(self,request,use_readline=True):
        for x in range(self._READ_ATTEMPTS):
            try:
                self._debug_print(request)
                self._serial_interface.reset_input_buffer()
                self._serial_interface.reset_output_buffer()
                response = self._serial_interface.write_read(request + self._REQUEST_EOL,
                                                             use_readline=use_readline,
                                                             check_write_freq=True,
                                                             max_read_attempts=1000)
                self._debug_print(response)
                if response and not response.strip() == b'':
                    return response.strip()
                else:
                    self._debug_print('no response')
                    self._sleep()
            except ReadError:
                self._debug_print('ReadError')
                self._sleep()
        return None

    def _sleep(self):
        time.sleep(self._DURATION_BETWEEN_ATTEMPTS)

    def _send_test_request(self):
        response = self._write_read('',use_readline=False)
        return response

    def _response_is_valid_from_test_request(self):
        response = self._send_test_request()
        return response.strip() == self._GOOD_RESPONSE

    def _send_test_requests_until_response_is_valid(self):
        for x in range(self._READ_ATTEMPTS):
            if self._response_is_valid_from_test_request():
                self._debug_print('response is valid from test request')
                return True
            else:
                self._debug_print('response is not valid from test request')
                self._sleep()
        return False

    def _debug_print(self,to_print):
        if self._debug:
            print(to_print)


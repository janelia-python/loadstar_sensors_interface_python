"""Python interface to Loadstar Sensors USB devices."""
import time
import serial
from enum import Enum

from serial_interface import SerialInterface, ReadError


DEBUG = False


class ScaleFactor(Enum):
    """Common scale factors to convert units."""

    ONE = 1.0
    LB_TO_GM = 453.59237
    LB_TO_KG = 0.45359237
    LB_TO_N = 4.44822
    LB_TO_OZ = 16


class LoadstarSensorsInterface():
    """Loadstar Sensors USB device."""

    _TIMEOUT = 0.05
    _WRITE_TIMEOUT = 0.05
    _WRITE_READ_DELAY = 0.001
    _WRITE_WRITE_DELAY = 0.005
    _REQUEST_EOL = '\r'
    _RESPONSE_EOL = b'\r\n'
    _READ_ATTEMPTS = 100
    _DURATION_BETWEEN_ATTEMPTS = 0.01
    _GOOD_RESPONSE = b'A'
    _AVERAGING_WINDOW_MIN = 1
    _AVERAGING_WINDOW_MAX = 1024
    _AVERAGING_THRESHOLD_MIN = 1
    _AVERAGING_THRESHOLD_MAX = 100
    _AVERAGING_THRESHOLD_SCALING = 4545.4556

    def __init__(self, *args, **kwargs):
        """Accept SerialInterface kwargs."""
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
        self._scale_factor_name = 'ONE'
        self._serial_interface = SerialInterface(*args, **kwargs)

    def get_device_info(self):
        """Query device and return information."""
        device_info = {}
        device_info['port'] = self.get_port()
        device_info['model'] = self.get_model()
        device_info['id'] = self.get_id()
        device_info['native_units'] = self.get_native_units()
        device_info['scale_factor'] = self.get_scale_factor()
        device_info['scale_factor_name'] = self.get_scale_factor_name()
        device_info['load_capacity'] = self.get_load_capacity()
        device_info['averaging_window'] = self.get_averaging_window()
        device_info['averaging_threshold'] = self.get_averaging_threshold()
        return device_info

    def print_device_info(self, additional_device_info={}):
        """Query device and print information."""
        device_info = self.get_device_info()
        device_info.update(additional_device_info)
        print('device info:')
        for key, value in device_info.items():
            print(f'{key:<25}{value}')
        print('')

    def tare(self):
        """Reset sensor values so current value is zero."""
        for x in range(self._READ_ATTEMPTS):
            response = self._send_request_get_response('tare')
            if response == self._GOOD_RESPONSE:
                return True
            else:
                self._debug_print('bad response')
                self._sleep()
        return False

    def get_sensor_value(self):
        """Sensor value after multiplying by scale factor."""
        for x in range(self._READ_ATTEMPTS):
            try:
                response = self._send_request_get_response('w')
                sensor_value = float(response) * self._scale_factor
                return sensor_value
            except ValueError:
                self._debug_print('ValueError')
                self._sleep()
        return None

    def get_port(self):
        """Sensor device name."""
        return self._serial_interface.port

    def get_model(self):
        """Sensor device model."""
        response = self._send_request_get_response('model')
        response = response.decode()
        return response

    def get_id(self):
        """Sensor device id."""
        response = self._send_request_get_response('id')
        response = response.decode()
        return response

    def get_native_units(self):
        """Units before sensor value is multiplied by scale factor."""
        response = self._send_request_get_response('unit')
        response = response.decode()
        return response

    def get_scale_factor(self):
        """Float that gets multiplied to the sensor value."""
        return self._scale_factor

    def get_scale_factor_name(self):
        """Name of the scale factor, if any."""
        return self._scale_factor_name

    def set_scale_factor(self, scale_factor):
        """Float that gets multiplied to the sensor value."""
        if isinstance(scale_factor, ScaleFactor):
            self._scale_factor = scale_factor.value
            self._scale_factor_name = scale_factor.name
            return
        try:
            self._scale_factor = ScaleFactor[scale_factor].value
            self._scale_factor_name = ScaleFactor[scale_factor].name
        except KeyError:
            self._scale_factor = float(scale_factor)
            self._scale_factor_name = None

    def get_load_capacity(self):
        """Maximum sensor value in native units multiplied by scale factor."""
        response = self._send_request_get_response('lc')
        load_capacity = float(response) * self._scale_factor
        return load_capacity

    def get_averaging_window(self):
        """Count of samples to average (1-1024 samples)."""
        response = self._send_request_get_response('css')
        averaging_window = int(response)
        return averaging_window

    def set_averaging_window(self, averaging_window):
        """Count of samples to average (1-1024 samples)."""
        averaging_window = int(averaging_window)
        if averaging_window < self._AVERAGING_WINDOW_MIN:
            averaging_window = self._AVERAGING_WINDOW_MIN
        if averaging_window > self._AVERAGING_WINDOW_MAX:
            averaging_window = self._AVERAGING_WINDOW_MAX
        self._send_request_get_response('css ' + str(averaging_window))

    def get_averaging_threshold(self):
        """Percentage of capacity below which average is performed (1-100%)."""
        response = self._send_request_get_response('cla')
        # e.g. b'00000\t( 2.1999995e-01)'
        averaging_threshold = float(response.decode().split('(')[1].split(')')[0])
        averaging_threshold *= self._AVERAGING_THRESHOLD_SCALING
        averaging_threshold = int(averaging_threshold)
        return averaging_threshold

    def set_averaging_threshold(self, averaging_threshold):
        """Percentage of capacity below which average is performed (1-100%)."""
        averaging_threshold = int(averaging_threshold)
        if averaging_threshold < self._AVERAGING_THRESHOLD_MIN:
            averaging_threshold = self._AVERAGING_THRESHOLD_MIN
        if averaging_threshold > self._AVERAGING_THRESHOLD_MAX:
            averaging_threshold = self._AVERAGING_THRESHOLD_MAX
        averaging_threshold = averaging_threshold/self._AVERAGING_THRESHOLD_MAX
        self._send_request_get_response('cla ' + str(averaging_threshold))

    def _get_device_settings(self):
        response = self._send_request_get_response('settings')
        settings = []
        for x in range(self._READ_ATTEMPTS):
            response = self._serial_interface.readline()
            if response == b'' or response == self._GOOD_RESPONSE:
                break
            else:
                settings.append(response.strip().decode())
        return settings

    def _send_request_get_response(self, request, use_readline=True):
        self._send_test_requests_until_response_is_valid()
        return self._write_read(request, use_readline)

    def _write_read(self, request, use_readline=True):
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
        response = self._write_read('', use_readline=False)
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

    def _debug_print(self, to_print):
        if self._debug:
            print(to_print)

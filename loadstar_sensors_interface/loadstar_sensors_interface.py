"""Python interface to Loadstar Sensors USB devices."""
import asyncio
import serial_asyncio
from time import perf_counter


DEBUG = False


class LoadstarSensorsInterface():
    """Loadstar Sensors USB device."""

    _REQUEST_EOL = b'\r'
    _RESPONSE_EOL = b'\n'
    _MAX_TRY_COUNT = 100
    _GOOD_RESPONSE = b'A'
    _READ_TIMEOUT = 1.0
    # _AVERAGING_WINDOW_MIN = 1
    # _AVERAGING_WINDOW_MAX = 1024
    # _AVERAGING_THRESHOLD_MIN = 1
    # _AVERAGING_THRESHOLD_MAX = 100
    # _AVERAGING_THRESHOLD_SCALING = 4545.4556

    def __init__(self, *args, **kwargs):
        """ """
        self._write_lock = asyncio.Lock()
        self._read_lock = asyncio.Lock()
        self._write_read_lock = asyncio.Lock()
        self._port = None
        self._reader = None
        self._writer = None
        self._getting_sensor_values = False
        self._sensor_value_count = 0

    async def _open_serial_connection(self, port, baudrate):
        """ """
        self._port = port
        self._reader, self._writer = await serial_asyncio.open_serial_connection(url=port, baudrate=baudrate)
        await self._read_until_no_response()
        await self._write_empty_request_until_good_response()

    async def open_high_speed_serial_connection(self, port='/dev/ttyUSB0'):
        """ """
        await self._open_serial_connection(port, baudrate=230400)

    async def open_low_speed_serial_connection(self, port='/dev/ttyUSB0'):
        """ """
        await self._open_serial_connection(port, baudrate=9600)

    async def _write(self, request=b''):
        """ """
        async with self._write_lock:
            await asyncio.sleep(0)
            self._writer.write(request + self._REQUEST_EOL)

    async def _read(self):
        """ """
        async with self._read_lock:
            response = b''
            response = await self._reader.readuntil(self._RESPONSE_EOL)
            response = response.strip()
            return response

    async def _write_read(self, request=b''):
        async with self._write_read_lock:
            await self._write(request)
            response = await self._read()
            return response

    async def _read_until_no_response(self):
        while True:
            try:
                await asyncio.wait_for(self._read(), timeout=self._READ_TIMEOUT)
            except asyncio.TimeoutError:
                return

    async def _write_empty_request_until_good_response(self):
        try_count = 0
        while try_count < self._MAX_TRY_COUNT:
            try_count += 1
            print(f'try_count: {try_count}')
            response = await self._write_read()
            if response == self._GOOD_RESPONSE:
                return
            else:
                print(f'got: {response}')

    async def start_getting_sensor_values(self):
        if not self._getting_sensor_values:
            self._getting_sensor_values = True
            self._sensor_value_count = 0
            await self._write(b'wc')
            self._start_counter = perf_counter()
            while self._getting_sensor_values:
                response = await self._read()
                try:
                    sensor_value = float(response)
                    self._sensor_value_count += 1
                    print(f'{self._sensor_value_count}: {sensor_value}')
                except ValueError:
                    print(f'{response} cannot be converted to float!')

    async def stop_getting_sensor_values(self):
        await asyncio.sleep(0)
        self._getting_sensor_values = False
        end_counter = perf_counter()
        await self._write()
        await self._read_until_no_response()
        duration = end_counter - self._start_counter
        print(f'{self._sensor_value_count} values took: {duration}')
        values_per_second = self._sensor_value_count / duration
        print(f'values_per_second: {values_per_second}')

    async def get_device_info(self):
        """Query device and return information."""
        device_info = {}
        device_info['port'] = self.get_port()
        device_info['model'] = await self.get_model()
        device_info['id'] = await self.get_id()
        device_info['native_units'] = await self.get_native_units()
        device_info['load_capacity'] = await self.get_load_capacity()
        # device_info['averaging_window'] = await self.get_averaging_window_in_samples()
    #     device_info['averaging_threshold'] = self.get_averaging_threshold()
        return device_info

    async def print_device_info(self, additional_device_info={}):
        """Query device and print information."""
        device_info = await self.get_device_info()
        device_info.update(additional_device_info)
        print('device info:')
        for key, value in device_info.items():
            print(f'{key:<25}{value}')
        print('')

    # def tare(self):
    #     """Reset sensor values so current value is zero."""
    #     for x in range(self._READ_ATTEMPTS):
    #         response = self._send_request_get_response('tare')
    #         if response == self._GOOD_RESPONSE:
    #             return True
    #         else:
    #             self._debug_print('bad response')
    #             self._sleep()
    #     return False

    async def get_sensor_value(self):
        """Sensor value."""
        sensor_value = None
        response = await self._write_read(b'w')
        try:
            sensor_value = float(response)
            self._sensor_value_count += 1
            print(f'{self._sensor_value_count}: {sensor_value}')
        except ValueError:
            print(f'{response} cannot be converted to float!')
        return sensor_value

    # def get_adc_value(self):
    #     """ADC value."""
    #     for x in range(self._READ_ATTEMPTS):
    #         try:
    #             response = self._send_request_get_response('r')
    #             sensor_value = float(response)
    #             return sensor_value
    #         except ValueError:
    #             self._debug_print('ValueError')
    #             self._sleep()
    #     return None

    def get_port(self):
        """Sensor device name."""
        return self._port

    async def get_model(self):
        """Sensor device model."""
        response = await self._write_read(b'model')
        response = response.decode()
        return response

    async def get_id(self):
        """Sensor device id."""
        response = await self._write_read(b'id')
        response = response.decode()
        return response

    async def get_native_units(self):
        """Sensor value units."""
        response = await self._write_read(b'unit')
        response = response.decode()
        return response

    async def get_load_capacity(self):
        """Maximum sensor value in native units."""
        response = await self._write_read(b'lc')
        load_capacity = float(response)
        return load_capacity

    # async def get_averaging_window_in_samples(self):
    #     """Count of samples to average (1-1024 samples)."""
    #     response = await self._write_read(b'css')
    #     averaging_window = int(response)
    #     return averaging_window

    # def set_averaging_window_in_samples(self, averaging_window):
    #     """Count of samples to average (1-1024 samples)."""
    #     averaging_window = int(averaging_window)
    #     if averaging_window < self._AVERAGING_WINDOW_MIN:
    #         averaging_window = self._AVERAGING_WINDOW_MIN
    #     if averaging_window > self._AVERAGING_WINDOW_MAX:
    #         averaging_window = self._AVERAGING_WINDOW_MAX
    #     self._write_read(b'css ' + str(averaging_window))

    # def get_averaging_threshold_in_percent(self):
    #     """Percentage of capacity below which average is performed (1-100%)."""
    #     response = self._write_read(b'cla')
    #     # e.g. b'00000\t( 2.1999995e-01)'
    #     averaging_threshold = float(response.decode().split('(')[1].split(')')[0])
    #     averaging_threshold *= self._AVERAGING_THRESHOLD_SCALING
    #     averaging_threshold = int(averaging_threshold)
    #     return averaging_threshold

    # def set_averaging_threshold_in_percent(self, averaging_threshold):
    #     """Percentage of capacity below which average is performed (1-100%)."""
    #     averaging_threshold = int(averaging_threshold)
    #     if averaging_threshold < self._AVERAGING_THRESHOLD_MIN:
    #         averaging_threshold = self._AVERAGING_THRESHOLD_MIN
    #     if averaging_threshold > self._AVERAGING_THRESHOLD_MAX:
    #         averaging_threshold = self._AVERAGING_THRESHOLD_MAX
    #     averaging_threshold = averaging_threshold/self._AVERAGING_THRESHOLD_MAX
    #     self._write_read(b'cla ' + str(averaging_threshold))

    # def _get_device_settings(self):
    #     response = self._write_read(b'settings')
    #     settings = []
    #     for x in range(self._READ_ATTEMPTS):
    #         response = self._serial_interface.readline()
    #         if response == b'' or response == self._GOOD_RESPONSE:
    #             break
    #         else:
    #             settings.append(response.strip().decode())
    #     return settings

    # def _send_request_get_response(self, request, use_readline=True):
    #     self._send_test_requests_until_response_is_valid()
    #     return self._write_read(request, use_readline)

    # def _write_read(self, request, use_readline=True):
    #     for x in range(self._READ_ATTEMPTS):
    #         try:
    #             self._debug_print(request)
    #             self._serial_interface.reset_input_buffer()
    #             self._serial_interface.reset_output_buffer()
    #             response = self._serial_interface.write_read(
    #                 request + self._REQUEST_EOL,
    #                 use_readline=use_readline,
    #                 check_write_freq=True,
    #                 max_read_attempts=1000)
    #             self._debug_print(response)
    #             if response and not response.strip() == b'':
    #                 return response.strip()
    #             else:
    #                 self._debug_print('no response')
    #                 self._sleep()
    #         except ReadError:
    #             self._debug_print('ReadError')
    #             self._sleep()
    #     return None

    # def _sleep(self):
    #     time.sleep(self._DURATION_BETWEEN_ATTEMPTS)

    # def _send_test_request(self):
    #     response = self._write_read('', use_readline=False)
    #     return response

    # def _response_is_valid_from_test_request(self):
    #     response = self._send_test_request()
    #     return response.strip() == self._GOOD_RESPONSE

    # def _send_test_requests_until_response_is_valid(self):
    #     for x in range(self._READ_ATTEMPTS):
    #         if self._response_is_valid_from_test_request():
    #             self._debug_print('response is valid from test request')
    #             return True
    #         else:
    #             self._debug_print('response is not valid from test request')
    #             self._sleep()
    #     return False

    # def _debug_print(self, to_print):
    #     if self._debug:
    #         print(to_print)

async def main():
    dev = LoadstarSensorsInterface()
    await dev.open_high_speed_serial_connection()
    await dev.print_device_info()
    task = asyncio.create_task(dev.start_getting_sensor_values())
    await asyncio.sleep(4)
    await dev.stop_getting_sensor_values()
    await task
    for _ in range(2):
        await dev.get_sensor_value()
        await asyncio.sleep(1)
    await dev.print_device_info()

if __name__ == '__main__':
    asyncio.run(main())

"""Python interface to Loadstar Sensors USB devices."""
import asyncio
import serial_asyncio
from time import perf_counter


async def sensor_value_callback(sensor_value):
    print(f'sensor_value_callback: {sensor_value}')
    await asyncio.sleep(0)

class LoadstarSensorsInterface():
    """Loadstar Sensors USB device."""

    _REQUEST_EOL = b'\r'
    _RESPONSE_EOL = b'\n'
    _TARE_RESPONSE = b'Tared'
    _MAX_TRY_COUNT = 10
    _GOOD_RESPONSE = b'A'
    _READ_TIMEOUT = 1.0
    _TARE_SLEEP = 1.0

    def __init__(self, debug=False):
        """ """
        self._debug = debug
        self._debug_print('LoadstarSensorsInterface initializing...')
        self._write_lock = asyncio.Lock()
        self._read_lock = asyncio.Lock()
        self._write_read_lock = asyncio.Lock()
        self._port = None
        self._baudrate = None
        self._reader = None
        self._writer = None
        self._getting_sensor_values = False
        self._getting_sensor_values_task = None
        self._sensor_value_count = 0
        self._sensor_value_t_start = 0
        self._sensor_value_t_stop = 0
        self._sensor_value_duration = 1
        self._sensor_value_rate = 0
        self._debug_print('LoadstarSensorsInterface initialized')

    async def _open_serial_connection(self, port, baudrate):
        """ """
        self._port = port
        self._baudrate = baudrate
        self._reader, self._writer = await serial_asyncio.open_serial_connection(url=port, baudrate=baudrate)
        self._debug_print(f'serial connection opened with port: {port}, baudrate: {baudrate}')
        await self._read_until_no_response()
        await self._write_empty_request_until_good_response()

    async def open_high_speed_serial_connection(self, port='/dev/ttyUSB0'):
        """ """
        self._debug_print('Opening high speed serial connection...')
        await self._open_serial_connection(port, baudrate=230400)

    async def open_low_speed_serial_connection(self, port='/dev/ttyUSB0'):
        """ """
        self._debug_print('Opening low speed serial connection...')
        await self._open_serial_connection(port, baudrate=9600)

    async def _write(self, request=b''):
        """ """
        async with self._write_lock:
            await asyncio.sleep(0)
            request += self._REQUEST_EOL
            self._writer.write(request)
            self._debug_print(f'request: {request}')

    async def _read(self):
        """ """
        async with self._read_lock:
            response = b''
            try:
                response = await asyncio.wait_for(self._reader.readuntil(self._RESPONSE_EOL), timeout=self._READ_TIMEOUT)
            except asyncio.TimeoutError:
                pass
            response = response.strip()
            self._debug_print(f'response: {response}')
            return response

    async def _write_read(self, request=b''):
        async with self._write_read_lock:
            await self._write(request)
            response = await self._read()
            return response

    async def _read_until_no_response(self):
        self._debug_print(f'_read_until_no_response...')
        while True:
                response = await self._read()
                self._debug_print(f'_read_until_no_response: {response}')
                if response == b'':
                    break
        self._debug_print(f'_read_until_no_response complete')

    async def _write_empty_request_until_good_response(self):
        try_count = 0
        self._debug_print(f'_write_empty_request_until_good_response...')
        while try_count < self._MAX_TRY_COUNT:
            try_count += 1
            response = await self._write_read()
            self._debug_print(f'_write_empty_request_until_good_response: {response}')
            if response == b'':
                raise ConnectionError('Sensor not found, check power and connections!')
            if response == self._GOOD_RESPONSE:
                self._debug_print(f'_write_empty_request_until_good_response complete')
                return

    async def _getting_sensor_values_loop(self, callback):
        self._sensor_value_count = 0
        self._sensor_value_t_start = perf_counter()
        await self._write(b'wc')
        try:
            while True:
                response = await self._read()
                try:
                    sensor_value = float(response)
                    self._sensor_value_count += 1
                    self._debug_print(f'{self._sensor_value_count}: {sensor_value}')
                    await callback(sensor_value)
                except ValueError:
                    self._debug_print(f'{response} cannot be converted to float!')
        except asyncio.CancelledError:
            self._debug_print(f'_getting_sensor_values_loop canceled')

    def start_getting_sensor_values(self, callback=sensor_value_callback):
        if not self._getting_sensor_values:
            self._getting_sensor_values = True
            self._getting_sensor_values_task = asyncio.create_task(self._getting_sensor_values_loop(callback))

    async def stop_getting_sensor_values(self):
        await self._write()
        await asyncio.sleep(0.05)
        self._getting_sensor_values_task.cancel()
        self._sensor_value_t_stop = perf_counter()
        self._sensor_value_duration = self._sensor_value_t_stop - self._sensor_value_t_start
        self._sensor_value_rate = self._sensor_value_count / self._sensor_value_duration
        await self._read_until_no_response()
        self._getting_sensor_values = False

    def get_sensor_value_count(self):
        return self._sensor_value_count

    def get_sensor_value_duration(self):
        return self._sensor_value_duration

    def get_sensor_value_rate(self):
        return self._sensor_value_rate

    async def get_device_info(self):
        """Query device and return information."""
        device_info = {}
        device_info['port'] = self.get_port()
        device_info['baudrate'] = self.get_baudrate()
        device_info['model'] = await self.get_model()
        device_info['id'] = await self.get_id()
        device_info['native_units'] = await self.get_native_units()
        device_info['load_capacity'] = await self.get_load_capacity()
        return device_info

    async def print_device_info(self, additional_device_info={}):
        """Query device and print information."""
        device_info = await self.get_device_info()
        device_info.update(additional_device_info)
        print('device info:')
        for key, value in device_info.items():
            print(f'{key:<25}{value}')
        print('')

    async def tare(self):
        """Reset sensor values so current value is zero."""
        self._debug_print('taring')
        for _ in range(self._MAX_TRY_COUNT):
            response = await self._write_read(b'tare')
            if response == self._TARE_RESPONSE or response == self._GOOD_RESPONSE:
                self._debug_print('taring succeeded')
                return True
            else:
                self._debug_print('bad response from taring')
                asyncio.sleep(self._TARE_SLEEP)
        self._debug_print('taring failed')
        return False

    async def get_sensor_value(self):
        """Sensor value."""
        sensor_value = None
        response = await self._write_read(b'w')
        try:
            sensor_value = float(response)
            self._debug_print(f'sensor_value: {sensor_value}')
        except ValueError:
            self._debug_print(f'{response} cannot be converted to float!')
        return sensor_value

    async def get_adc_value(self):
        """ADC value."""
        adc_value = None
        response = await self._write_read(b'r')
        try:
            adc_value = int(response)
            self._debug_print(f'adc_value: {adc_value}')
        except ValueError:
            self._debug_print(f'{response} cannot be converted to int!')
        return adc_value

    def get_port(self):
        """Sensor device name."""
        return self._port

    def get_baudrate(self):
        """Sensor device port baudrate."""
        return self._baudrate

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

    def _debug_print(self, to_print):
        if self._debug:
            print(to_print)


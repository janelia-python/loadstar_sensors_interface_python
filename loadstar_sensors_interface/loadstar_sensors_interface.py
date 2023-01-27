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
    _MAX_TRY_COUNT = 100
    _GOOD_RESPONSE = b'A'
    _READ_TIMEOUT = 1.0
    _TARE_SLEEP = 1.0

    def __init__(self, debug=False):
        """ """
        self._debug = debug
        self._write_lock = asyncio.Lock()
        self._read_lock = asyncio.Lock()
        self._write_read_lock = asyncio.Lock()
        self._port = None
        self._reader = None
        self._writer = None
        self._getting_sensor_values = False
        self._sensor_value_count = 0
        self._debug_print('LoadstarSensorsInterface initialized')

    async def _open_serial_connection(self, port, baudrate):
        """ """
        self._port = port
        self._reader, self._writer = await serial_asyncio.open_serial_connection(url=port, baudrate=baudrate)
        await self._read_until_no_response()
        await self._write_empty_request_until_good_response()
        self._debug_print(f'serial connection opened with port: {port}, baudrate: {baudrate}')

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
            request += self._REQUEST_EOL
            self._writer.write(request)
            self._debug_print(f'request: {request}')

    async def _read(self):
        """ """
        async with self._read_lock:
            response = b''
            response = await self._reader.readuntil(self._RESPONSE_EOL)
            response = response.strip()
            self._debug_print(f'response: {response}')
            return response

    async def _write_read(self, request=b''):
        async with self._write_read_lock:
            await self._write(request)
            response = await self._read()
            return response

    async def _read_until_no_response(self):
        while True:
            try:
                response = await asyncio.wait_for(self._read(), timeout=self._READ_TIMEOUT)
                self._debug_print(f'_read_until_no_response: {response}')
            except asyncio.TimeoutError:
                return

    async def _write_empty_request_until_good_response(self):
        try_count = 0
        while try_count < self._MAX_TRY_COUNT:
            try_count += 1
            response = await self._write_read()
            self._debug_print(f'_write_empty_request_until_good_response: {response}')
            if response == self._GOOD_RESPONSE:
                return

    async def start_getting_sensor_values(self, callback=sensor_value_callback):
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
                    self._debug_print(f'{self._sensor_value_count}: {sensor_value}')
                    await callback(sensor_value)
                except ValueError:
                    self._debug_print(f'{response} cannot be converted to float!')

    async def stop_getting_sensor_values(self):
        await asyncio.sleep(0)
        self._getting_sensor_values = False
        end_counter = perf_counter()
        await self._write()
        await self._read_until_no_response()
        duration = end_counter - self._start_counter
        self._debug_print(f'{self._sensor_value_count} values took: {duration}')
        values_per_second = self._sensor_value_count / duration
        self._debug_print(f'values_per_second: {values_per_second}')

    async def get_device_info(self):
        """Query device and return information."""
        device_info = {}
        device_info['port'] = self.get_port()
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
            if response == self._GOOD_RESPONSE:
                return True
            else:
                self._debug_print('bad response')
        asyncio.sleep(self._TARE_SLEEP)
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

async def test():
    dev = LoadstarSensorsInterface(debug=True)
    await dev.open_high_speed_serial_connection(port='/dev/ttyUSB0')
    await dev.print_device_info()
    await asyncio.sleep(2)
    task = asyncio.create_task(dev.start_getting_sensor_values())
    await asyncio.sleep(4)
    await dev.stop_getting_sensor_values()
    await task
    for _ in range(2):
        await dev.get_sensor_value()
        await asyncio.sleep(1)
    for _ in range(2):
        await dev.get_adc_value()
        await asyncio.sleep(1)
    await dev.print_device_info()

if __name__ == '__main__':
    asyncio.run(test())

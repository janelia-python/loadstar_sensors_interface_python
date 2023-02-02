- [About](#orgf17de4b)
- [Example Usage](#orgca78427)
- [Installation](#org535d571)
- [Development](#orga1f7467)

    <!-- This file is generated automatically from metadata -->
    <!-- File edits may be overwritten! -->


<a id="orgf17de4b"></a>

# About

```markdown
- Python Package Name: loadstar_sensors_interface
- Description: Python async interface to Loadstar Sensors USB devices.
- Version: 1.1.0
- Release Date: 2023-02-02
- Creation Date: 2022-08-16
- License: BSD-3-Clause
- URL: https://github.com/janelia-pypi/loadstar_sensors_interface_python
- Author: Peter Polidoro
- Email: peter@polidoro.io
- Copyright: 2023 Howard Hughes Medical Institute
- References:
  - https://pyserial-asyncio.readthedocs.io/en/latest/
  - https://python.readthedocs.io/en/latest/library/asyncio.html
  - https://pint.readthedocs.io/en/stable/getting/overview.html
  - https://tinkering.xyz/async-serial/
  - https://www.loadstarsensors.com/
  - https://www.loadstarsensors.com/di-100u-di-1000u-command-set.html
- Dependencies:
  - pyserial-asyncio
  - pint
  - click
```


<a id="orgca78427"></a>

# Example Usage


## Python

```python
from loadstar_sensors_interface import LoadstarSensorsInterface
import asyncio

async def my_sensor_value_callback(sensor_value):
    print(f'my_sensor_value_callback: {sensor_value:.1f}')
    await asyncio.sleep(0)

async def example():
    dev = LoadstarSensorsInterface()
    await dev.open_high_speed_serial_connection(port='/dev/ttyUSB0')
    dev.set_output_units(dev.units.gram)
    await dev.tare()
    dev.start_getting_sensor_values(my_sensor_value_callback)
    await asyncio.sleep(5)
    await dev.stop_getting_sensor_values()
    count = dev.get_sensor_value_count()
    duration = dev.get_sensor_value_duration()
    rate = dev.get_sensor_value_rate()
    print(f'{count} sensor values in {duration:.1f}s at a rate of {rate:.1f}Hz')
    await dev.print_device_info()

asyncio.run(example())
```


## Command Line


### help

```sh
loadstar --help
# Usage: loadstar [OPTIONS]

#   Command line interface for loadstar sensors.

# Options:
#   -p, --port TEXT         Device name (e.g. /dev/ttyUSB0 on GNU/Linux or COM3
#                           on Windows)
#   -H, --high-speed        Open serial port with high speed baudrate.
#   -d, --debug             Print debugging information.
#   -i, --info              Print the device info and exit
#   -T, --tare              Tare before getting sensor values.
#   -d, --duration INTEGER  Duration of sensor value measurements in seconds.
#                           [default: 10]
#   -h, --help              Show this message and exit.
```


### device info

```sh
# DI-100, DI-1000
loadstar --port /dev/ttyUSB0 --info

# DI-1000UHS
loadstar --port /dev/ttyUSB0 --high-speed --info
```


### example usage

```sh
# DI-100, DI-1000
loadstar --port /dev/ttyUSB0 --tare --duration 10

# DI-1000UHS
loadstar --port /dev/ttyUSB0 --high-speed --tare --duration 10
```


<a id="org535d571"></a>

# Installation

<https://github.com/janelia-pypi/python_setup>


## GNU/Linux


### Drivers

GNU/Linux computers usually have all of the necessary drivers already installed, but users need the appropriate permissions to open the device and communicate with it.

Udev is the GNU/Linux subsystem that detects when things are plugged into your computer.

Udev may be used to detect when a loadstar sensor is plugged into the computer and automatically give permission to open that device.

If you plug a sensor into your computer and attempt to open it and get an error such as: "FATAL: cannot open /dev/ttyUSB0: Permission denied", then you need to install udev rules to give permission to open that device.

Udev rules may be downloaded as a file and placed in the appropriate directory using these instructions:

[99-platformio-udev.rules](https://docs.platformio.org/en/stable/core/installation/udev-rules.html)

1.  Download rules into the correct directory

    ```sh
    curl -fsSL https://raw.githubusercontent.com/platformio/platformio-core/master/scripts/99-platformio-udev.rules | sudo tee /etc/udev/rules.d/99-platformio-udev.rules
    ```

2.  Restart udev management tool

    ```sh
    sudo service udev restart
    ```

3.  Ubuntu/Debian users may need to add own “username” to the “dialout” group

    ```sh
    sudo usermod -a -G dialout $USER
    sudo usermod -a -G plugdev $USER
    ```

4.  After setting up rules and groups

    You will need to log out and log back in again (or reboot) for the user group changes to take effect.
    
    After this file is installed, physically unplug and reconnect your board.


### Python Code

The Python code in this library may be installed in any number of ways, chose one.

1.  pip

    ```sh
    python3 -m venv ~/venvs/loadstar_sensors_interface
    source ~/venvs/loadstar_sensors_interface/bin/activate
    pip install loadstar_sensors_interface
    ```

2.  guix

    Setup guix-janelia channel:
    
    <https://github.com/guix-janelia/guix-janelia>
    
    ```sh
    guix install python-loadstar-sensors-interface
    ```


## Windows


### Drivers

Download and install Windows driver:

[Loadstar Sensors Windows Driver](https://www.loadstarsensors.com/drivers-for-usb-load-cells-and-load-cell-interfaces.html)


### Python Code

The Python code in this library may be installed in any number of ways, chose one.

1.  pip

    ```sh
    python3 -m venv C:\venvs\loadstar_sensors_interface
    C:\venvs\loadstar_sensors_interface\Scripts\activate
    pip install loadstar_sensors_interface
    ```


<a id="orga1f7467"></a>

# Development


## Install Guix

[Install Guix](https://guix.gnu.org/manual/en/html_node/Binary-Installation.html)


## Clone Repository

```sh
git clone git@github.com:janelia-pypi/loadstar_sensors_interface_python.git
cd loadstar_sensors_interface_python
```


## Make alias

```sh
source .metadata/.alias
```


## Edit metadata.org

```sh
,make metadata-edits
```


## Tangle metadata.org

```sh
,make metadata
```


## Test Python package using ipython shell

```sh
,make ipython-shell
import loadstar_sensors_interface
exit
```


## Test installation of Guix package

```sh
,make installed-shell
exit
```


## Upload Python package to pypi

```sh
,make upload
```


## Test direct device interaction using serial terminal


### Low Speed

DI-100, DI-1000

```sh
,make serial-shell # PORT=/dev/ttyUSB0
# ,make PORT=/dev/ttyUSB1 serial-shell
? # help
settings
[C-a][C-x] # to exit
```


### High Speed

DI-1000UHS

```sh
,make serial-shell-hs # PORT=/dev/ttyUSB0
# ,make PORT=/dev/ttyUSB1 serial-shell-hs
? # help
settings
[C-a][C-x] # to exit
```


## Test Python package using ipython shell and serial port

```sh
,make ipython-shell-port # PORT=/dev/ttyUSB0
# ,make PORT=/dev/ttyUSB1 ipython-shell-port
import loadstar_sensors_interface
exit
```


## Test installation of Guix package and serial port

```sh
,make installed-shell-port # PORT=/dev/ttyUSB0
# ,make PORT=/dev/ttyUSB1 installed-shell-port
exit
```
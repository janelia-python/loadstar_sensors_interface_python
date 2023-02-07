- [About](#org8b7274e)
- [Example Usage](#org5611217)
- [Installation](#org0e4ec54)
- [Development](#orgc008076)

    <!-- This file is generated automatically from metadata -->
    <!-- File edits may be overwritten! -->


<a id="org8b7274e"></a>

# About

```markdown
- Python Package Name: loadstar_sensors_interface
- Description: Python async interface to Loadstar Sensors USB devices.
- Version: 2.0.0
- Python Version: 3.9
- Release Date: 2023-02-07
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


<a id="org5611217"></a>

# Example Usage


## Python

```python
from loadstar_sensors_interface import LoadstarSensorsInterface
import asyncio

async def my_sensor_value_callback(sensor_value):
    print(f'my_sensor_value_callback: {sensor_value}')
    await asyncio.sleep(0)

async def example():
    dev = LoadstarSensorsInterface()
    await dev.open_high_speed_serial_connection(port='/dev/ttyUSB0')
    dev.set_sensor_value_units('gram')
    dev.set_units_format('.1f')
    await dev.tare()
    dev.start_getting_sensor_values(my_sensor_value_callback)
    await asyncio.sleep(5)
    await dev.stop_getting_sensor_values()
    count = dev.get_sensor_value_count()
    duration = dev.get_sensor_value_duration()
    rate = dev.get_sensor_value_rate()
    print(f'{count} sensor values in {duration} at a rate of {rate}')
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
#   -p, --port TEXT          Device name (e.g. /dev/ttyUSB0 on GNU/Linux or COM3
#                            on Windows)
#   -H, --high-speed         Open serial port with high speed baudrate.
#   -d, --debug              Print debugging information.
#   -i, --info               Print the device info and exit
#   -T, --tare               Tare before getting sensor values.
#   -d, --duration INTEGER   Duration of sensor value measurements in seconds.
#                            [default: 10]
#   -u, --units TEXT         Sensor value units.  [default: gram]
#   -f, --units-format TEXT  Units format.  [default: .1f]
#   -h, --help               Show this message and exit.
```


### device info

```sh
# DI-100, DI-1000
loadstar --port /dev/ttyUSB0 --info

# DI-1000UHS
loadstar --port /dev/ttyUSB0 --high-speed --info
# device info:
# port                     /dev/ttyUSB0
# baudrate                 230400
# model                    FCM DI-1000
# id                       F230235995
# sensor_value_units       gram
# units_format             .1f
# load_capacity            2041.2 gram
```


### example usage

```sh
# DI-100, DI-1000
loadstar --port /dev/ttyUSB0 --tare --duration 10 --units kilogram --units-format=.3f

# DI-1000UHS
loadstar --port /dev/ttyUSB0 --high-speed --tare --duration 10 --units kilogram --units-format=.3f
# 2023-02-03 18:35:11.086982 - sensor_value -> 0.500 kilogram
# 2023-02-03 18:35:11.087548 - sensor_value -> 0.500 kilogram
# 2023-02-03 18:35:11.088130 - sensor_value -> 0.500 kilogram
# 2023-02-03 18:35:11.088705 - sensor_value -> 0.500 kilogram
# 2023-02-03 18:35:11.089174 - sensor_value -> 0.500 kilogram
# 2023-02-03 18:35:11.089540 - sensor_value -> 0.500 kilogram
# 2023-02-03 18:35:11.089905 - sensor_value -> 0.500 kilogram
# 2023-02-03 18:35:11.090268 - sensor_value -> 0.500 kilogram
# 2023-02-03 18:35:11.090634 - sensor_value -> 0.500 kilogram
# 2023-02-03 18:35:11.091001 - sensor_value -> 0.500 kilogram
# 5166 sensor values in 10.051 second at a rate of 513.980 hertz
# device info:
# port                     /dev/ttyUSB0
# baudrate                 230400
# model                    FCM DI-1000
# id                       F230235995
# sensor_value_units       kilogram
# units_format             .3f
# load_capacity            2.041 kilogram
```


<a id="org0e4ec54"></a>

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


<a id="orgc008076"></a>

# Development


## Clone Repository

```sh
git clone git@github.com:janelia-pypi/loadstar_sensors_interface_python.git
cd loadstar_sensors_interface_python
```


## Guix


### Install Guix

[Install Guix](https://guix.gnu.org/manual/en/html_node/Binary-Installation.html)


### Edit metadata.org

```sh
make -f .metadata/Makefile metadata-edits
```


### Tangle metadata.org

```sh
make -f .metadata/Makefile metadata
```


### Develop Python package

```sh
make -f .metadata/Makefile guix-dev-container
exit
```


### Test Python package using ipython shell

```sh
make -f .metadata/Makefile guix-dev-container-ipython
import loadstar_sensors_interface
exit
```


### Test Python package installation

```sh
make -f .metadata/Makefile guix-container
exit
```


### Upload Python package to pypi

```sh
make -f .metadata/Makefile upload
```


### Test direct device interaction using serial terminal

1.  Low Speed

    DI-100, DI-1000
    
    ```sh
    make -f .metadata/Makefile guix-dev-container-port-serial # PORT=/dev/ttyUSB0
    # make -f .metadata/Makefile PORT=/dev/ttyUSB1 guix-dev-container-port-serial
    ? # help
    settings
    [C-a][C-x] # to exit
    ```

2.  High Speed

    DI-1000UHS
    
    ```sh
    make -f .metadata/Makefile guix-dev-container-port-serial-hs # PORT=/dev/ttyUSB0
    # make -f .metadata/Makefile PORT=/dev/ttyUSB1 guix-dev-container-port-serial-hs
    ? # help
    settings
    [C-a][C-x] # to exit
    ```


### Test Python package using ipython shell with serial port access

```sh
make -f .metadata/Makefile guix-dev-container-port-ipython # PORT=/dev/ttyUSB0
# make -f .metadata/Makefile PORT=/dev/ttyUSB1 guix-dev-container-port-ipython
import loadstar_sensors_interface
exit
```


### Test Python package installation with serial port access

```sh
make -f .metadata/Makefile guix-container-port # PORT=/dev/ttyUSB0
# make -f .metadata/Makefile PORT=/dev/ttyUSB1 guix-container-port
exit
```


## Docker


### Install Docker Engine

<https://docs.docker.com/engine/>


### Develop Python package

```sh
make -f .metadata/Makefile docker-dev-container
exit
```


### Test Python package using ipython shell

```sh
make -f .metadata/Makefile docker-dev-container-ipython
import loadstar_sensors_interface
exit
```


### Test Python package installation

```sh
make -f .metadata/Makefile docker-container
exit
```


### Test Python package using ipython shell with serial port access

```sh
make -f .metadata/Makefile docker-dev-container-port-ipython # PORT=/dev/ttyUSB0
# make -f .metadata/Makefile PORT=/dev/ttyUSB1 docker-dev-container-port-ipython
import loadstar_sensors_interface
exit
```


### Test Python package installation with serial port access

```sh
make -f .metadata/Makefile docker-container-port # PORT=/dev/ttyUSB0
# make -f .metadata/Makefile PORT=/dev/ttyUSB1 docker-container-port
exit
```
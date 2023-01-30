- [About](#orgc574338)
- [Example Usage](#org142b95e)
- [Installation](#org6c17d2b)
- [Development](#org34f28e7)

    <!-- This file is generated automatically from metadata -->
    <!-- File edits may be overwritten! -->


<a id="orgc574338"></a>

# About

```markdown
- Python Package Name: loadstar_sensors_interface
- Description: Python async interface to Loadstar Sensors USB devices.
- Version: 1.0.0
- Release Date: 2023-01-30
- Creation Date: 2022-08-16
- License: BSD-3-Clause
- URL: https://github.com/janelia-pypi/loadstar_sensors_interface_python
- Author: Peter Polidoro
- Email: peter@polidoro.io
- Copyright: 2023 Howard Hughes Medical Institute
- References:
  - https://pyserial-asyncio.readthedocs.io/en/latest/
  - https://tinkering.xyz/async-serial/
  - https://www.loadstarsensors.com/
  - https://www.loadstarsensors.com/di-100u-di-1000u-command-set.html
- Dependencies:
  - pyserial-asyncio
  - click
```


<a id="org142b95e"></a>

# Example Usage


## Python

```python
from loadstar_sensors_interface import LoadstarSensorsInterface
import asyncio

async def my_sensor_value_callback(sensor_value):
    print(f'my_sensor_value_callback: {sensor_value}')
    await asyncio.sleep(0)

async def example():
    dev = LoadstarSensorsInterface(debug=False)
    await dev.open_high_speed_serial_connection(port='/dev/ttyUSB0')
    await dev.print_device_info()
    await dev.tare()
    dev.start_getting_sensor_values(my_sensor_value_callback)
    await asyncio.sleep(4)
    await dev.stop_getting_sensor_values()

asyncio.run(example())
```


## Command Line

```sh
loadstar --help
# Usage: loadstar [OPTIONS]

```

```sh
loadstar --info

```

```sh
loadstar -p /dev/ttyUSB0 --tare -s LB_TO_GM -w 1 -t 25 -f 2 -d 10

```


<a id="org6c17d2b"></a>

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


<a id="org34f28e7"></a>

# Development


## Install Guix

[Install Guix](https://guix.gnu.org/manual/en/html_node/Binary-Installation.html)


## Clone Repository

```sh
git clone https://github.com/janelia-pypi/loadstar_sensors_interface_python
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
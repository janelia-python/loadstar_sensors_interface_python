<!---
    This file is generated automatically from .metadata.org
    File edits may be overwritten!
    --->


# About

```markdown
- Name: loadstar_sensors_interface
- Description: Python interface to Loadstar Sensors USB devices.
- Version: 0.9.0
- Date: 2022-10-26
- License: BSD-3-Clause
- URL: https://github.com/janelia-pypi/loadstar_sensors_interface_python
- Author: Peter Polidoro
- Email: peter@polidoro.io
- Copyright: 2022 Howard Hughes Medical Institute
- Reference: https://www.loadstarsensors.com/
- Dependencies:
  - serial_interface
  - click
```


# Example Usage


## Python

```python
from loadstar_sensors_interface import LoadstarSensorsInterface, ScaleFactor
dev = LoadstarSensorsInterface() # Try to automatically detect port
dev = LoadstarSensorsInterface(port='/dev/ttyUSB0') # GNU/Linux specific port
dev = LoadstarSensorsInterface(port='/dev/tty.usbmodem262471') # Mac OS X specific port
dev = LoadstarSensorsInterface(port='COM3') # Windows specific port

dev.get_device_info()
dev.tare()
dev.get_sensor_value()

dev.get_port()
dev.get_model()
dev.get_id()
dev.get_native_units()
dev.get_load_capacity()
dev.set_averaging_window(5) # 1-1024 samples
dev.get_averaging_window()
dev.set_averaging_threshold(25) # 1-100 percent
dev.get_averaging_threshold()

dev.set_scale_factor(ScaleFactor.LB_TO_GM)
dev.get_scale_factor()

dev.set_scale_factor('LB_TO_GM') # ScaleFactor string
dev.get_scale_factor()

dev.set_scale_factor(25.4) # float e.g. in to mm
dev.get_scale_factor()
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


# Development


## Install Guix

[Install Guix](https://guix.gnu.org/manual/en/html_node/Binary-Installation.html)


## Clone Repository

```sh
git clone https://github.com/janelia-pypi/loadstar_sensors_interface_python
cd loadstar_sensors_interface_python
```


## Edit .metadata.org

```sh
make edits
```


## Tangle .metadata.org

```sh
make files
```


## Test Python package using ipython shell

```sh
make ipython-shell
import loadstar_sensors_interface
exit
```


## Test installation of Guix package

```sh
make installed-shell
exit
```


## Upload Python package to pypi

```sh
make upload
```


## Test direct device interaction using serial terminal

```sh
make serial-shell
? # help
settings
[C-a][C-x] # to exit
```
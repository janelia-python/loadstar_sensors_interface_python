<!-- README.md is generated automatically from .single-source-of-truth.org
    File edits may be overwritten! -->


# About

```markdown
- Name: loadstar_sensors_interface
- Version: 0.6.0
- Description: Python interface to Loadstar Sensors USB devices.
- License: BSD 3-Clause License
- URL: https://github.com/janelia-pypi/loadstar_sensors_interface_python
- Author: Peter Polidoro
- Email: peter@polidoro.io
- Copyright: 2022 Howard Hughes Medical Institute
- Reference: https://www.loadstarsensors.com/
- Dependencies:
  - serial_interface
  - click
  - plotext
```


# Example Usage

```python
from loadstar_sensors_interface import LoadstarSensorsInterface
dev = LoadstarSensorsInterface() # Try to automatically detect port
dev = LoadstarSensorsInterface(port='/dev/ttyUSB0') # Linux specific port
dev = LoadstarSensorsInterface(port='/dev/tty.usbmodem262471') # Mac OS X specific port
dev = LoadstarSensorsInterface(port='COM3') # Windows specific port

dev.tare()
sensor_value = dev.get_sensor_value()

model = dev.get_model()
device_id = dev.get_device_id()
units = dev.get_units()
load_capactiy = dev.get_load_capacity()
dev.set_averaging_window(10) # 1-1024 samples
dev.set_averaging_threshold(10) # 1-100 percent

dev.set_scale_factor(453.59) # e.g. lb to gram
scale_factor = dev.get_scale_factor()

settings = dev.get_settings()

```


# Installation

<https://github.com/janelia-pypi/python_setup>


## Linux


### udev rules

[99-platformio-udev.rules](https://docs.platformio.org/en/stable/core/installation/udev-rules.html)

```sh
# Recommended
curl -fsSL https://raw.githubusercontent.com/platformio/platformio-core/master/scripts/99-platformio-udev.rules | sudo tee /etc/udev/rules.d/99-platformio-udev.rules

# OR, manually download and copy this file to destination folder
sudo cp 99-platformio-udev.rules /etc/udev/rules.d/99-platformio-udev.rules

# Restart udev management tool
sudo service udev restart

# or
sudo udevadm control --reload-rules
sudo udevadm trigger

# Ubuntu/Debian users may need to add own “username” to the “dialout” group
sudo usermod -a -G dialout $USER
sudo usermod -a -G plugdev $USER
```


### pip

```sh
python3 -m venv ~/venvs/loadstar_sensors_interface
source ~/venvs/loadstar_sensors_interface/bin/activate
pip install loadstar_sensors_interface
```


### guix

Setup guix-janelia channel:

<https://github.com/guix-janelia/guix-janelia>

```sh
guix install python-loadstar-sensors-interface
```


## Windows


### drivers

Download and install Windows driver:

[Loadstar Sensors Windows Driver](https://www.loadstarsensors.com/drivers-for-usb-load-cells-and-load-cell-interfaces.html)


### pip

```sh
python3 -m venv C:\venvs\loadstar_sensors_interface
C:\venvs\loadstar_sensors_interface\Scripts\activate
pip install loadstar_sensors_interface
```
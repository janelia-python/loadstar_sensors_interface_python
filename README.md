<!-- README.md is generated automatically from .single-source-of-truth.org
    File edits may be overwritten! -->


# About

```text
- Name: loadstar_sensors_interface
- Version: 0.2.0
- Description: Python interface to Loadstar Sensors USB devices.
- License: BSD 3-Clause License
- URL: https://github.com/janelia-pypi/loadstar_sensors_interface_python
- Author: Peter Polidoro
- Email: peter@polidoro.io
- Copyright: 2022 Howard Hughes Medical Institute
- Reference: [Loadstar Sensors](https://www.loadstarsensors.com/)
- Dependencies:
  - serial_interface
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
id = dev.get_id()
units = dev.get_units()
load_capactiy = dev.get_load_capacity()
gain = dev.get_gain()

```


# Installation

<https://github.com/janelia-pypi/python_setup>


## Linux


### udev rules

```sh
sudo cp 77-loadstar-sensors.rules /etc/udev/rules.d/
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

```sh
python3 -m venv C:\venvs\loadstar_sensors_interface
C:\venvs\loadstar_sensors_interface\Scripts\activate
pip install loadstar_sensors_interface
```


# Test

```sh
guix shell picocom
picocom -b 9600 -f n -y n -d 8 -p 1 -c /dev/ttyUSB0
?
```
<!-- README.me is generated automatically from .single-source-of-truth.org
    File edits may be overwritten! -->


# About

```text
- Name: loadstar_sensors_interface
- Version: 0.1.0
- Description: Python interface to Loadstar Sensors USB devices.
- License: BSD 3-Clause License
- URL: https://github.com/janelia-pypi/loadstar_sensors_interface_python
- Author: Peter Polidoro
- Email: peter@polidoro.io
- Copyright: 2022 Howard Hughes Medical Institute
- Dependencies:
  - serial_interface
```


# More Information

This library is an interface to [Loadstar Sensors](https://www.loadstarsensors.com/) USB devices.


# Example Usage

```python
from loadstar_sensors_interface import LoadstarSensorsInterface
dev = LoadstarSensorsInterface() # Try to automatically detect port
dev = LoadstarSensorsInterface(port='/dev/ttyACM0') # Linux specific port
dev = LoadstarSensorsInterface(port='/dev/tty.usbmodem262471') # Mac OS X specific port
dev = LoadstarSensorsInterface(port='COM3') # Windows specific port

```


# Installation

<https://github.com/janelia-pypi/python_setup>


## Linux and Mac OS X

```sh
python3 -m venv ~/venvs/loadstar_sensors_interface
source ~/venvs/loadstar_sensors_interface/bin/activate
pip install loadstar_sensors_interface
```


## Windows

```sh
python3 -m venv C:\venvs\loadstar_sensors_interface
C:\venvs\loadstar_sensors_interface\Scripts\activate
pip install loadstar_sensors_interface
```


## Guix

Setup guix-janelia channel:

<https://github.com/guix-janelia/guix-janelia>

```sh
guix install python-loadstar-sensors-interface
```
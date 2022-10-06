<!---
    This file is generated automatically from .single-source-of-truth.org
    File edits may be overwritten!
    --->


# About

```markdown
- Name: loadstar_sensors_interface
- Version: 0.9.0
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
```


# Example Usage


## Python

```python
from loadstar_sensors_interface import LoadstarSensorsInterface, ScaleFactor
dev = LoadstarSensorsInterface() # Try to automatically detect port
dev = LoadstarSensorsInterface(port='/dev/ttyUSB0') # Linux specific port
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


# Development

[DEVELOPMENT.md](./DEVELOPMENT.md)


# Redistributions of source code must retain the above copyright notice, this

list of conditions and the following disclaimer.


# Redistributions in binary form must reproduce the above copyright notice, this

list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.


# Neither the name of HHMI nor the names of its contributors may be used to

endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. \#+END\_SRC
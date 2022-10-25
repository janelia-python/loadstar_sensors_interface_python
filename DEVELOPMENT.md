<!---
This file is generated automatically from .single-source-of-truth.org
File edits may be overwritten!
--->
# Install Guix
[Install Guix](https://guix.gnu.org/manual/en/html_node/Binary-Installation.html)

# Clone Repository

```shell
git clone https://github.com/janelia-pypi/loadstar_sensors_interface_python
cd loadstar_sensors_interface_python
```

# Edit .single-source-of-truth

```shell
make edits
```

# Tangle .single-source-of-truth

```shell
make files
```

# Test Python package using ipython shell

```shell
make ipython-shell
import loadstar_sensors_interface
exit
```

# Test installation of Guix package

```shell
make installed-shell
exit
```

# Upload Python package to pypi

```shell
make upload
```

# Test direct device interaction using serial terminal

```shell
make serial-shell
? # help
settings
[C-a][C-x] # to exit
```

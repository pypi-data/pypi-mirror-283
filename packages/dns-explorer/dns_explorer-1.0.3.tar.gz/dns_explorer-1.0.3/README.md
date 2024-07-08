# DNS explorer

<img align="right" src="https://raw.githubusercontent.com/vroncevic/dns_explorer/dev/docs/dns_explorer_logo.png" width="25%">

**dns_explorer** is toolset for checking DNS.

Developed in **[python](https://www.python.org/)** code.

The README is used to introduce the modules and provide instructions on
how to install the modules, any machine dependencies it may have and any
other information that should be provided before the modules are installed.

[![dns_explorer python checker](https://github.com/vroncevic/dns_explorer/actions/workflows/dns_explorer_python_checker.yml/badge.svg)](https://github.com/vroncevic/dns_explorer/actions/workflows/dns_explorer_python_checker.yml) [![dns_explorer package checker](https://github.com/vroncevic/dns_explorer/actions/workflows/dns_explorer_package_checker.yml/badge.svg)](https://github.com/vroncevic/dns_explorer/actions/workflows/dns_explorer_package.yml) [![GitHub issues open](https://img.shields.io/github/issues/vroncevic/dns_explorer.svg)](https://github.com/vroncevic/dns_explorer/issues) [![GitHub contributors](https://img.shields.io/github/contributors/vroncevic/dns_explorer.svg)](https://github.com/vroncevic/dns_explorer/graphs/contributors)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [Installation](#installation)
    - [Install using pip](#install-using-pip)
    - [Install using build](#install-using-build)
    - [Install using py setup](#install-using-py-setup)
    - [Install using docker](#install-using-docker)
- [Dependencies](#dependencies)
- [Tool structure](#tool-structure)
- [Docs](#docs)
- [Contributing](#contributing)
- [Copyright and licence](#copyright-and-licence)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

### Installation

Used next development environment

![debian linux os](https://raw.githubusercontent.com/vroncevic/dns_explorer/dev/docs/debtux.png)

[![dns_explorer python3 build](https://github.com/vroncevic/dns_explorer/actions/workflows/dns_explorer_python3_build.yml/badge.svg)](https://github.com/vroncevic/dns_explorer/actions/workflows/dns_explorer_python3_build.yml)

Currently there are three ways to install package
* Install process based on using pip mechanism
* Install process based on build mechanism
* Install process based on setup.py mechanism
* Install process based on docker mechanism

##### Install using pip

**dns_explorer** is located at **[pypi.org](https://pypi.org/project/dns_explorer/)**.

You can install by using pip

```bash
# python3
pip3 install dns_explorer
```

##### Install using build

Navigate to release **[page](https://github.com/vroncevic/dns_explorer/releases/)** download and extract release archive.

To install **dns_explorer** type the following

```bash
tar xvzf dns_explorer-x.y.z.tar.gz
cd dns_explorer-x.y.z/
# python3
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py 
python3 -m pip install --upgrade setuptools
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade build
pip3 install -r requirements.txt
python3 -m build --no-isolation --wheel
pip3 install ./dist/dns_explorer-*-py3-none-any.whl
rm -f get-pip.py
chmod 755 /usr/local/lib/python3.10/dist-packages/usr/local/bin/dns_explorer_run.py
ln -s /usr/local/lib/python3.10/dist-packages/usr/local/bin/dns_explorer_run.py /usr/local/bin/dns_explorer_run.py
```

##### Install using py setup

Navigate to **[release page](https://github.com/vroncevic/dns_explorer/releases)** download and extract release archive.

To install **dns_explorer** locate and run setup.py with arguments

```bash
tar xvzf dns_explorer-x.y.z.tar.gz
cd dns_explorer-x.y.z
# python3
pip3 install -r requirements.txt
python3 setup.py install_lib
python3 setup.py install_egg_info
```

##### Install using docker

You can use Dockerfile to create image/container.

### Dependencies

**dns_explorer** requires next modules and libraries

* [ats-utilities - Python App/Tool/Script Utilities](https://pypi.org/project/ats-utilities/)
* [dnspython - DNS toolkit for Python](https://pypi.org/project/dnspython/)

### Tool structure

**dns_explorer** is based on OOP.

Tool structure

```bash
    dns_explorer/
          ├── conf/
          │   ├── dns_explorer.cfg
          │   ├── dns_explorer.logo
          │   ├── dns_explorer_util.cfg
          │   └── subdomains.yaml
          ├── __init__.py
          ├── log/
          │   └── dns_explorer.log
          ├── pro/
          │   └── __init__.py
          ├── py.typed
          └── run/
              └── dns_explorer_run.py
    
    5 directories, 9 files
```

### Code coverage

| Name | Stmts | Miss | Cover |
|------|-------|------|-------|
| `dns_explorer/__init__.py` | 61 | 9 | 85% |
| `dns_explorer/pro/__init__.py` | 96 | 12 | 88% |
| **Total** | 157 | 21 | 87% |

### Docs

[![Documentation Status](https://readthedocs.org/projects/dns_explorer/badge/?version=latest)](https://dns-explorer.readthedocs.io/en/latest/?badge=latest)

More documentation and info at

* [dns_explorer.readthedocs.io](https://dns-explorer.readthedocs.io)
* [www.python.org](https://www.python.org/)

### Contributing

[Contributing to dns_explorer](CONTRIBUTING.md)

### Copyright and licence

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Copyright (C) 2024 by [vroncevic.github.io/dns_explorer](https://vroncevic.github.io/dns_explorer)

**dns_explorer** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 3.x or,
at your option, any later version of Python 3 you may have available.

Lets help and support PSF.

[![Python Software Foundation](https://raw.githubusercontent.com/vroncevic/dns_explorer/dev/docs/psf-logo-alpha.png)](https://www.python.org/psf/)

[![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.python.org/psf/donations/)

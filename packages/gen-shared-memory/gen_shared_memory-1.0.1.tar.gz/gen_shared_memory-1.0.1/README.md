# Generate Shared Memory Modules

<img align="right" src="https://raw.githubusercontent.com/vroncevic/gen_shared_memory/dev/docs/gen_shared_memory_logo.png" width="25%">

**gen_shared_memory** is tool for generation of shared memory modules.

Developed in **[python](https://www.python.org/)** code: **100%**.

The README is used to introduce the modules and provide instructions on
how to install the modules, any machine dependencies it may have and any
other information that should be provided before the modules are installed.

[![gen_shared_memory python checker](https://github.com/vroncevic/gen_shared_memory/actions/workflows/gen_shared_memory_python_checker.yml/badge.svg)](https://github.com/vroncevic/gen_shared_memory/actions/workflows/gen_shared_memory_python_checker.yml) [![gen_shared_memory package checker](https://github.com/vroncevic/gen_shared_memory/actions/workflows/gen_shared_memory_package_checker.yml/badge.svg)](https://github.com/vroncevic/gen_shared_memory/actions/workflows/gen_shared_memory_package.yml) [![GitHub issues open](https://img.shields.io/github/issues/vroncevic/gen_shared_memory.svg)](https://github.com/vroncevic/gen_shared_memory/issues) [![GitHub contributors](https://img.shields.io/github/contributors/vroncevic/gen_shared_memory.svg)](https://github.com/vroncevic/gen_shared_memory/graphs/contributors)

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
- [Copyright and Licence](#copyright-and-licence)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

### Installation

![debian linux os](https://raw.githubusercontent.com/vroncevic/gen_shared_memory/dev/docs/debtux.png)

[![gen_shared_memory python3 build](https://github.com/vroncevic/gen_shared_memory/actions/workflows/gen_shared_memory_python3_build.yml/badge.svg)](https://github.com/vroncevic/gen_shared_memory/actions/workflows/gen_shared_memory_python3_build.yml)

Currently there are three ways to install package
* Install process based on using pip mechanism
* Install process based on build mechanism
* Install process based on setup.py mechanism
* Install process based on docker mechanism

##### Install using pip

**gen_shared_memory** is located at **[pypi.org](https://pypi.org/project/gen-shared-memory/)**.

You can install by using pip

```bash
# python3
pip3 install gen-shared-memory
```

##### Install using build

Navigate to release **[page](https://github.com/vroncevic/gen_shared_memory/releases/)** download and extract release archive.

To install **gen_shared_memory** type the following

```bash
tar xvzf gen_shared_memory-x.y.z.tar.gz
cd gen_shared_memory-x.y.z/
# python3
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py 
python3 -m pip install --upgrade setuptools
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade build
pip3 install -r requirements.txt
python3 -m build --no-isolation --wheel
pip3 install ./dist/gen_shared_memory-*-py3-none-any.whl
rm -f get-pip.py
chmod 755 /usr/local/lib/python3.10/dist-packages/usr/local/bin/gen_shared_memory_run.py
ln -s /usr/local/lib/python3.10/dist-packages/usr/local/bin/gen_shared_memory_run.py /usr/local/bin/gen_shared_memory_run.py
```

##### Install using py setup

Navigate to release **[page](https://github.com/vroncevic/gen_shared_memory/releases/)** download and extract release archive.

To install **gen_shared_memory** locate and run setup.py with arguments

```bash
tar xvzf gen_shared_memory-x.y.z.tar.gz
cd gen_shared_memory-x.y.z/
# python3
pip3 install -r requirements.txt
python3 setup.py install_lib
python3 setup.py install_data
python3 setup.py install_egg_info
```

##### Install using docker

You can use docker to create image/container.

### Dependencies

**gen_shared_memory** requires next modules and libraries

* [ats-utilities - Python App/Tool/Script Utilities](https://vroncevic.github.io/ats_utilities)

### Tool structure

**gen_shared_memory** is based on OOP

Generator structure

```bash
    gen_shared_memory/
           ├── conf/
           │   ├── gen_shared_memory.cfg
           │   ├── gen_shared_memory.logo
           │   ├── gen_shared_memory_util.cfg
           │   ├── project.yaml
           │   └── template/
           │       ├── client.template
           │       ├── Makefile.template
           │       ├── server.template
           │       └── shared_memory.template
           ├── __init__.py
           ├── log/
           │   └── gen_shared_memory.log
           ├── pro/
           │   ├── __init__.py
           │   ├── read_template.py
           │   └── write_template.py
           ├── py.typed
           └── run/
               └── gen_shared_memory_run.py
    
    6 directories, 15 files
```

### Code coverage

| Name | Stmts | Miss | Cover |
|------|-------|------|-------|
| `gen_shared_memory/__init__.py` | 71 | 12 | 83% |
| `gen_shared_memory/pro/__init__.py` | 59 | 2 | 97% |
| `gen_shared_memory/pro/read_template.py` | 53 | 2 | 96% |
| `gen_shared_memory/pro/write_template.py` | 54 | 3 | 94% |
| **Total** | 237 | 19 | 92% |

### Docs

[![Documentation Status](https://readthedocs.org/projects/gen_shared_memory/badge/?version=latest)](https://gen-shared-memory.readthedocs.io/projects/gen_shared_memory/en/latest/?badge=latest)

More documentation and info at
* [gen_shared_memory.readthedocs.io](https://gen-shared-memory.readthedocs.io/en/latest/)
* [www.python.org](https://www.python.org/)

### Contributing

[Contributing to gen_shared_memory](CONTRIBUTING.md)
    
### Copyright and Licence

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Copyright (C) 2018 - 2024 by [vroncevic.github.io/gen_shared_memory](https://vroncevic.github.io/gen_shared_memory)

**gen_shared_memory** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 3.x or,
at your option, any later version of Python 3 you may have available.

Lets help and support PSF.

[![Python Software Foundation](https://raw.githubusercontent.com/vroncevic/gen_shared_memory/dev/docs/psf-logo-alpha.png)](https://www.python.org/psf/)

[![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.python.org/psf/donations/)
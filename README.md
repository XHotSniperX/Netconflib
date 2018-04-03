# netconflib

[![build](https://travis-ci.org/XHotSniperX/Netconflib.svg?branch=master)](https://travis-ci.org/XHotSniperX/Netconflib)
[![PyPI version](https://badge.fury.io/py/netconflib.svg)](https://badge.fury.io/py/netconflib)
[![codecov](https://codecov.io/gh/XHotSniperX/Netconflib/branch/master/graph/badge.svg)](https://codecov.io/gh/XHotSniperX/Netconflib)
[![HitCount](http://hits.dwyl.io/xhotsniperx/Netconflib.svg)](http://hits.dwyl.io/xhotsniperx/Netconflib)
[![license](https://img.shields.io/badge/license-GPLv3-blue.svg)](LICENSE)
[![platform](https://img.shields.io/badge/platform-Windows%2010%2C%20macOS%2C%20Linux-blue.svg)](https://img.shields.io)

A library for configuring the network topology of a Linux  cluster

## Table Of Contents

- [netconflib](#netconflib)
    - [Table Of Contents](#table-of-contents)
    - [Summary](#summary)
    - [Requirements](#requirements)
        - [Platform](#platform)
        - [Windows specific](#windows-specific)
        - [macOS specific](#macos-specific)
        - [Linux specific (via apt-get)](#linux-specific-via-apt-get)
    - [Installation](#installation)
    - [Usage](#usage)
        - [Use it as an application](#use-it-as-an-application)
        - [Use it as a library](#use-it-as-a-library)
    - [Roadmap](#roadmap)
    - [License](#license)

## Summary

Für den 4x4x4 Cluster mit Odroid-Knoten, der dieses Jahr am Departenment gebaut wurde, soll eine Python-Bibliothek entworfen und geschrieben werden, die eine Rekonfiguration der Netzwerktopologie erlaubt. Angedacht sind Stern- sowie mehrere Bäume und Ring-Topologien, die an einem Kontrollrechner ausgewählt und dann automatisch auf den Knoten des Clusters aktiviert werden. Damit kann man verteilte Anwendungen verschiedenem "Internet-Wetter" aussetzen und ihre Reaktion darauf zeigen. Interessant wäre es, die graphischen Anzeigen zur Darstellung der aktuellen Topologie einzusetzen.

For the 4x4x4 cluster with Odroid nodes, which was built at the Departenment of the University of Basel this year, a Python library is to be designed and written, which allows a reconfiguration of the network topology. It is intended to have star as well as several tree and ring topologies, which are selected on a control computer and then automatically activated on the node of the cluster. This can expose distributed applications to various "internet weather" and show their reaction to it. It would be interesting to use the graphic displays to represent the current topology (or to visualize it in a different way).

## Requirements

Please check the requirements stated below to make sure that everything runs fine.

### Platform

Windows | macOS | Linux
---------|----------|---------
 10 version 1709+ | 10.13+ | Ubuntu 17.10+

### Windows specific

- Python 3.5+ incl. pip3 and Tk toolkit
- Npcap 0.98+
- OpenSSH client (activate it in your Windows settings under optional features)

### macOS specific

- Python 3.5+ incl. pip3 and Tk toolkit
- tcpdump (should be installed already)

### Linux specific (via apt-get)

- Python 3.5+ incl. pip3 and Tk toolkit
- tcpdump
- build-essential
- libssl-dev
- libffi-dev
- python3-pip
- python3-dev
- python3-tk

## Installation

After having prepared all the requirements listed above, you can install the software via one single command:

```
python pip install netconflib
```

or

```
python pip3 install netconflib
```

On the cluster, make sure to install it with `sudo` because it needs further rights for the sniffing part.

## Usage

You can use Netconflib as a runnable application or as a Python library in your own Python software.

### Use it as an application

```
python -m netconflib -h
```

You can also use the visualization to see the actual topology while sending ping packets. For this, you have to start both, the server and then the client on a controller PC. Don't forget to having configured everything before (installation, config.ini and the cluster).

```
python -m netconflib -server
python -m netconflib -client
```

![The gui.](raw/master/images/gui2.PNG "GUI")

### Use it as a library

There are many function that you can use. Below are a few examples... All the functions are documented.
```python
from netconflib import netconf
nc = netconf.NetConf() #don't forget to configure the config.ini in the app folder in your home directory
nc.enable_ip_forwarding() #activates ip package forwarding on all cluster nodes
nc.update_hosts_file() #updates the hosts file on all nodes with the names specified in config.ini
nc.configure_tree_topology(0, 2) #configures the tree topology on your cluster
nc.open_shell(1) #opens one new SSH enabled window to the node with id=1
```

## Roadmap

Begin: 29.11.2017
End: 29.03.2018

## License

GPL v3
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
        - [Python](#python)
    - [Usage](#usage)
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
 0.3+ | 0.3+ | 0.3+

### Python

- Python 3.5
- Python 3.6

## Usage

How to use the library...

```python
s = "Python syntax highlighting"
print s
```

## Roadmap

Begin: 29.11.2017
End: 29.03.2018

## License

GPL v3
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [1.0.5] - 25.04.2018

### Changed

- added option to specify manual server address for visualization part (useful for laptops or PCs with multiple network adapters)

## [1.0.1] - 20.03.2018

### Changed

- few logging improvements

## [1.0] - 18.03.2018

### Added

- added helper and server unit tests
- added program folder for program files
- added more loggings
- added remaining arguments for main

### Changed

- major performance improvements to sniffing and gui
- updated travis
- updated setup.py
- many logging text improvements
- improved logs
- improved stability in sniffing

### Fixed

- fixed server bug
- fixed server config path
- handling exception
- fixed bug in ssh cluster setup
- fixed remote ssh key generation bug
- fixed ipforward permission
- fixed bug in main

### Removed

- dropped python 3.4 support (sorry)

## [0.9] - 11.03.2018

### Added

- gui shows now separate counter for each node
- added unit test for gui

### Changed

- improved logging messages
- updated gui with colors
- separated inits

### Fixed

- fixed logging mess
- fixed exit endless loop

## [0.8] - 10.03.2018

### Added

- client server progress
- added initial gui base

### Changed

- other minor improvements to threading and code

### Fixed

- connection fix (threading) and permission fix

## [0.7] - 06.03.2018

### Changed

- shell update
- multithreaded ssh send and processing for faster speed
- changed sniff command from python to python3

### Fixed

- max shell fix
- open shell fix for mac
- args fix
- sniffing client server fixes
- minor fixes

## [0.6] - 03.03.2018

### Added

- code coverage
- added base for server/client sniffing
- open shell support for Linux, Windows and macOS
- automatic cluster ssh key configuration

### Changed

- readme updates
- travis updates
- improved path management

### Fixed

- scapy bug fixed
- package fixes
- fix for open shell on linux and mac
- fixed open shells

## [0.3] - 14.02.2018

- first PyPI release

[1.0]: https://github.com/XHotSniperX/Netconflib/releases/tag/v1.0
[0.3]: https://github.com/XHotSniperX/Netconflib/releases/tag/0.3
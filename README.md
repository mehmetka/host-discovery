# Host Discovery

### Features
- Host discovery
- Open port discovery by discovered hosts
- IP, Mac Address, Operating System informations

### Used Technologies
- Python Flask for web interface
- Scapy for host, port discovery and information gathering about hosts
- SQLite for data persistence

### Install
- ``docker build -t hostdiscovery .``
- ``docker run -it --name hostdiscovery -p 666:8080 -d hostdiscovery``
- Go to http://host:666

### Theme: 
https://usebootstrap.com/theme/tinydash

### Contributing

Please feel free to contribute.

### License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
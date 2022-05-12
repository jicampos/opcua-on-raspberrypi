# opcua-on-raspberrypi

## Requirements
Server and Client require the following to run:
- Python3.7+
- pyserial
- [opcua-asyncio](https://github.com/FreeOpcUa/opcua-asyncio)

## Installation
```
git clone https://github.com/jicampos/opcua-on-raspberrypi.git
cd opcua-on-raspberrypi
pip install -r requirements.txt
```

## Getting Started 

#### Server
```
python opcua_server.py --ip 0.0.0.0 --port 4840 --serial-port /dev/ttyUSB0
```

#### Client
```
python opcua_client.py --ip 0.0.0.0 --port 4840
```

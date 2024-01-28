mqmiio uses the python-miio (https://github.com/rytilahti/python-miio) library to connect to connect to MIoT devices and make sensor readings and settings available via MQTT.

Installation
- Install python 3
- Install python-miio, use the latest version directly from github
- Instal Paho MQTT
- Checkout mqmiio
- Copy the example mqmiio.cfg to /etc and modify according to your settings. To get the token for your MIoT device, use the command line tool miiocli of the python-miio library
- Start mqmiio: python main.oy

Note: Currently user name and encryption for MQTT is not implemented yet.

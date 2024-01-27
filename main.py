from miio import DeviceFactory
from configparser import ConfigParser
import miiomqtt
import time

if __name__ == '__main__':
    config = ConfigParser()
    config.read('/etc/mqmiio.cfg')

    host = config.get('miio', 'host')
    token = config.get('miio', 'token')

    dev = DeviceFactory.create(host, token, None, force_generic_miot=True)

    while True:
        devStatus = dev.status()

        for attr in devStatus.data:
            print(attr + str(getattr(devStatus, attr)))

        mqtt = miiomqtt.MiioMqtt(config.get('mqtt', 'host'), int(config.get('mqtt', 'port')))
        mqtt.publish_status(devStatus)

        time.sleep(10)

        print("--")

    # settings = dev.settings()
    #
    # on = settings["air-purifier:on"]
    # on.setter(True)

    # print(settings)



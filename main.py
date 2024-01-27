from miio import DeviceFactory
from configparser import ConfigParser
import time
import miiomqtt
import signal

def handler(signum, frame):
    print("Shutting down")
    mqtt.close()
    exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)

    config = ConfigParser()
    config.read('/etc/mqmiio.cfg')

    host = config.get('miio', 'host')
    token = config.get('miio', 'token')

    dev = DeviceFactory.create(host, token, None, force_generic_miot=True)

    while True:
        devStatus = dev.status()

        for attr in devStatus.data:
            print(attr + ": " + str(getattr(devStatus, attr)))

        mqtt = miiomqtt.MiioMqtt(config.get('mqtt', 'host'), int(config.get('mqtt', 'port')))
        mqtt.publish_status(devStatus)

        time.sleep(10)

        print("--")

    # settings = dev.settings()
    #
    # on = settings["air-purifier:on"]
    # on.setter(False)

    # print(on)
    #
    # print(dev.actions)



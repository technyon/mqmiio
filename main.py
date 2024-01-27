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
    
    mqtt_host = config.get('mqtt', 'host')
    mqtt_port = int(config.get('mqtt', 'port'))
    mqtt_topic = config.get('mqtt', 'topic')

    mqtt = miiomqtt.MiioMqtt(mqtt_host, mqtt_port, mqtt_topic)



    host = config.get('miio', 'host')
    token = config.get('miio', 'token')

    dev = DeviceFactory.create(host, token, None, force_generic_miot=True)

    while True:
        devStatus = dev.status()

        for attr in devStatus.data:
            print(attr + ": " + str(getattr(devStatus, attr)))

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



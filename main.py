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

    # Read config
    config = ConfigParser()
    config.read('/etc/mqmiio.cfg')

    # Initialize device
    host = config.get('miio', 'host')
    token = config.get('miio', 'token')

    dev = DeviceFactory.create(host, token, None, force_generic_miot=True)

    # Initialize broker
    mqtt_host = config.get('mqtt', 'host')
    mqtt_port = int(config.get('mqtt', 'port'))
    mqtt_topic = config.get('mqtt', 'topic')

    mqtt = miiomqtt.MiioMqtt(dev, mqtt_host, mqtt_port, mqtt_topic)



    # devInfo = dev.get_property_by(2, 1)
    # devProp = dev.get_properties(["air_purifier_on"])

    lastPubTime = 0

    while True:
        current_time = time.time()

        if current_time - lastPubTime > 3 or mqtt.publish_requested():
            devStatus = dev.status()

            for attr in devStatus.data:
                print(attr + ": " + str(getattr(devStatus, attr)))
            print("--")

            mqtt.publish_status()
            mqtt.publish_setting()

            lastPubTime = time.time()

        time.sleep(0.5)




    # on = settings["air-purifier:on"]
    # on.setter(False)


    # print(dev.actions)



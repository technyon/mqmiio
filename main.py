from miio import DeviceFactory, DeviceException
from configparser import ConfigParser
import time
import miiomqtt
import signal

def handler(signum, frame):
    print("Shutting down")
    try:
        mqtt.close()
    except NameError:
        print()

    exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)

    # Read config
    config = ConfigParser()
    config.read('/etc/mqmiio.cfg')

    # Initialize device
    host = config.get('miio', 'host')
    token = config.get('miio', 'token')

    success = False

    while not success:
        try:
            dev = DeviceFactory.create(host, token, None, force_generic_miot=True)
            success = True
        except DeviceException as err:
            print(f"Failed to connect to MIoT device. Retry in 10 seconds. {err}")
            time.sleep(10)

    # Initialize broker
    mqtt_host = config.get('mqtt', 'host')
    mqtt_port = int(config.get('mqtt', 'port'))
    mqtt_topic = config.get('mqtt', 'topic')

    mqtt = miiomqtt.MiioMqtt(dev, mqtt_host, mqtt_port, mqtt_topic)

    lastPubTime = 0

    while True:
        current_time = time.time()

        if current_time - lastPubTime > 3 or mqtt.publish_requested():
            try:
                devStatus = dev.status()

                for attr in devStatus.data:
                    print(attr + ": " + str(getattr(devStatus, attr)))
                print("--")

                mqtt.publish_status()
                mqtt.publish_setting()

                lastPubTime = time.time()
            except DeviceException as err:
                print(f"Error occured communicating with the MIoT device: {err}")

        time.sleep(0.5)




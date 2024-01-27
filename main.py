from miio import DeviceFactory
from configparser import ConfigParser
import miiomqtt

if __name__ == '__main__':
    config = ConfigParser()
    config.read('/etc/mqmiio.cfg')

    host = config.get('miio', 'host')
    token = config.get('miio', 'token')

    dev = DeviceFactory.create(host, token, None, force_generic_miot=True)
    devStatus = dev.status()

    print("Temperature: " + str(getattr(devStatus, "environment:temperature")))
    print("Humidity: " + str(getattr(devStatus, "environment:relative-humidity")))
    print("Air quality: " + str(getattr(devStatus, "environment:air_quality")))
    print("PM2.5: " + str(getattr(devStatus, "environment:pm2.5_density")))
    print("Filter time left: " + str(getattr(devStatus, "filter:filter_left_time")))
    print("Filter life level: " + str(getattr(devStatus, "filter:filter_life_level")))
    print("Filter used time: " + str(getattr(devStatus, "filter:filter_used_time")))

    mqtt = miiomqtt.MiioMqtt(config.get('mqtt', 'host'), int(config.get('mqtt', 'port')))
    mqtt.publish_status(devStatus)

    # settings = dev.settings()
    #
    # on = settings["air-purifier:on"]
    # on.setter(True)

    # print(settings)



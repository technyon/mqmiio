from miio import DeviceFactory
from configparser import ConfigParser

config = ConfigParser()
config.read('/etc/mqmiio.cfg')

host = config.get('connection', 'host')
token = config.get('connection', 'token')



if __name__ == '__main__':
    dev = DeviceFactory.create(host, token, None, force_generic_miot=True)
    devStatus = dev.status()

    properties = devStatus.property_dict()

    print("Temperature: " + str(getattr(devStatus, "environment:temperature")))
    print("Humidity: " + str(getattr(devStatus, "environment:relative-humidity")))
    print("Air quality: " + str(getattr(devStatus, "environment:air_quality")))
    print("PM2.5: " + str(getattr(devStatus, "environment:pm2.5_density")))
    print("Filter time left: " + str(getattr(devStatus, "filter:filter_left_time")))
    print("Filter life level: " + str(getattr(devStatus, "filter:filter_life_level")))
    print("Filter used time: " + str(getattr(devStatus, "filter:filter_used_time")))


# environment_air_quality
# environment_pm2.5_density
# environment_relative_humidity
# environment_temperature
# filter_filter_left_time
# filter_filter_life_level
# filter_filter_used_time
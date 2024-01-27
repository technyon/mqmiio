from paho.mqtt import client as mqtt_client
import random

class MiioMqtt:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_id = f'miio-{random.randint(0, 10000)}'
        self.client = self.connect()

    def connect(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        # Set Connecting Client ID
        client = mqtt_client.Client(self.client_id)
        # client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.connect(self.host, self.port)
        return client

    def _publish(self, topic, message):
        result = self.client.publish(topic, message)
        status = result[0]
        return status

    def publish_status(self, devStatus):
        self._publish("miio/environment/temperature", getattr(devStatus, "environment:temperature"))
        self._publish("miio/environment/humidity", getattr(devStatus, "environment:relative-humidity"))
        self._publish("miio/environment/air_quality", getattr(devStatus, "environment:air_quality"))
        self._publish("miio/environment/pm_2_5", getattr(devStatus, "environment:pm2.5_density"))
        self._publish("miio/filter/timeleft", getattr(devStatus, "filter:filter_left_time"))
        self._publish("miio/filter/level", getattr(devStatus, "filter:filter_life_level"))
        self._publish("miio/filter/used_time", getattr(devStatus, "filter:filter_used_time"))

         # print("Temperature: " + str(getattr(devStatus, "environment:temperature")))
         # print("Humidity: " + str(getattr(devStatus, "environment:relative-humidity")))
         # print("Air quality: " + str(getattr(devStatus, "environment:air_quality")))
         # print("PM2.5: " + str(getattr(devStatus, "environment:pm2.5_density")))
         # print("Filter time left: " + str(getattr(devStatus, "filter:filter_left_time")))
         # print("Filter life level: " + str(getattr(devStatus, "filter:filter_life_level")))
         # print("Filter used time: " + str(getattr(devStatus, "filter:filter_used_time")))
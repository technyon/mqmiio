from paho.mqtt import client as mqtt_client
import random

class MiioMqtt:
    def __init__(self, device, host, port, topic):
        self.device = device
        self.host = host
        self.port = port
        self.topic = topic
        self.client_id = f'miio-{random.randint(0, 10000)}'
        self.client = self.connect()
        self.client.loop_start()
        # self.client.subscribe(topic)
        # self.client.on_message = self.on_message

    # def on_message(client, userdata, msg):
    #     print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    def close(self):
        self.client.loop_stop()
        self.client.disconnect()

    def connect(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker.")
            else:
                print("Failed to connect to MQTT Broker, return code %d\n", rc)

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

    def publish_status(self):
        devStatus = self.device.status()
        for attr in devStatus.data:
            value = str(getattr(devStatus, attr))
            topic = self.topic + "/" + attr.replace(":", "/").replace(".", "_")

            self._publish(topic, value)

    def publish_setting(self):
        settings = self.device.settings()

        for setting in settings:
            setter = settings[setting].setter
            siid = setter.args[0]
            piid = setter.args[1]
            valueObj = self.device.get_property_by(siid, piid)[0]

            topic = self.topic + "/" + setting.replace(":", "/").replace(".", "_")

            self._publish(topic, str(valueObj["value"]))

            # print(setting + ": " + str(valueObj["value"]))
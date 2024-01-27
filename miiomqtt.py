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
        self.client.miiomqtt = self
        self.mapping_topic_setting = {}
        self._subscribe()
        self.client.loop_start()

    def on_message(client, userdata, msg, data):
        # print(f"`{payload.topic}` from `{payload.payload}` topic")
        self = userdata.miiomqtt
        settings = self.device.settings()
        settingName = self.mapping_topic_setting[data.topic]
        setting = settings[settingName]
        payload = data.payload
        # print(setting.type)

        siid = setting.setter.args[0]
        piid = setting.setter.args[1]
        valueObj = self.device.get_property_by(siid, piid)[0]
        current_value = valueObj["value"]

        if "bool" in str(setting.type):
            value = False
            if payload.lower() == b'true':
                value = True

            if value != current_value:
                print(f'bool value {settingName} change from {current_value} to {value}')
                setting.setter(value)
        elif "int" in str(setting.type):
            value = int(payload)

            if value != current_value:
                print(f'int value {settingName} change from {current_value} to {value}')
                setting.setter(value)

        # setting.setter(payload)

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

    def _subscribe(self):
        settings = self.device.settings()

        for setting in settings:
            setter = settings[setting].setter
            siid = setter.args[0]
            piid = setter.args[1]

            topic = self.topic + "/" + setting.replace(":", "/").replace(".", "_")
            self.client.subscribe(topic)
            self.mapping_topic_setting[topic] = setting

        self.client.on_message = self.on_message

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
from paho.mqtt import client as mqtt_client
import random
import time

class MiioMqtt:
    def __init__(self, device, host, port, topic):
        self.device = device
        self.host = host
        self.port = port
        self.topic = topic
        self.client_id = f'miio-{random.randint(0, 10000)}'
        self.client = self._connect()
        self.client.miiomqtt = self
        self.publish_req = False
        self.mapping_topic_setting = {}
        self._subscribe()
        self.client.loop_start()

    def close(self):
        self.client.loop_stop()
        self.client.disconnect()

    def publish_requested(self):
        val = self.publish_req
        self.publish_req = False
        return val

    def _connect(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker.")
                client.miiomqtt._subscribe()
            else:
                print("Failed to connect to MQTT Broker, return code %d\n", rc)

        # Set Connecting Client ID
        client = mqtt_client.Client(self.client_id)
        client.on_connect = on_connect
        client.on_disconnect = self._on_disconnect
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

        self.client.on_message = self._on_message

    def _on_disconnect(self, userdata, rc, data):
        reconnect_delay = 10
        client = self.client

        print("Disconnected with result code: %s", rc)
        while True:
            print("Reconnecting in %d seconds...", reconnect_delay)
            time.sleep(reconnect_delay)

            try:
                client.reconnect()
                print("Reconnected successfully!")
                return
            except Exception as err:
                print("%s. Reconnect failed. Retrying...", err)

        # print.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)

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

            value = valueObj["value"]

            if isinstance(value, bool):
                self._publish(topic, "true" if value else "false")
            else:
                self._publish(topic, str(value))

    def _on_message(client, userdata, msg, data):
        self = userdata.miiomqtt
        settings = self.device.settings()
        settingName = self.mapping_topic_setting[data.topic]
        setting = settings[settingName]
        payload = data.payload

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
                self.publish_req = True
        elif "int" in str(setting.type):
            value = int(payload)

            if value != current_value:
                print(f'int value {settingName} change from {current_value} to {value}')
                setting.setter(value)
                self.publish_req = True

    def _publish(self, topic, message):
        result = self.client.publish(topic, message)
        status = result[0]
        return status
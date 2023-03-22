import paho.mqtt.client as mqtt
import time


class Subscriber:
    def __init__(self, on_message):
        self.mqttc = None
        self.set_client(on_message)

    def set_client(self, on_message):
        self.mqttc = mqtt.Client()
        self.mqttc.on_connect = self.connect
        self.mqttc.on_disconnect = self.disconnect
        self.mqttc.on_subscribe = self.subscribe
        self.mqttc.on_message = on_message

    def connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("subscriber connected")
        else:
            print("bad connection return code = ", rc)

    def disconnect(self, client, userdata, flags, rc=0):
        print(str(rc))

    def subscribe(self, client, userdata, mid, granted_qos):
        print("subscribed: " + str(mid) + " " + str(granted_qos))

    def start(self, host_url, port, topic):
        self.mqttc.connect(host_url, port)
        self.mqttc.subscribe(topic, 1)
        self.mqttc.loop_forever()

    def stop(self):
        self.mqttc.disconnect()


class Publisher:
    def __init__(self):
        self.mqttc = None
        self.set_client()

    def set_client(self):
        self.mqttc = mqtt.Client()
        self.mqttc.on_connect = self.connect
        self.mqttc.on_disconnect = self.disconnect
        self.mqttc.on_publish = self.publish

    def connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("publisher connected")
        else:
            print("bad connection return code = ", rc)

    def disconnect(self, client, userdata, flags, rc=0):
        print(str(rc))

    def publish(self, client, userdata, mid):
        print("publish success, callback mid = ", mid)

    def start(self, host_url, port):
        self.mqttc.connect(host_url, port)
        # self.mqttc.loop_start()

    def stop(self):
        self.mqttc.loop_stop()
        self.mqttc.disconnect()

    def publish(self, topic, data):
        self.mqttc.publish(topic, data, 1)

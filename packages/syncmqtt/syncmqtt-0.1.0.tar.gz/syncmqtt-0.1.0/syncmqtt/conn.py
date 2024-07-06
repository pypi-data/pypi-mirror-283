import paho.mqtt.client as mqtt
from urllib.parse import urlparse

class Connection:
    def __init__(self):
        self.client = None

    def connect(self, broker, live_topic,v2=True):
        self.live_topic = live_topic
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2 if v2 else mqtt.CallbackAPIVersion.VERSION1)
        self.client.will_set(live_topic, 'offline', retain=True)
        
        parsed_url = urlparse(broker)
        hostname = parsed_url.hostname
        port = parsed_url.port or 1883  # Use default MQTT port 1883 if not specified
        
        self.client.connect(hostname, port)
        self.client.loop_start()
        self.client.publish(live_topic, 'online', retain=True)

    def destroy(self):
        if self.client:
            self.client.publish(self.live_topic, 'offline', retain=True)
            self.client.disconnect()
            self.client.loop_stop()


conn = Connection()

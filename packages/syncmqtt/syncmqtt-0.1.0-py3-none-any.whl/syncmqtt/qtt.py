from .conn import conn
from .attr import SyncedAttr
import json

def qtt():
    def decorator(cls):
        original_init = cls.__init__

        def __init__(self, *args, **kwargs):
            if not conn.client:
                raise RuntimeError("MQTT connection is not ready. Please call conn.connect() first.")
            original_init(self, *args, **kwargs)
            self._mqtt_client = conn.client
            self.set_mqtt_client(conn.client)
            self._mqtt_subscriptions = {}
            self._initialize_subscriptions()

        def set_mqtt_client(self, client):
            self._mqtt_client = client
            for name, attr in cls.__dict__.items():
                if isinstance(attr, SyncedAttr):
                    attr.set_mqtt_client(client)

        def _initialize_subscriptions(self):
            for name, method in cls.__dict__.items():
                if hasattr(method, '_mqtt_sub_topic'):
                    topic = method._mqtt_sub_topic
                    self._mqtt_subscriptions[topic] = method
                    self._mqtt_client.subscribe(topic)
                    print(f"Subscribed to topic: {topic}")

            self._mqtt_client.on_message = self._on_message

        def _on_message(self, client, userdata, msg):
            topic = msg.topic
            if topic in self._mqtt_subscriptions:
                method = self._mqtt_subscriptions[topic]
                if method._mqtt_sub_json:
                    payload = json.loads(msg.payload)
                else:
                    payload = msg.payload.decode()
                method(self, payload)

        cls.__init__ = __init__
        cls.set_mqtt_client = set_mqtt_client
        cls._initialize_subscriptions = _initialize_subscriptions
        cls._on_message = _on_message
        return cls

    return decorator
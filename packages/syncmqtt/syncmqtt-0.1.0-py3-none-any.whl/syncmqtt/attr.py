import json

class SyncedAttr:
    def __init__(self, val, topic, push_on_set=True, sync=True, retained=True, json=True):
        self.val = val
        self.topic = topic
        self.push_on_set = push_on_set
        self.sync = sync
        self.retained = retained
        self.json_format = json
        self._mqtt_client = None

    def set_mqtt_client(self, client):
        self._mqtt_client = client
        if self.sync:
            client.subscribe(self.topic)
            client.message_callback_add(self.topic, self._on_message)

    def _on_message(self, client, userdata, message):
        new_val = message.payload
        if self.json_format:
            new_val = json.loads(new_val)
        self.val = new_val

    def __set__(self, instance, value):
        self.val = value
        if self.push_on_set and self._mqtt_client:
            payload = json.dumps(value) if self.json_format else value
            self._mqtt_client.publish(self.topic, payload, retain=self.retained)

    def __get__(self, instance, owner):
        return self.val


def attr(val, topic, push_on_set, sync, retained, json=False):
    return SyncedAttr(val, topic, push_on_set, sync, retained, json)

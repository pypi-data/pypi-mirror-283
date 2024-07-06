def sub(topic, json=False):
    def decorator(method):
        def wrapper(self, *args, **kwargs):
            return method(self, *args, **kwargs)

        wrapper._mqtt_sub_topic = topic
        wrapper._mqtt_sub_json = json
        return wrapper

    return decorator
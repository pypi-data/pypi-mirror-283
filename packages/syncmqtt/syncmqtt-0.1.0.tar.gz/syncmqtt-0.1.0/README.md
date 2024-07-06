# syncmqtt

sync your data with mqtt

## example usage:

```
from syncmqtt import qtt, attr, sub, conn


@qtt()
class SyncedMqtt:
    # push_on_set will pub to topic when assign new value
    # sync wil update value when new message from topic
    # json means value are serialized before send and parsed after receive 
    test_a = attr(val='test_a', topic='/a', push_on_set=True, sync=True, retained=True)
    test_b = attr(val=20, topic='/b', push_on_set=False, sync=True, json=True)  
    test_c = attr(val='test_c', topic='/c', push_on_set=True, sync=False, retained=False)
        
    @sub(topic='/c', json=True)  # make sure test_cb is called when topic='/c' got new message
    def test_cb(self, val):
        print(val)
        self.test_a = val


async def main():
    conn.connect(broker='mqtt://localhost:8000', live_topic='/test_status')
    # init with last_will off => /test_status
    # pub on => /test_status retained, let other know I'm online
    # during conn.connect
    
    sq = SyncedMqtt()  # if use qttclass before conn.connect, raise error

    sq.test_c = 'hello' 

    # pub hello => /c
    # test_cb
    # print hello
    # set test_a
    # pub hello => /a

    conn.destory()  # stop connection
    
    # mqtt connect broken and off => /test_status base on last wil setting

```
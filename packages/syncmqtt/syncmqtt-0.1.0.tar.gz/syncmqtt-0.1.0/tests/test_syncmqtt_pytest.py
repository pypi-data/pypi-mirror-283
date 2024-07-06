import os
import sys

path =  os.path.abspath(os.path.join(os.path.dirname(__file__), '..','syncmqtt'))
print(path)
sys.path.insert(0,path)


import asyncio
import pytest
from syncmqtt import qtt, attr, sub, conn

@qtt()
class SyncedMqtt:
    test_a = attr(val='test_a', topic='/a', push_on_set=True, sync=True, retained=True,json=False)
    test_b = attr(val=5, topic='/b', push_on_set=False, sync=True, json=True,retained=True)
    test_c = attr(val='test_c', topic='/c', push_on_set=True, sync=False, retained=False)
    test_d = attr(val='test_d', topic='/d', push_on_set=True, sync=True, retained=True)
    

    def __init__(self):
        self.callback_called = False

    @sub(topic='/c', json=True)
    def test_cb(self, val):
        self.test_a = val
        conn.client.publish('/b',val)
        self.callback_called = True

@pytest.fixture(scope='module', autouse=True)
def setup_and_teardown():
    conn.connect(broker='mqtt://127.0.0.1:1883', live_topic='/test_status')
    yield
    conn.destroy()

@pytest.mark.asyncio
async def test_attr_set_and_callback():
    sq = SyncedMqtt()
    sq.set_mqtt_client(conn.client)
    sq.test_c = '"12"'
    await asyncio.sleep(1)  # Wait for the message to be processed
    assert sq.test_a == '12' or sq.test_a == b'12' 
    assert sq.test_b == 12
    assert sq.callback_called
    assert sq.test_d == 'test_d'

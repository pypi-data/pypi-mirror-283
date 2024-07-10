from __future__ import annotations

from .credentials import Credentials

import paho.mqtt.client as mqtt
from typing_extensions import Annotated
from pydantic import  PositiveInt
from pydantic.dataclasses import dataclass, Field 
from pydantic.networks import IPvAnyAddress

import yaml
import re
            
CALLBACK_NAMES = [
    'on_connect', 'on_connect_fail', 'on_disconnect',
    'on_subscribe', 'on_unsubscribe',
    'on_message', 'on_publish', 'on_log'
]

@dataclass(config=dict(arbitrary_types_allowed=True, validate_assignment=True,extra='forbid'))
class MQTTClient:

    username: str
    password: str
    topics: list[str]
    server: IPvAnyAddress
    port: Annotated[int, Field(ge=1, le=65535)] = 1883
    qos: Annotated[int, Field(ge=0, le=2)] = 2
    timeout: PositiveInt = 60
    client: mqtt.Client = Field(
        default=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2), 
        repr=False
    )

    @classmethod
    def from_credentials(cls, user: str ='generic_obstech', topics: list[str]=[]) -> MQTTClient:

        creds = Credentials.load('mqtt', user=user)
        return cls(topics=topics, **creds)

    def __post_init__(self):

        self.client.username_pw_set(self.username, password=self.password)

        for callback_name in CALLBACK_NAMES:
            if callback := getattr(self, callback_name, None):
                setattr(self.client, callback_name, callback)

    def loop_forever(self): self.client.loop_forever()

    def loop_start(self): self.client.loop_start()

    def loop_stop(self): self.client.loop_stop()

    def publish(self, **args): self.client.publish(**args)
        
    def connect(self):

        server = str(self.server)
        self.client.connect(server, self.port, self.timeout)

    def disconnect(self):

        self.client.disconnect()

    def on_connect(self, client, userdata, flags, rc, prop):

        if rc != 0:
            msg = 'MQTT connection to {self.server}:{self.port} failed'
            raise ConnectionError(msg)

        topics = [(t, self.qos) for t in self.topics]
        self.client.subscribe(topics)
    
   

class MQTTConsole(MQTTClient):
    
    def on_message(self, client, userdata, message):

        topic = message.topic
        data = message.payload.decode()
        data = re.sub('\\s', '', data)
        msg = f"{topic} {data}"
        msg = msg if len(msg) < 80 else f"{msg[:77]}..."

        print(msg)
    
def console_script():

    import argparse

    parser = argparse.ArgumentParser(
        description='Print MQTT messages to the console'
    )
    parser.add_argument(
        '--topics', nargs="+", default=['#'], metavar='TOPIC',
        help='MQTT topics to monitor.  By default, all.'
    )
    args = parser.parse_args()

    user = 'generic_obstech'
    console = MQTTConsole.from_credentials(user, args.topics)
    console.connect()
    console.loop_forever()

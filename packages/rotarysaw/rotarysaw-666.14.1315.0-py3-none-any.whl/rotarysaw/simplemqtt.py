from rotarysaw.basic import *

try:
    import paho.mqtt.client as mqtt
except ModuleNotFoundError:
    log.error("Module not found: pip3 install paho-mqtt")
    sys.exit(1)


def utf2str(x):
    if isinstance(x, bytes):
        return x.decode('utf8')
    if isinstance(x, str):
        return x
    raise Exception(f"What did you feed me? {x}")

class SimpleMQTT(mqtt.Client):
    def __init__(self, utf8=True, certfile='nucleus_chain.crt', username=None, password=None, initial_subscriptions=None):
        super().__init__(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)


        if username is not None:
            if password is None:
                log.warning("Username set but password blank")
            self.username_pw_set(username, password)

        self.ca = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'ca.crt'
        self.certfile = certfile
        if not self.certfile or not os.path.exists(self.certfile):
            if self.certfile is not None:
                log.warning(f"{self.certfile} missing for MQTT")

            self.certfile = None
            self.tls_set(self.ca, cert_reqs=True)
            self.connect_async("mqtt.uraanikaivos.com", 3883, 60)
        else:
            self.tls_set(self.ca, self.certfile, self.certfile, cert_reqs=True)
            self.connect_async("mqtt.uraanikaivos.com", 8883, 60)

        self.on_connect = self.connect_handler
        self.on_message = self.message_handler
        self.on_disconnect = self.disconnect_handler
        self.payload2utf8 = utf8
        self.listeners = []
        self.initial_subscriptions = ['debug/#', 'brokers']

        if initial_subscriptions is not None:
            self.initial_subscriptions += initial_subscriptions

        self.loop_start()


    def qobject(self):
        if hasattr(self, '_qobj'):
            return self._qobj

        from PyQt6.QtCore import QObject, pyqtSignal

        class Signaler(QObject):
            receive = pyqtSignal(str, str)

            def __init__(self, parent):
                super().__init__(parent=None)
                super().__setattr__('parent', parent)

            def forward(self, msg):
                self.receive.emit(msg.topic, msg.payload)

            def __getattr__(self, item):
                return getattr(self.parent, item)

            def __setattr__(self, key, value):
                setattr(self.parent,key, value)

        self._qobj = Signaler(self)

        return self._qobj


    def register(self, topic, fn):
        self.listeners.append((topic, fn))

    def register_only_payload(self, topic, fn):
        self.register(topic, lambda msg: fn(msg.payload))

    def disconnect_handler(self, client, userdata, disconnect_flag, reason_code, properties):
        log.warning(f"MQTT disconnected: {reason_code}")
        self.reconnect()

    def connect_handler(self, client, userdata, flags, reason_code, properties):
        log.debug(f"Connected with status {reason_code}")
        if reason_code == mqtt.MQTT_ERR_SUCCESS:
            for s in self.initial_subscriptions:
                self.subscribe(s)

    def message_handler(self, client, userdata, msg):
        if self.payload2utf8:
            msg.payload = msg.payload.decode('utf8')

        if hasattr(self,'_qobj'):
            self._qobj.forward(msg)

        for t, fn in self.listeners:
            try:
                if msg.topic[0:len(t)] == t:
                    fn(msg)
            except IndexError as ex:
                log.error(repr(ex))

if __name__ == '__main__':
    log.getLogger().setLevel(log.DEBUG)
    s = SimpleMQTT()
    s.register_only_payload('debug/kraut', lambda msg: print(msg))

    q = s.qobject()
    q.publish('debug/kraut','testi',qos=2)

    while True:
        q.publish('debug/kraut', 'testi')
        s.publish('debug/kraut','moi')
        sleep(1)

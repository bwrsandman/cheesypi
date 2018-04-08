class SensorConfig:
    def __init__(self, string=None, name=None, data_pin=None, DHT_version=None):
        assert((string is None) != (name is None and data_pin is None and DHT_version is None))
        if string is not None:
            splits = string.split(":")
            self.name = splits[0]
            self.data_pin = int(splits[1])
            self.DHT_version = int(splits[2])
        else:
            self.name = name
            self.data_pin = data_pin
            self.DHT_version = DHT_version

    def __repr__(self):
        return "%s:%d:%d" % (self.name, self.data_pin, self.DHT_version)

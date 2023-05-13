import json

from .helpers import get_config_dir


class JsonConfig():
    def __init__(self):
        self.conf = None

    def load(self):
        with open(get_config_dir() + '/settings.json', 'r') as file:
            self.conf = json.load(file)

    def add(self, name: str, ads: bool, delay: str, offset: str):
        if self.conf != None:
            self.conf[name] = {
                'ads': ads,
                'delay': delay,
                'offset': offset,
            }
        self.write()

    def delete(self, name: str):
        if self.conf != None and name != 'default':
            if self.conf.get(name) != None:
                del self.conf[name]
                self.write()

    def write(self):
        if self.conf != None:
            with open(get_config_dir() + '/settings.json', 'w') as file:
                json.dump(self.conf, file)

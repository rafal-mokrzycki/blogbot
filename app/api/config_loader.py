from ruamel.yaml import YAML


class SingletonMeta(type):
    _instance = None

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance


class AuditConfig(metaclass=SingletonMeta):
    def __init__(self):

        print("AuditConfig __init__")
        config_file = r"C:\Users\rafal\Documents\python\blogbot\config.yaml"
        yaml = YAML(typ="safe")
        self.properties = yaml.load(open(config_file))

import yaml
from subscription import Sub


class V2rayManager:

    def __init__(self):
        with open('./config.yaml', 'r', encoding='utf-8') as f:
            self.settings = yaml.safe_load(f.read())

    @property
    def sub(self) -> Sub:
        return Sub(self)


if __name__ == '__main__':
    main = V2rayManager()
    sub = main.sub
    sub.update_subs()

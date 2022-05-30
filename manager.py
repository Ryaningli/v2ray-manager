import os
import sys
from getopt import getopt

import yaml
from settings import Settings
from subscription import Sub
from v2ray import V2ray


BASE_DIR = os.path.split(os.path.realpath(__file__))[0]


class V2rayManager:

    def __init__(self):
        with open(os.path.join(BASE_DIR, 'config.yaml'), 'r', encoding='utf-8') as f:
            self.settings: Settings = Settings(yaml.safe_load(f.read()))

    @property
    def sub(self) -> Sub:
        return Sub(self)

    @property
    def v2ray(self):
        return V2ray(self)

    def main(self, *args):
        opts, argv = getopt(args)
        print(opts)
        print(args)

        allowed_methods = {
            'v2ray': [
                {'start': ['--config']},
                'stop',
                {'restart': ['--config']},
                {'testspeed': ['--config']}],
            'sub': ['upgrade'],
            'proxy': ['set', 'unset']
        }
        # assert len(args) == 2, '参数错误'
        # method, arg = args
        # assert method in allowed_methods, f'未知的方法：{method}'
        # assert arg in allowed_methods[method], f'未知的参数：{arg}'


if __name__ == '__main__':
    manage = V2rayManager()
    manage.main(*sys.argv[1:])
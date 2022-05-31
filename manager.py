import os
import sys
from getopt import getopt

import yaml

from exceptions import ResetMainError
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

    def ruler_and_formatter(self, cmd: str, args: list, configs_list: list):

        def can_int(value):
            try:
                int(value)
                return True
            except ValueError:
                return False

        '''规则集'''
        rules = {
            '1': [
                (lambda: len(args) < 2, '参数错误，最多可输入一个配置id！'),
                (lambda:
                 (len(args) == 1 and can_int(args[0]) and 0 < int(args[0]) <= len(configs_list)) or len(args) == 0,
                 '请输入正确的配置id！')
            ]
        }

        if cmd in rules:
            for rule in rules[cmd]:
                if not rule[0]():
                    if len(rule) > 1:
                        msg = rule[1]
                    else:
                        msg = '命令异常'
                    print(msg)
                    self.main()
        else:
            if args:
                print(f'参数不正确')
                self.main()

        '''格式化集'''
        formatter = {
            '1': lambda: configs_list[int(args[0]) - 1] if len(args) == 1 else None
        }

        if cmd in formatter:
            return formatter[cmd]()
        else:
            return args

    def main(self):
        configs_str, configs_list = self.sub.configs_list()
        msg = '请输入命令：\n' \
              '1：启动v2ray <ID>\n' \
              '2：停止v2ray\n' \
              '3：重启v2ray\n' \
              '4：列出全部订阅' \
              '5：更新订阅\n' \
              '6：列出全部配置文件\n' \
              '7：开启临时代理\n' \
              '8：关闭临时代理\n' \
              '9：开启永久代理\n' \
              '10：关闭永久代理\n' \
              'q：退出\n' \
              '>>> '
        inp = input(msg)
        args = inp.split()
        cmd = args.pop(0)
        args = self.ruler_and_formatter(cmd, args, configs_list)
        match cmd:
            case '1':
                self.v2ray.start(args)
            case '2':
                self.v2ray.stop()
            case '3':
                self.v2ray.restart(args)
            case '6':
                print(configs_str)
            case 'q':
                raise KeyboardInterrupt
            case _:
                print('命令有误')
        self.main()


if __name__ == '__main__':
    try:
        manage = V2rayManager()
        # manage.sub.configs_list()
        manage.main()
    except KeyboardInterrupt:
        print('\nBye!')

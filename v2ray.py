import subprocess
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from manager import V2rayManager


class V2ray:

    def __init__(self, manager: 'V2rayManager'):
        self.manager = manager
        self.settings = manager.settings

    def start(self, config=None):
        print(f'启动{config}')
        # subprocess.run('nohup v2ray -config /etc/v2ray/config-jpn3.json > /etc/v2ray/access.log 2>&1 &')

    def stop(self):
        print('停止V2ray')

    def restart(self, config=None):
        print('重启V2ray')

    def speed_test(self, configs=None):
        ...
import os
import shutil
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from manager import V2rayManager
import subprocess


class Proxy:
    def __init__(self, manager: 'V2rayManager'):
        self.manager = manager
        self.settings = manager.settings

    def set_proxy(self, port=None):
        if port is None:
            port = self.settings.port.http
        file_path = '/root/.bashrc_proxy'
        with open(file_path, 'w', encoding='UTF-8') as f:
            f.write(f'export http_proxy=http://127.0.0.1:{port}/\n'
                    f'export https_proxy=http://127.0.0.1:{port}/')
        print('已设置代理，执行 source ~/.bashrc 或重开shell以生效\n')

    @staticmethod
    def unset_proxy():
        file_path = '/root/.bashrc_proxy'
        if os.path.exists(file_path):
            os.remove(file_path)
        print('已取消设置代理，重开shell以生效\n')

    @staticmethod
    def get_proxy():
        http = os.environ.get('http_proxy')
        https = os.environ.get('https_proxy')
        if http is None and https is None:
            print('未设置代理\n')
        else:
            print('已设置代理\n'
                  f'http_proxy={http}\n'
                  f'https_proxy={https}\n')
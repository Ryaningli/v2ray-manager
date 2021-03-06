import datetime
import hashlib
import json
import os
import random
import shutil
import time
from base64 import b64decode
from typing import TYPE_CHECKING
from urllib.parse import urlsplit
import requests
from base_config import BaseConfig

if TYPE_CHECKING:
    from manager import V2rayManager


class SubConfig:
    def __init__(self, name, path, url, status=True):
        self.name = name
        self.path = path
        self.url = url
        self.status = status

    def to_dict(self):
        return dict(
            name=self.name,
            path=self.path,
            url=self.url,
            status=self.status
        )


class Sub:
    def __init__(self, manager: 'V2rayManager'):
        self.manager = manager
        self.settings = self.manager.settings
        self.tmp_path = os.path.join('/tmp', 'v2ray-subs',
                                     datetime.datetime.now().strftime(f'%Y%m%d%H%M%S%f_{random.randint(1000, 9999)}'))
        self.schemes_allow = ['vmess', 'ss', 'socks']
        self.subs = self.subs_formatter()
        self.configs_path = self.settings['configs_path']

    def subs_formatter(self, subs=None):
        if subs is None:
            subs = self.settings['subs']
        subs_format = []
        for sub in subs:
            url = sub['url']
            path = sub.get('path', hashlib.sha1(url.encode('UTF-8')).hexdigest())
            name = sub.get('name', path)
            status = sub.get('status', True)
            subs_format.append(SubConfig(name, path, url, status).to_dict())
        self.settings_subs_checker(subs_format)
        return subs_format

    @staticmethod
    def settings_subs_checker(subs):
        if len(list(set(list(map(lambda x: x['url'], subs))))) != len(subs):
            print('订阅链接不允许重复，请检查配置文件！')
            exit()

        if len(list(set(list(map(lambda x: x['path'], subs))))) != len(subs):
            print('订阅目录名不允许重复，请检查配置文件！')
            exit()

        return subs

    @staticmethod
    def get_sub_content(url):
        return requests.get(url).text

    def update_subs(self, subs: list = None):
        if subs is None:
            subs = self.subs
        for sub in subs:
            self.update_sub(sub['url'], sub['path'])
        for config_name in os.listdir(self.tmp_path):
            tmp_config_path = os.path.join(self.tmp_path, config_name)
            config_path = os.path.join(self.configs_path, config_name)
            if os.path.exists(config_path):
                shutil.rmtree(config_path)
            os.makedirs(config_path)
            for config_file in os.listdir(tmp_config_path):
                shutil.copyfile(os.path.join(tmp_config_path, config_file), os.path.join(config_path, config_file))

    def update_sub(self, url, path):
        content = self.get_sub_content(url)
        if not content:
            print(f'未获取到订阅内容[{url}]：'
                  f'{content}')
            exit()
        print(f'获取订阅内容[{url}]:')
        share_links = b64decode(content).decode('utf-8').splitlines()
        unknown_node_count = 1
        sub_tmp_path = os.path.join(self.tmp_path, path)
        if not os.path.exists(sub_tmp_path):
            os.makedirs(sub_tmp_path)
        for share_link in share_links:
            try:
                config = self.parse_config(share_link)
                name = config.get('ps', None)
                if not name:
                    name = f'未知节点_{unknown_node_count}'
                    unknown_node_count += 1
                file_path = os.path.join(sub_tmp_path, 'v2ray-config-' + name + '.json')
                BaseConfig(config['add'], int(config['port']), config['id'], alter_id=int(config['aid']),
                           path=config['path']).save(file_path)
                print(f'添加节点配置-{name}')
            except Exception as e:
                msg = f'解析订阅异常：\n{e}'
                if self.settings['strict']:
                    raise RuntimeError(msg)
                else:
                    print(msg)

    def parse_config(self, share_link):
        url = urlsplit(share_link)
        if url.scheme not in self.schemes_allow:
            raise RuntimeError(f'无效的分享链接：\n{url}')
        netloc = url.netloc + url.path
        netloc_len = len(netloc)
        if netloc_len % 4 > 0:
            netloc += '=' * (4 - netloc_len % 4)
        config = b64decode(netloc).decode('utf-8')
        return json.loads(config)

    def get_subs(self, except_invalid=True, hide_secret=True):
        if except_invalid:
            return list(filter(lambda x: x.status, self.settings.subs))
        else:
            return self.settings.subs

    def get_configs(self):
        out_configs = {'默认节点': []}
        config_paths = os.listdir(self.settings.configs_path)
        for config_path in config_paths:
            p = os.path.join(self.settings.configs_path, config_path)
            if os.path.isfile(p):
                if p.endswith('.json'):
                    out_configs['默认节点'].append(p)
            else:
                configs = os.listdir(p)
                out_configs[config_path] = []
                for c in configs:
                    pp = os.path.join(p, c)
                    if os.path.isfile(pp) and pp.endswith('.json'):
                        out_configs[config_path].append(pp)
        filter_out = {}
        for k, v in out_configs.items():
            if len(v) > 0:
                filter_out[k] = v
        return filter_out

    def configs_list(self):
        configs = self.get_configs()
        list_str = ''
        num = 1
        configs_list = []
        for name, config in configs.items():
            list_str += name + '\n'
            list_str += f'{"ID":>6}' + '\t' * 2 + '配置文件名\n'
            for c in config:
                configs_list.append(c)
                list_str += f'{num:>6}' + '\t' * 2 + f'{os.path.split(c)[-1]}\n'
                num += 1
        return list_str, configs_list

    def __del__(self):
        if hasattr(self, 'tmp_path') and os.path.exists(self.tmp_path):
            shutil.rmtree(self.tmp_path)

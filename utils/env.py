import datetime
import os
import random
import shutil
import subprocess
import time


def source_env(cmd, interpreter='#!/bin/bash'):

    tmp_path = f"/tmp/tmp_for_source"
    file_name = f"tmp_for_source_{datetime.datetime.now().strftime(f'%Y%m%d%H%M%S%f_{random.randint(1000, 9999)}')}"
    file_path = os.path.join(tmp_path, file_name)
    print(file_path)
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)
    with open(file_path, 'w', encoding='UTF-8') as f:
        content = f'{interpreter}\n{cmd}'
        f.write(content)
    print(os.listdir(tmp_path))
    # subprocess.run(f'source {file_path}', shell=True)
    # shutil.rmtree(file_path)


def set_proxy(port):
    cmd = f'export http_proxy=http://127.0.0.1:{port}/\n' \
          f'export https_proxy=http://127.0.0.1:{port}/\n'
    source_env(cmd)


if __name__ == '__main__':
    set_proxy(10810)
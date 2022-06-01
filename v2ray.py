import subprocess
from typing import TYPE_CHECKING
import psutil
if TYPE_CHECKING:
    from manager import V2rayManager


class V2ray:

    def __init__(self, manager: 'V2rayManager'):
        self.manager = manager
        self.settings = manager.settings

    def start(self, config=None):
        log_path = '/etc/v2ray/access.log'
        cmd = f'nohup v2ray -config {self.settings.default_config if config is None else config} > {log_path} 2>&1 &'
        subprocess.run(cmd, shell=True)
        print(cmd)
        print('已启动v2ray\n')

    def stop(self):
        self.kill_processes()
        print('停止v2ray\n')

    def restart(self, config=None):
        self.stop()
        self.start(config)

    def speed_test(self, configs=None):
        ...

    @staticmethod
    def get_processes():
        pids = psutil.pids()
        v2ray_p = []
        for pid in pids:
            p = psutil.Process(pid)
            if p.name() == 'v2ray':
                v2ray_p.append(p)
        return v2ray_p

    def list_processes(self):
        processes = self.get_processes()
        if not processes:
            print('无进程')
            return
        for process in processes:
            print(f'[{process}]{process.cmdline()}')

    def kill_processes(self, ps: list[int] = None):
        processes = self.get_processes()
        if not processes:
            print('无进程')
            return
        for process in processes:
            if ps:
                if process.pid not in list(map(lambda x: int(x), ps)):
                    continue
            cmd = process.cmdline()
            process.kill()
            print(f'终止进程[{process.pid}][{process}][{cmd}]')
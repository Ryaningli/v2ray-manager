import json
import os


class BaseConfig:

    def __init__(self, address, port, user_id, alter_id=0):
        self.base_config = {
            "inbounds": [
                {
                    "port": 10809,
                    "listen": "127.0.0.1",
                    "protocol": "socks",
                    "sniffing": {
                        "enabled": True,
                        "destOverride": ["http", "tls"]
                    },
                    "settings": {
                        "auth": "noauth",
                        "udp": True
                    }
                },
                {
                    "port": 10810,
                    "listen": "127.0.0.1",
                    "protocol": "http",
                    "sniffing": {
                        "enabled": True,
                        "destOverride": ["http", "tls"]
                    },
                    "settings": {
                        "auth": "noauth",
                        "udp": True
                    }
                }
            ],
            "outbounds": [
                {
                    "protocol": "vmess",
                    "settings": {
                        "vnext": [
                            {
                                "address": address,
                                "port": port,
                                "users": [
                                    {
                                        "id": user_id,
                                        "alterId": alter_id
                                    }
                                ]
                            }
                        ]
                    }
                }
            ]
        }

    def to_json(self):
        return json.dumps(self.base_config)

    def save(self, path):
        with open(path, 'w', encoding='UTF-8') as f:
            json.dump(self.base_config, f, indent=2, sort_keys=True, ensure_ascii=False)

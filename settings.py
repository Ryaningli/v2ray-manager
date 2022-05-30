from utils.dot_dict import DotDict


class Settings(DotDict):
    configs_path: str

    class Port(DotDict):
        sock: int
        http: int

    port: Port

    class Subs(DotDict):
        name: str
        path: str
        url: str
        status: bool

    subs: list[Subs]

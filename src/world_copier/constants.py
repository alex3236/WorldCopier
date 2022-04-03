from typing import List, Union
from mcdreforged.api.utils.serializer import Serializable
from mcdreforged.api.types import ServerInterface

class Configure(Serializable):
    command: str = '!!sync'
    permission: int = 0
    source_path: str = '/foo/bar/qb_multi/slot1'
    world_list: List[str] = ['world']
    server_path: str = './server'
    backup: bool = False
    backup_path: str = './sync_backup'
    timed_sync: int = -1
    ignored_files: List[str] = ['seesion.lock']

psi = ServerInterface.get_instance().as_plugin_server_interface()
import os
import time
from mcdreforged.api.all import *
from world_copier.constants import Configure, psi
import shutil

config: Configure
abort = False
flag = False
unloaded = False

def brodcast(src: CommandSource, msg):
    psi.say(msg)
    if src.is_console:
        src.reply(msg)

def is_file_ignored(file_name: str) -> bool:
    for item in config.ignored_files:
        if len(item) > 0:
            if item[0] == '*' and file_name.endswith(item[1:]):
                return True
            if item[-1] == '*' and file_name.startswith(item[:-1]):
                return True
            if file_name == item:
                return True
    return False

def remove_worlds(folder: str):
	for world in config.world_list:
		target_path = os.path.join(folder, world)

		while os.path.islink(target_path):
			link_path = os.readlink(target_path)
			os.unlink(target_path)
			target_path = link_path if os.path.isabs(link_path) else os.path.normpath(os.path.join(os.path.dirname(target_path), link_path))

		if os.path.isdir(target_path):
			shutil.rmtree(target_path)
		elif os.path.isfile(target_path):
			os.remove(target_path)
		else:
			psi.logger.warning('[WorldCopier] {} does not exist while removing'.format(target_path))

def copy_worlds(src: str, dst: str):
	for world in config.world_list:
		src_path = os.path.join(src, world)
		dst_path = os.path.join(dst, world)

		while os.path.islink(src_path):
			psi.logger.info('Copying {} -> {} (symbolic link)'.format(src_path, dst_path))
			dst_dir = os.path.dirname(dst_path)
			if not os.path.isdir(dst_dir):
				os.makedirs(dst_dir)
			link_path = os.readlink(src_path)
			os.symlink(link_path, dst_path)
			src_path = link_path if os.path.isabs(link_path) else os.path.normpath(os.path.join(os.path.dirname(src_path), link_path))
			dst_path = os.path.join(dst, os.path.relpath(src_path, src))

		psi.logger.info('Copying {} -> {}'.format(src_path, dst_path))
		if os.path.isdir(src_path):
			shutil.copytree(src_path, dst_path, ignore=lambda path, files: set(filter(is_file_ignored, files)))
		elif os.path.isfile(src_path):
			dst_dir = os.path.dirname(dst_path)
			if not os.path.isdir(dst_dir):
				os.makedirs(dst_dir)
			shutil.copy(src_path, dst_path)
		else:
			psi.logger.warning('{} does not exist while copying ({} -> {})'.format(src_path, src_path, dst_path))

@new_thread('world_copier')
def sync(src: CommandSource):
    global abort, flag
    flag = True
    for i in range(1, 10)[::-1]:
        brodcast(src, psi.tr('world_copier.countdown', i, config.command))
        if abort:
            abort = False
            brodcast(src, psi.tr('world_copier.aborted', config.command))
            return
        time.sleep(1)
    try:
        brodcast(src, psi.tr('world_copier.sync'))
        time.sleep(0.7)
        psi.stop()
        psi.logger.info('Wait for server to stop')
        psi.wait_for_start()
        if config.backup:
            psi.logger.info('Backup current world to avoid idiot')
            overwrite_backup_path = config.backup_path
            if os.path.exists(overwrite_backup_path):
                shutil.rmtree(overwrite_backup_path)
            copy_worlds(config.sever_path, overwrite_backup_path)
        psi.logger.info('Deleting world')
        remove_worlds(config.server_path)
        psi.logger.info('Syncing ' + config.source_path + ' -> ' + config.server_path)
        copy_worlds(config.source_path, config.server_path)
        psi.start()
    except:
        psi.logger.exception('Failed to sync server worlds.')
    finally:
        abort = False
        flag = False

def do_abort(src):
    global abort
    if flag:
        abort = True

@new_thread('world_copier_clock')
def timed_sync():
    for i in range(config.timed_sync*60):
        if unloaded:
            return
        time.sleep(1)
    sync(psi.get_plugin_command_source())


def on_load(server: PluginServerInterface, prev):
    global config
    config = server.load_config_simple('config.json', target_class=Configure)
    server.register_command(Literal(config.command).runs(sync).then(Literal('abort').runs(do_abort)))
    if config.timed_sync >= 1:
        timed_sync()
        server.logger.info(server.tr('world_copier.timer', config.timed_sync))

def on_unload(foo):
    global unloaded, abort
    abort = True
    unloaded = True
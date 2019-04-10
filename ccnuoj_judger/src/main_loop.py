import os
import requests
import traceback
from time import sleep

from .global_object import session, config
from .webapi import get_fetched_command, get_unfetched_command
from .command import execute_command_list


data_subfolder_names = ['judge-data', 'judge-request']


def init(config_module):
    config_key_names = [
        "data_folder",
        "default_folder_mode",
        "default_file_mode",
        "sandbox_command",
        "api_base",
        "token"
    ]
    for key_name in config_key_names:
        value = getattr(config_module, key_name)
        config[key_name] = value

    session.headers.update({"X-CCNU-AUTH-TOKEN": config["token"]})


def prepare_data_folder():
    if not os.path.exists(config['data_folder']):
        os.mkdir(config['data_folder'], mode=config['default_folder_mode'])
    for subfolder_name in data_subfolder_names:
        subfolder_path = '%s/%s' % (config['data_folder'], subfolder_name)
        if not os.path.exists(subfolder_path):
            os.mkdir(subfolder_path, mode=config['default_folder_mode'])


def main_loop_internal():
    prepare_data_folder()

    print("Recovering...")
    fetched_command_list = get_fetched_command()
    execute_command_list(fetched_command_list)

    while True:
        sleep(1)

        unfetched_command_list = get_unfetched_command(5)
        execute_command_list(unfetched_command_list)


def main_loop():
    while True:
        try:
            sleep(2)
            main_loop_internal()
        except requests.RequestException:
            print("Network Error:")
            print(traceback.format_exc())
        except Exception:
            print("Unknown Error:")
            print(traceback.format_exc())

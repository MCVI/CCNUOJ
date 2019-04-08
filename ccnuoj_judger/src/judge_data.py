import io
import os
import shutil
import zipfile

from .global_object import config
from .webapi import JudgeDataNotUploaded
from .webapi import get_judge_data_info, download_judge_data


def prepare_judge_data(problem_id: int, judge_data_folder: str):
    if os.path.exists(judge_data_folder + '/prepare_accomplished'):
        return
    else:
        get_judge_data_info(problem_id)

        if os.path.exists(judge_data_folder):
            shutil.rmtree(judge_data_folder)

        os.makedirs(
            judge_data_folder,
            mode=config['default_folder_mode'],
            exist_ok=True
        )

        judge_data = download_judge_data(problem_id)
        archived_path = '%s/archived' % (judge_data_folder, )
        with open(archived_path, 'wb') as file:
            file.write(judge_data)

        archived_file = zipfile.ZipFile(archived_path)
        archived_file.extractall('%s/extracted'  % (judge_data_folder, ))

        with open(judge_data_folder + '/prepare_accomplished', 'w'):
            pass

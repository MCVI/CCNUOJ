import os
import json
import shutil

from .common import JudgeState
from .global_object import config
from .webapi import get_submission
from .webapi import get_problem
from .webapi import update_judge_request_state
from .judge_data import JudgeDataNotUploaded
from .judge_data import prepare_judge_data


def do_judge(judge_request: dict):
    judge_request_id = judge_request['id']
    update_judge_request_state(judge_request_id, JudgeState.pending)

    submission_id = judge_request['submission']
    submission = get_submission(submission_id)
    problem_id = submission['problem']['id']

    judge_data_folder = '%s/judge-data/%d' % (config['data_folder'], problem_id)
    prepare_judge_data(problem_id, judge_data_folder)
    with open('%s/extracted/settings.json' % (judge_data_folder,)) as settings_file:
        settings_str = settings_file.read()

    judge_request_folder = '%s/judge-request/%d' % (config['data_folder'], judge_request['id'])
    if os.path.exists(judge_request_folder):
        shutil.rmtree(judge_request_folder)
    os.mkdir(judge_request_folder, mode=config['default_folder_mode'])

    source_file_path = '%s/submission-%d.cpp' % (judge_request_folder, submission_id)
    with open(source_file_path, mode='wt') as source_file:
        source_file.write(submission['text'])
    settings = json.loads(settings_str)

    problem = get_problem(problem_id)
    if problem['judgeScheme'] == 'SimpComp':
        exe_file_path = '%s/submission-%d' % (judge_request_folder, submission_id)

        update_judge_request_state(judge_request_id, JudgeState.compiling)
        compile_command = 'g++ -O3 -o {output} {source} -lm'.format(
            source=source_file_path,
            output=exe_file_path
        )
        os.system(compile_command)
        if not os.path.exists(exe_file_path):
            update_judge_request_state(judge_request_id, JudgeState.compileError)
            return

        update_judge_request_state(judge_request_id, JudgeState.running)

        for (testcase_name, testcase) in settings['testcases'].items():
            testcase_folder = '%s/%s' % (judge_request_folder, testcase_name)
            os.mkdir(testcase_folder)

            input_path = '%s/extracted/%s' % (judge_data_folder, testcase['input'])
            output_path = '%s/output.txt' % (testcase_folder, )

            ret_num = os.system('./{program} <{input} >{output}'.format(
                program=exe_file_path,
                input=input_path,
                output=output_path
            ))
            if ret_num != 0:
                update_judge_request_state(judge_request_id, JudgeState.runtimeError)
                return

            answer_path = '%s/extracted/%s' % (judge_data_folder, testcase['answer'])
            diff_status = os.system('diff -q {output} {answer}'.format(output=output_path, answer=answer_path))
            if diff_status != 0:
                update_judge_request_state(judge_request_id, JudgeState.wrongAnswer)
                return

        update_judge_request_state(judge_request_id, JudgeState.accepted)
        return

    else:
        raise NotImplementedError()

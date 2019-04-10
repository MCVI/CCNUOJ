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
from .diff import diff_ignore_all_space, diff_ignore_trailing
from .sandbox_driver import sandbox_run_stdio


judge_state_severe_order = [
    JudgeState.accepted,
    JudgeState.presentationError,
    JudgeState.wrongAnswer,
    JudgeState.timeLimitExceeded,
    JudgeState.memoryLimitExceeded,
    JudgeState.runtimeError,
]


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

        most_severe_state = judge_state_severe_order[0]
        for (testcase_name, testcase) in settings['testcases'].items():
            testcase_folder = '%s/%s' % (judge_request_folder, testcase_name)
            os.mkdir(testcase_folder)

            input_path = '%s/extracted/%s' % (judge_data_folder, testcase['input'])
            output_path = '%s/stdout.txt' % (testcase_folder, )
            error_path = '%s/stderr.txt' % (testcase_folder, )

            run_result = sandbox_run_stdio(
                sandbox_file_path=testcase_folder,
                program_path=exe_file_path,
                time_limit=1000,
                memory_limit=134217728,
                stdio_redirection={
                    'stdin': input_path,
                    'stdout': output_path,
                    'stderr': error_path,
                },
            )
            if 'ProgramExited' in run_result['category']:
                if run_result['detail']['ret'] == 0:
                    with open(output_path, 'rt') as file:
                        output_content = file.read()

                    answer_path = '%s/extracted/%s' % (judge_data_folder, testcase['answer'])
                    with open(answer_path, 'rt') as file:
                        answer_content = file.read()

                    if diff_ignore_trailing(output_content, answer_content):
                        testcase_state = JudgeState.accepted
                    else:
                        if diff_ignore_all_space(output_content, answer_content):
                            testcase_state = JudgeState.presentationError
                        else:
                            testcase_state = JudgeState.wrongAnswer
                else:
                    testcase_state = JudgeState.runtimeError
            elif 'TimeLimitExceeded' in run_result['category']:
                testcase_state = JudgeState.timeLimitExceeded
            elif 'MemoryLimitExceeded' in run_result['category']:
                testcase_state = JudgeState.memoryLimitExceeded
            else:
                testcase_state = JudgeState.runtimeError

            if judge_state_severe_order.index(testcase_state) > judge_state_severe_order.index(most_severe_state):
                most_severe_state = testcase_state
            if most_severe_state == judge_state_severe_order[-1]:
                break

        update_judge_request_state(judge_request_id, most_severe_state)
        return

    else:
        raise NotImplementedError()

import json

from .common import JudgeState
from .global_object import session, config


class RequestFailed(Exception):
    pass


class JudgeDataNotUploaded(RequestFailed):
    pass


def get_fetched_command() -> list:
    api_url = config["api_base"] + "/judge_command/fetched/all"
    result = session.get(api_url).json()
    if result["status"] != "Success":
        raise RequestFailed()
    else:
        return result["result"]


def get_unfetched_command(num: int) -> list:
    api_url = config["api_base"] + "/judge_command/unfetched/%d" % num
    result = session.get(api_url).json()
    if result["status"] != "Success":
        raise RequestFailed()
    else:
        return result["result"]


def mark_judge_command_fetched(command_id: int) -> None:
    api_url = config["api_base"] + '/judge_command/%d/fetched' % command_id
    result = session.post(api_url).json()
    if result["status"] != "Success":
        raise RequestFailed()
    else:
        return


def mark_judge_command_finished(command_id: int, result=None) -> None:
    api_url = '%s/judge_command/%d/finished' % (config['api_base'], command_id)
    response = session.post(api_url, json={
        "result": result,
    }).json()
    if response['status'] != 'Success':
        raise RequestFailed()
    else:
        return


def get_judge_request(judge_request_id: int) -> dict:
    api_url = config["api_base"] + '/judge_request/id/%d' % judge_request_id
    result = session.get(api_url).json()
    if result["status"] != "Success":
        raise RequestFailed()
    else:
        return result["result"]


def get_submission(submission_id: int) -> dict:
    api_url = config["api_base"] + '/submission/id/%d' % submission_id
    result = session.get(api_url).json()
    if result["status"] != "Success":
        raise RequestFailed()
    else:
        return result["result"]


def get_problem(problem_id: int) -> dict:
    api_url = '%s/problem/id/%d' %(config['api_base'], problem_id)
    result = session.get(api_url).json()
    if result['status'] == 'Success':
        return result['result']
    else:
        raise RequestFailed()


def get_judge_data_info(problem_id: int) -> dict:
    api_url = '%s/problem/id/%d/judge_data/resolved' % (config['api_base'], problem_id)
    result = session.get(api_url).json()
    if result['status'] == 'Success':
        return result['result']
    else:
        if result['reason'] == 'JudgeDataNotUploaded':
            raise JudgeDataNotUploaded()
        else:
            raise RequestFailed()


def download_judge_data(problem_id: int) -> bytes:
    api_url = '%s/problem/id/%d/judge_data/raw' % (config['api_base'], problem_id)
    result = session.get(api_url)
    if result.status_code == 200:
        return result.content
    else:
        raise RequestFailed()


def update_judge_request_state(judge_request_id: int, state: JudgeState, detail=None):
    api_url = '%s/judge_request/id/%d/state' % (config['api_base'], judge_request_id)
    result = session.put(api_url, json={
        "state": state.name,
        "detail": detail
    }).json()
    if result['status'] == 'Success':
        return
    else:
        raise RequestFailed()


def mark_judge_request_finished(judge_request_id: int) -> None:
    api_url = '%s/judge_request/id/%d/finished' % (config['api_base'], judge_request_id)
    result = session.post(api_url).json()
    if result['status'] != 'Success':
        raise RequestFailed()
    else:
        return

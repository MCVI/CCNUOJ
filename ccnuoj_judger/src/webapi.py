from .global_object import session, config


class RequestFailed(Exception):
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


def mark_judge_command_finished(command_id: int) -> None:
    api_url = config["api_base"] + '/judge_command/%d/finished' % command_id
    result = session.post(api_url).json()
    if result["status"] != "Success":
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

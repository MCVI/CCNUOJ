from .webapi import get_submission


def do_judge(judge_request: dict):
    submission = get_submission(judge_request["submission"])
    print(submission)
    raise NotImplementedError()

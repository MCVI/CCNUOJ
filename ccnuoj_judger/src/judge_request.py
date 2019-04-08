from .webapi import get_judge_request
from .webapi import mark_judge_request_finished
from .judge import do_judge


def judge_request_handler(command: dict):
    judge_request_id = command["judgeRequestID"]
    judge_request = get_judge_request(judge_request_id)

    if judge_request["finishTime"] is None:
        do_judge(judge_request)
        mark_judge_request_finished(judge_request_id)
    else:
        print("JudgeRequest #%d already finished")

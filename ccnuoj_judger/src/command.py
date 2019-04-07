from .webapi import mark_judge_command_fetched, mark_judge_command_finished
from .judge_request import judge_request_handler


command_handlers = {
    "JudgeRequest": judge_request_handler,
}


def dispatch_command(command: dict):
    handler = command_handlers[command["type"]]
    result = handler(command)
    mark_judge_command_finished(command["id"])
    return result


def execute_command_list(command_list: list):
    for command in command_list:
        if command["fetchTime"] is None:
            mark_judge_command_fetched(command["id"])
        print("Successfully fetched judge command #%d: %s" % (command["id"], command["command"]))
        dispatch_command(command["command"])

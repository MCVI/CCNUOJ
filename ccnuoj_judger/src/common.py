from enum import Enum


class JudgeState(Enum):
    waiting = 'WAIT'
    pending = 'PEND'

    compiling = 'CMPL'
    compileError = 'CE'
    compileTimeLimitExceeded = 'CTLE'

    running = 'RUN'
    runtimeError = 'RE'
    timeLimitExceeded = 'TLE'
    memoryLimitExceeded = 'MLE'
    outputLimitExceeded = 'OLE'

    comparing = 'CMPR'

    accepted = 'AC'
    wrongAnswer = 'WA'
    presentationError = 'PE'

    systemError = 'SYSE'

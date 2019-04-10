import os
import json

from .global_object import config


class SandboxError(Exception):
    pass


def generate_config(
        sandbox_output: str,
        program_path: str,
        time_limit: int,
        memory_limit: int,
        file: dict,
        stdio_redirection: dict,
):
    return {
        "sandboxOutput": sandbox_output,

        "programPath": program_path,

        "timeLimit": time_limit,
        "memoryLimit": memory_limit,

        "file": dict(**{
            "/etc/ld.so.cache": ["read"],
            "/usr/lib/*": ["read"],
        }, **file),

        "stdioRedirection": stdio_redirection,

        "syscall": {
            "allow": [
                "arch_prctl",
                "exit_group",

                "brk",
                "mmap",
                "munmap",
                "mprotect",

                "access",
                "openat",
                "close",

                "read",
                "write",
                "lseek",
                "fstat"
            ]
        }
    }


def sandbox_run_stdio(
        sandbox_file_path: str,
        program_path: str,
        time_limit: int,
        memory_limit: int,
        stdio_redirection: dict,
):
    permission_table = {
        'stdin': ['read'],
        'stdout': ['create', 'read', 'write'],
        'stderr': ['create', 'read', 'write'],
    }
    stdio_name_map = {
        'stdin': 'stdin',
        'in': 'stdin',

        'stdout': 'stdout',
        'out': 'stdout',

        'stderr': 'stderr',
        'err': 'stderr',
        'error': 'stderr',
    }

    file_whitelist = {}

    for (stdio_name, path) in stdio_redirection.items():
        formal_name = stdio_name_map[stdio_name]
        permission = permission_table[formal_name]
        if path in file_whitelist:
            old_permission = file_whitelist[path]
            file_whitelist[path] = list(set(old_permission)|set(permission))
        else:
            file_whitelist[path] = permission

    sandbox_output_file_path = '%s/sandbox_output.json' % (sandbox_file_path, )

    config_json = generate_config(
        sandbox_output=sandbox_output_file_path,
        program_path=program_path,
        time_limit=time_limit,
        memory_limit=memory_limit,
        file=file_whitelist,
        stdio_redirection=stdio_redirection,
    )

    sandbox_config_file_path = '%s/sandbox_config.json' % (sandbox_file_path, )
    with open(sandbox_config_file_path, 'wt') as file:
        file.write(json.dumps(config_json))

    sandbox_ret = os.system('%s %s' % (config['sandbox_command'], sandbox_config_file_path))
    '''
    if sandbox_ret != 0:
        raise SandboxError()
    '''

    with open(sandbox_output_file_path, 'rt') as file:
        sandbox_output = json.loads(file.read())

    return sandbox_output

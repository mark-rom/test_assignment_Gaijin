import argparse
import importlib.util
import os
import sys

from typing import List


def find_py_files(path_to_dir: str) -> List[str]:
    py_files = []

    def recurse_dir(current_dir):
        for entry in os.listdir(current_dir):
            path = os.path.join(current_dir, entry)
            if os.path.isdir(path):
                recurse_dir(path)
            elif entry.endswith('.py'):
                py_files.append(path)

    recurse_dir(path_to_dir)
    return py_files


def execute_cmds_from_file(file_path: str, executed_commands: List):
    spec = importlib.util.spec_from_file_location("current_module", file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["current_module"] = module
    spec.loader.exec_module(module)

    try:
        cmds = module.CMDS
    except AttributeError:
        return

    for command in cmds:
        if command in executed_commands:
            print(f"команда {command} уже исполнялась")
        else:
            os.system(command)
            executed_commands.append(command)

    sys.modules.pop("current_module")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('directory')
    args = parser.parse_args()

    executed_commands = []
    py_files = find_py_files(args.directory)
    py_files.sort()

    for py_file in py_files:
        execute_cmds_from_file(py_file, executed_commands)

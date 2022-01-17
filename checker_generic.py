"""CSC108: Fall 2021 -- Assignment 2: Simulating Canadian Elections

This code is provided solely for the personal and private use of students 
taking the CSC108 course at the University of Toronto. Copying for purposes 
other than this use is expressly prohibited. All forms of distribution of 
this code, whether as given or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Michelle Craig, Tom Fairgrieve, Sadia Sharmin, and 
Jacqueline Smith.
"""

import sys
import subprocess
import importlib
from typing import Tuple
from copy import deepcopy

PYTHON_TA_VERSION = '2.1.1'
TYPE_ERROR_MSG = '{} should return a {}, but returned {}.'


def attempt_python_ta_installation(version: int) -> int:
    """Attempt installation of PythonTA.
    Returns the next version to attempt if there is one, or -1 if there
    are no other versions after version.
    """
    executables = ['python3.9', sys.executable]
    attempts = [f'-m pip install python-ta=={PYTHON_TA_VERSION}',
                # Turn off SSL verification (certificate errors)
                f'-m pip install python-ta=={PYTHON_TA_VERSION} '
                f'config --global http.sslVerify false',
                # Set pypi as a trusted host
                f'-m pip install python_ta=={PYTHON_TA_VERSION} '
                f'--trusted-host pypi.python.org'
                ]

    try:
        # Switch between python3.9 and sys.executable
        executable = executables[version % 2]
        attempt = attempts[version // 2]

        # python3.9 uses Popen, while sys.executable uses check_call
        if executable == 'python3.9':
            subprocess.Popen(executable + ' ' + attempt,
                             shell=True,
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
        else:
            subprocess.check_call([executable] + attempt.split(),
                                  stderr=subprocess.DEVNULL,
                                  stdout=subprocess.DEVNULL)
    except:
        pass

    if version < len(attempts) * 2:
        return version + 1

    return -1


def python_ta_installed() -> bool:
    """Return True if PythonTA is installed."""
    try:
        if 'python_ta' in sys.modules:
            del sys.modules['python_ta']

        import python_ta
        importlib.reload(python_ta)
        installed_version = python_ta.__version__
        return installed_version == PYTHON_TA_VERSION
    except:
        return False


def install_python_ta():
    """Tries to install PythonTA."""
    if not python_ta_installed():
        print("Installing / Updating the style checker", end='')

    i = 0
    while not python_ta_installed() and i != -1:
        print(".", end='')
        i = attempt_python_ta_installation(i)

    print("")


def run_pyta(filename: str, config_file: str) -> None:
    """Run PYTA with configuration config_file on the file named filename.
    """
    import json
    install_python_ta()

    error_message = '\nCould not install or run the style checker correctly.\n' \
                    'Please try to re-run the checker once.\n' \
                    'If you have already tried to re-run it, please go to office hours\n' \
                    'in order to resolve this. ' \
                    'For now, you may upload your code to MarkUs and run the self-test\n' \
                    'to see the style checker results.'

    try:
        import python_ta
        with open(config_file) as cf:
            config_dict = json.loads(cf.read())
            config_dict['output-format'] = 'python_ta.reporters.PlainReporter'

        python_ta.check_all(filename, config=config_dict)
    except:
        print(error_message)


def type_check_simple(func: callable, args: list,
                      expected: type) -> Tuple[bool, object]:
    """Check if func(args) returns a result of type expected.

    Return (True, result-of-call) if the check succeeds.
    Return (False, error-or-failure-message) if anything goes wrong.
    """

    try:
        args_copy = deepcopy(args)
        returned = func(*args_copy)
    except Exception as exn:
        return (False, error_message(func, args, exn))

    if isinstance(returned, expected):
        return (True, returned)

    return (False,
            type_error_message(func.__name__, expected.__name__, returned))


def type_check_full(func: callable, args: list,
                    checker_function: callable) -> Tuple[bool, object]:
    """Run checker_function on func(args).

    Pre: checker_function is also a type-checker (i.e. returns tuple
          in the same format).

    Return (True, result-of-call-func-args) if the check succeeds.
    Return (False, error-or-failure-message) if anything goes wrong.
    """

    try:
        args_copy = deepcopy(args)
        returned = func(*args_copy)
    except Exception as exn:
        return (False, error_message(func, args, exn))

    return checker_function(returned)


def type_error_message(func: str, expected: str, got: object) -> str:
    """Return an error message for function func returning got, where the
    correct return type is expected.

    """

    return TYPE_ERROR_MSG.format(func, expected, got)


def error_message(func: callable, args: list,
                  error: Exception) -> str:
    """Return an error message: func(args) raised an error."""

    return 'The call {}({}) caused an error: {}'.format(
        func.__name__, ','.join(map(repr, args)), error)


def returns_list_of_Ts(func: callable, args: list, tp: type):
    """Check if func(args) returns a list of elements of type tp.

    Return (True, result-of-call) if the check succeeds.
    Return (False, error-or-failure-message) if anything goes wrong.

    """

    result = type_check_simple(func, args, list)
    if not result[0]:
        return (False, result[1])

    msg = type_error_message(func.__name__, 'list of {}s'.format(tp.__name__),
                             result[1])
    for item in result[1]:
        if not isinstance(item, tp):
            return (False, msg)

    return (True, result[1])


def _mock_disallow(func_name: str):
    """Raise an Exception saying that use of function func_name is not
    allowed.

    """

    def mocker(*args):
        raise Exception(
            "The use of function {} is not allowed.".format(func_name))

    return mocker

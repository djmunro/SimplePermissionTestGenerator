__author__ = 'DMunro'
import re


def trim_method(method):
    """
    Returns method name with parameters
    e.g. method public boolean className(arg1, arg2) -> className(arg1, arg2)
    """
    match = re.search(r'\w+\((.+)\)|\w+\(()\)', method)

    if match:
        return match.group()


def parameter_string(parameter_string):
    match = re.search(r'\((.+)\)', parameter_string)
    if match:
        return match.group()
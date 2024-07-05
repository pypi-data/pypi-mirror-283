#!/usr/bin/python
"""
@Author  :  Lijiawei
@Date    :  2023/11/6 3:10 PM
@Desc    :  error line.
"""


class BaseError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class UTXError(BaseError):
    """
    This is UTX BaseError
    """


class InvalidMatchingMethodError(BaseError):
    """
    This is InvalidMatchingMethodError BaseError
    When an invalid matching method is used in settings.
    """


class TargetNotFoundError(UTXError):
    """
    This is TargetNotFoundError BaseError
    When something is not found
    """


class ScriptParamError(UTXError):
    """
    This is ScriptParamError BaseError
    When something goes wrong
    """

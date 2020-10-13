# coding : utf-8
import os
import typing

__version__ = "0.0.1b"
PACKAGE_DIR = os.path.abspath(os.path.dirname(__file__))


def clean_logs(data_path: typing.Optional[str] = None, include_current: bool = False):
    """
    TODO
    :param data_path:
    :param include_current:
    :return:
    """

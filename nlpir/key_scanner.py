#! coding=utf-8
"""
high-level toolbox for Chinese Key-word Extraction
"""
# pylint: disable=duplicate-code

from nlpir import get_instance as __get_instance__
from nlpir import native
import typing

# class and class instance
__cls__ = native.key_scanner.KeyScanner
__instance__: typing.Optional[native.key_scanner.KeyScanner] = None
# Location of DLL
__lib__ = None
# Data directory
__data__ = None
# license_code
__license_code__ = None
# encode
__nlpir_encode__ = native.UTF8_CODE


@__get_instance__
def get_native_instance() -> native.key_scanner.KeyScanner:
    """
    返回原生NLPIR接口,使用更多函数

    :return: The singleton instance
    """
    return __instance__


class KeyScanProcessor:
    @__get_instance__
    def __init__(self):
        self.handle = __instance__.new_instance()

    @__get_instance__
    def __del__(self):
        return __instance__.delete_instance(self.handle)

    def import_user_dict(
            self,
            filename: str,
            pinyin_abbrev_needed: bool = False,
            over_write: bool = False,
    ):
        return __instance__.import_user_dict(filename, pinyin_abbrev_needed, over_write, self.handle)

    def delete_user_dict(
            self,
            filename: str
    ):
        return __instance__.delete_instance(filename, self.handle)

    def scan(self, text: str):
        return __instance__.scan(text, self.handle)


def __user_dict2str(user_dict: typing.List) -> str:
    user_dict = [" ".join(user_dict_item) for user_dict_item in user_dict]
    user_dict = "\n".join(user_dict)
    return user_dict


@__get_instance__
def import_user_dict(user_dict: typing.List, pinyin_abbrev_needed: bool = True, over_write: bool = False) -> bool:
    handle = __instance__.new_instance()
    __instance__.import_user_dict(__user_dict2str(user_dict), pinyin_abbrev_needed, over_write)
    __instance__.delete_instance(handle)
    return True


@__get_instance__
def delete_user_dict(user_dict: typing.List) -> bool:
    handle = __instance__.new_instance()
    __instance__.delete_user_dic(__user_dict2str(user_dict))
    __instance__.delete_instance(handle)
    return True

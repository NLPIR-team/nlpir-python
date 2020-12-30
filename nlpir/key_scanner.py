#! coding=utf-8
"""
high-level toolbox for Chinese Key-word Extraction
"""
# pylint: disable=duplicate-code

from nlpir import get_instance as __get_instance__
from nlpir import native
import typing
import re
import json

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
    """
    关键词过滤处理单元, 需要指定使用的过滤器, 若要新建
    一过滤器, 选择没有被使用的编号实例化本类, 并使用
    :func:`import_user_dict` 导入词典后便可使用,下次使用时仅需
    实例化对应编号的本类即可.

    导入词典后的过滤器会保存在Data文件夹下,若不删除则会一直存在,和导入
    用户词典相似,不会消失.

    :param filter_type_index: 需要使用的过滤器

    """

    @__get_instance__
    def __init__(self, filter_type_index: int = 0):
        self.handle = __instance__.new_instance(filter_type_index=filter_type_index)

    @__get_instance__
    def __del__(self):
        __instance__.delete_instance(self.handle)

    def scan(self, text: str):
        """
        Scan text

        :param text:
        :return:

        ::

            [
                {
                    "class": class_name,
                    "freq": frequent_of_class_hit
                },{
                    ...
                },
                ...
            ]

        """
        result = __instance__.scan(text, self.handle)
        result = re.findall(r"(.+?)/(\d+)#", result)
        return [{"class": _[0], "freq": _[1]} for _ in result]

    def scan_detail(self, text: str):
        """
        Scan text get detail

        ::

            {
                'Rules': ['傻逼'],
                'illegal':{
                    'classes': [
                        {'freq': 1, 'word': '粗言秽语'},
                        {'freq': 1, 'word': '污言秽语'},
                        {'freq': 1, 'word': '新华社禁用'}
                    ],
                    'hit_count': 3,
                    'keys': ['傻逼'],
                    'scan_val': 3.333333333333333
                },
                'line_id': 0,
                'org_file': '',
                'score': 3.333333333333333
            }
        :param text:
        :return:

        """
        result = __instance__.scan_detail(text, handle=self.handle)
        result = json.loads(result) if len(result) > 2 else dict()
        result["rules"] = result.pop("Rules", None)
        result.pop("Details", None)
        result.pop("filename", None)
        result.pop("legal", None)
        return result


@__get_instance__
def import_user_dict(
        user_dict: str,
        filter_index: int = 0,
        pinyin_abbrev_needed: bool = True,
        over_write: bool = False
) -> bool:
    """
    导入词典, 对应参数参考 :func:`nlpir.native.key_scanner.KeyScanner.import_user_dict`

    :param user_dict:
    :param filter_index:
    :param pinyin_abbrev_needed:
    :param over_write:
    :return:
    """
    handle = __instance__.new_instance(filter_index)
    __instance__.import_user_dict(
        filename=user_dict,
        pinyin_abbrev_needed=pinyin_abbrev_needed,
        over_write=over_write,
        handle=handle
    )
    __instance__.delete_instance(handle)
    return True


@__get_instance__
def delete_user_dict(
        user_dict: str,
        filter_index: int = 0
) -> bool:
    """
    删除词典中的某些单词, 对应参数参考 :func:`nlpir.native.key_scanner.KeyScanner.delete_user_dict`

    :param user_dict:
    :param filter_index:
    :return:
    """
    handle = __instance__.new_instance(filter_index)
    __instance__.delete_user_dic(user_dict, handle=handle)
    __instance__.delete_instance(handle)
    return True

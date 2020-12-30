#! coding=utf-8
"""
high-level toolbox for Chinese Key-word Extraction
"""
# pylint: disable=duplicate-code

from nlpir import get_instance as __get_instance__
from nlpir import native
import typing
import nlpir
import json

# class and class instance
__cls__ = native.key_extract.KeyExtract
__instance__: typing.Optional[native.key_extract.KeyExtract] = None
# Location of DLL
__lib__ = None
# Data directory
__data__ = None
# license_code
__license_code__ = None
# encode
__nlpir_encode__ = native.UTF8_CODE


@__get_instance__
def get_native_instance() -> native.key_extract.KeyExtract:
    """
    返回原生NLPIR接口,使用更多函数

    :return: The singleton instance
    """
    return __instance__


@__get_instance__
def import_dict(word_list: list) -> list:
    """
    See :func:`nlpir.import_dict`

    :param word_list: list of words want to add to NLPIR
    :return: the word fail to add to the NLPIR
    """
    return nlpir.import_dict(word_list=word_list, instance=__instance__)


@__get_instance__
def clean_user_dict() -> bool:
    """
    See :func:`nlpir.clean_user_dict`

    :return: success or not
    """
    return nlpir.clean_user_dict(instance=__instance__)


@__get_instance__
def delete_user_word(word_list: list):
    """
    See :func:`nlpir.delete_user_word`

    :param word_list: list of words want to delete
    """
    return nlpir.delete_user_word(word_list=word_list, instance=__instance__)


@__get_instance__
def save_user_dict() -> bool:
    """
    See :func:`nlpir.save_user_dict`

    :return: Success or not
    """
    return nlpir.save_user_dict(instance=__instance__)


@__get_instance__
def clean_saved_user_dict():
    """
    See :func:`nlpir.clean_saved_user_dict`

    :return: Delete success or not
    """
    return nlpir.clean_saved_user_dict()


@__get_instance__
def import_blacklist(filename: str, pos_blacklist=typing.List[str]) -> bool:
    """
    Import Blacklist to system, see :func:`nlpir.import_blacklist`
    """
    return nlpir.import_blacklist(__instance__, filename, pos_blacklist)


@__get_instance__
def clean_blacklist() -> bool:
    """
    清除黑名单词表, see :func:`nlpir.clean_blacklist`

    :return: clean success or not
    """
    return nlpir.clean_blacklist()


@__get_instance__
def recover_blacklist() -> bool:
    """
    恢复黑名单词表,仅在被重命名的词表存在时才起作用, see :func:`nlpir.recover_blacklist`

    :return:
    """
    return nlpir.recover_blacklist()


@__get_instance__
def get_key_words(text: str, max_key: int = 50) -> typing.List[dict]:
    """
    获取文本对应的关键词,以及对应的权值,词性,词频等信息
    Get keyword from text with weight, frequent and pos

    :param text:
    :param max_key: max number keyword want to get
    :return: a list of keywords with weight, example:

    ::

        [
            {
                'freq': 2,
                'pos': 'n_new',
                'weight': 7.771335980376418,
                'word': '国家权力'
            },{
                'freq': 7,
                'pos': 'n',
                'weight': 7.438759706600493,
                'word': '权力'
            },{
                'freq': 1,
                'pos': 'nrf',
                'weight': 5.280000338096665,
                'word': '孟德斯鸠'
            },{ ...
            }, ...
        ]


    """
    result = __instance__.get_keywords(line=text, max_key_limit=max_key, format_opt=native.OUTPUT_FORMAT_JSON)
    try:
        return json.loads(result)
    except json.decoder.JSONDecodeError:
        return []

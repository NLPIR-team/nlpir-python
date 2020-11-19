#! coding=utf-8
"""
high-level toolbox for Chinese Key-word Extraction
"""
# pylint: disable=duplicate-code

from nlpir import get_instance as __get_instance__
from nlpir import native, PACKAGE_DIR
import typing
import nlpir
import os

# class and class instance
__cls__ = native.ictclas.ICTCLAS
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
def import_blacklist(filename: str, pos_blacklist=list) -> bool:
    """
    Import Blacklist to system

    This function will permanently import blacklist words to system not to the memory .
    If you want to delete the blacklist words, you should run :func:`clean_blacklist` to delete
    blacklist form system .

    此函数将会把词永久性保存在NLPIR中,和保存用户词典类似.这里删除使用的是 :func:`clean_blacklist` .

    停用词表,Format of stop word::
        word1 n1
        word2 n2
        word3 n3

    若 `pos_blacklist` 为: ``['n1', 'n2']`` 则 `word1`, `word2` 将会进入屏蔽列表

    If `pos_blacklist` : ``['n1', 'n2']`` Then `word1`, `word2` will be in the blacklist

    :param filename: A word list that the words want to import to the blacklist (stop word list),
        一个停用词词表,里面为想进行屏蔽的词,也可以包括别的词,是否不进行抽取是按照词表中的词性来确定的.
    :param pos_blacklist: A list of pos that want to block in the system, 想要屏蔽的词的词性
    :return: 是否成功导入
    """
    try:
        os.rename(
            os.path.join(PACKAGE_DIR, "Data/KeyBlackList.pdat"),
            os.path.join(PACKAGE_DIR, "Data/KeyBlackList.pdat.bak")
        )
    except OSError:
        return False
    return_result = __instance__.import_key_blacklist(
        filename=filename,
        pos_blacklist="#".join(pos_blacklist)
    )
    if return_result > 0:
        return True
    else:
        clean_blacklist()
        return False


@__get_instance__
def clean_blacklist() -> bool:
    """
    TODO
    :return:
    """
    try:
        os.rename(
            os.path.join(PACKAGE_DIR, "Data/KeyBlackList.pdat.bak"),
            os.path.join(PACKAGE_DIR, "Data/KeyBlackList.pdat")
        )
        return True
    except OSError:
        return False


def get_key_words():
    pass
# TODO

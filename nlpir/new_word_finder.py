#! coding=utf-8
"""
high-level toolbox for Chinese New Word Finder
"""
# pylint: disable=duplicate-code

from nlpir import get_instance as __get_instance__
from nlpir import native, logger
import typing
import json

# class and class instance
__cls__ = native.new_word_finder.NewWordFinder
__instance__: typing.Optional[native.new_word_finder.NewWordFinder] = None
# Location of DLL
__lib__ = None
# Data directory
__data__ = None
# license_code
__license_code__ = None
# encode
__nlpir_encode__ = native.UTF8_CODE


@__get_instance__
def get_native_instance() -> native.new_word_finder.NewWordFinder:
    """
    返回原生NLPIR接口,使用更多函数

    :return: The singleton instance
    """
    return __instance__


@__get_instance__
def find_new_words(text: str, max_key: int) -> typing.Optional[typing.List[dict]]:
    """
    获取新词,返回新词和对应权重词性,此函数适合较少数量的文本的新词发现功能(不超过20M),
    若数量较大可以使用 :func:`find_new_words_batch` 进行处理

    :param text: 文本内容
    :param max_key: 新词发现返回的新词数量最大值
    :return: 格式如下

    ::

        [
            {
                "freq" : 225,
                "pos" : "n_new",
                "weight" : 126.28066602434734,
                "word" : "主权者"
            }, {
                "freq" : 100,
                "pos" : "n_new",
                "weight" : 60.782738270597314,
                "word" : "行政官"
            }, {
                "freq" : 103,
                "pos" : "n_new",
                "weight" : 45.549023266744136,
                "word" : "卢梭"
            }, { ... }
            ...
        ]
    """
    return json.loads(__instance__.get_new_words(line=text, max_key_limit=max_key, format_opt=native.OUTPUT_FORMAT_JSON))


@__get_instance__
def find_new_words_batch(text_iter: typing.Iterable[str]) -> typing.Optional[typing.List[dict]]:
    """

    :param text_iter: 文本迭代器, 迭代器内容为文本
    :return: 同 :func:`find_new_words`
    """
    logger.debug("batch new word finder start")
    if not __instance__.batch_start():
        logger.error("batch start fail")
        return None
    for text in text_iter:
        logger.debug("adding text to system")
        if not __instance__.batch_addmen(text=text):
            logger.error("fail to add file")
    if not __instance__.batch_complete():
        logger.error("complete batch process fail")
        return None
    try:
        return json.loads(__instance__.batch_getresult(format_json=True))
    except json.decoder.JSONDecodeError:
        logger.error("get result fail")
        return []


def export_dict(words_result: typing.List[dict], save_path: str) -> bool:
    """
    将 :func:`find_new_words_batch` 和 :func:`find_new_words` 获得的结果保存为词典

    :param words_result: 新词发现返回结果
    :param save_path: 保存词典位置
    :return: 是否保存成功
    """
    dict_txt = ""
    for i in words_result:
        item = f"{i['word']}\t{i['pos']}\n"
        dict_txt += item
    with open(save_path, "w") as f:
        f.write(dict_txt)
    return True

#! coding=utf-8
"""
high-level toolbox for Summarization
"""
from nlpir import get_instance as __get_instance__
from nlpir import native
import typing

# class and class instance
__cls__ = native.summary.Summary
__instance__: typing.Optional[native.Summary] = None
# Location of DLL
__lib__ = None
# Data directory
__data__ = None
# license_code
__license_code__ = None
# encode
__nlpir_encode__ = native.UTF8_CODE


@__get_instance__
def get_native_instance() -> native.Summary:
    """
    返回原生NLPIR接口,使用更多函数

    :return: The singleton instance
    """
    return __instance__


@__get_instance__
def summarization(
        content: str,
        sum_rate: float = 0.0,
        sum_len: int = 250,
        html_tag_remove: bool = True,
        sentence_count: int = 0

) -> str:
    """
    摘要生成, 摘要长度受 `sum_rate` , `sum_len` 影响

    :param content: 文档内容 text content
    :param sum_rate: 文档摘要占原文百分比(为0.00则不限制）
        the percentage of summarization length comparing to original text (0.00 represent no limit):
    :param sum_len: 用户限定的摘要长度(为0则不限制）The max len of summarization(0 will no limit)
    :param html_tag_remove: 是否需要对原文进行Html标签的去除 remove the html tag or not
    :param int sentence_count: 用户限定的句子数量 （为0则不限制）limit number of sentence, set 0 to no limit
    :return: 摘要字符串；出错返回空串 the summarization content, get null string if occurs error.
    """
    return __instance__.single_doc_e(
        text=content,
        sum_rate=sum_rate,
        sum_len=sum_len,
        html_tag_remove=0 if html_tag_remove else 1
    )

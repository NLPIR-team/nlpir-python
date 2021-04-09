#! coding=utf-8
"""
high-level toolbox for Summarization
"""
from nlpir import get_instance as __get_instance__
from nlpir import native
from nlpir.native.text_similarity import SIM_MODEL_WORD, SIM_MODEL_CHAR, SIM_MODEL_KEY
import typing

# class and class instance
__cls__ = native.text_similarity.TextSimilarity
__instance__: typing.Optional[native.TextSimilarity] = None
# Location of DLL
__lib__ = None
# Data directory
__data__ = None
# license_code
__license_code__ = None
# encode
__nlpir_encode__ = native.UTF8_CODE

__all__ = [
    "get_native_instance",
    "similarity",
    "SIM_MODEL_WORD",
    "SIM_MODEL_KEY",
    "SIM_MODEL_CHAR"
]


@__get_instance__
def get_native_instance() -> native.TextSimilarity:
    """
    返回原生NLPIR接口,使用更多函数

    :return: The singleton instance
    """
    return __instance__


@__get_instance__
def similarity(text_1: str, text_2: str, model=SIM_MODEL_WORD) -> float:
    """
    compute text similarity, there are three models:

    - :data:`SIM_MODEL_WORD` 词模型，速度适中，常规适用于正常规范的长文档
    - :data:`IM_MODEL_CHAR` 字模型，速度最快，适用于相对规范的短文本
    - :data:`SIM_MODEL_KEY` 主题词模型，速度最慢，考虑语义最多，适合于复杂文本

    :param text_1:
    :param text_2:
    :param model:
    :return:
    """
    return __instance__.compute_sim(
        text_1=text_1,
        text_2=text_2,
        model=model,
    )

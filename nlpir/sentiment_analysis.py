#! coding=utf-8
"""
high-level toolbox for Sentiment Analysis
"""
from nlpir import get_instance as __get_instance__
from nlpir import native
from enum import Enum
import typing

# class and class instance
__cls__ = native.sentiment.SentimentAnalysis
__instance__: typing.Optional[native.SentimentAnalysis] = None
# Location of DLL
__lib__ = None
# Data directory
__data__ = None
# license_code
__license_code__ = None
# encode
__nlpir_encode__ = native.UTF8_CODE


class EmotionType(str, Enum):
    EMOTION_HAPPY = "EMOTION_HAPPY"
    EMOTION_GOOD = "EMOTION_GOOD"
    EMOTION_ANGER = "EMOTION_ANGER"
    EMOTION_SORROW = "EMOTION_SORROW"
    EMOTION_FEAR = "EMOTION_FEAR"
    EMOTION_EVIL = "EMOTION_EVIL"
    EMOTION_SURPRISE = "EMOTION_SURPRISE"


@__get_instance__
def get_native_instance() -> native.SentimentAnalysis:
    """
    返回原生NLPIR接口,使用更多函数

    :return: The singleton instance
    """
    return __instance__


@__get_instance__
def get_emotion(
        content: str,
) -> typing.Dict[EmotionType, int]:
    """
    获取 Sentiment Analysis 结果

    :param content: 文档内容 text content
    :return:
    """
    result = __instance__.get_paragraph_sent_e(
        paragraph=content,
    )
    result = [_.split("/") for _ in result.split("\n")]
    structured_result = dict()
    for _ in result:
        if len(_) < 2:
            continue
        emotion, score = _
        structured_result[EmotionType(emotion)] = int(score)

    return structured_result

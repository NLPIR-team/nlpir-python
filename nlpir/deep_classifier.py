#! coding=utf-8
"""
high-level toolbox for text classify
"""
import re
import typing
import nlpir
from nlpir import get_instance as __get_instance__
from nlpir import native

# class and class instance
__cls__ = native.deep_classifier.DeepClassifier
__instance__: typing.Optional[native.deep_classifier.DeepClassifier] = None
# Location of DLL
__lib__ = None
# Data directory
__data__ = None
# license_code
__license_code__ = None
# encode
__nlpir_encode__ = native.UTF8_CODE

__handler__ = None


@__get_instance__
def get_native_instance() -> native.deep_classifier.DeepClassifier:
    """
    返回原生NLPIR接口,使用更多函数

    :return: The singleton instance
    """
    return __instance__


@__get_instance__
def classify(txt: str) -> str:
    """
    Text classify

    :param txt: text
    :return: class
    """
    global __handler__
    if __handler__ is None:
        # default model
        __handler__ = __instance__.new_instance(800)
        __instance__.load_train_result(__handler__)
    return __instance__.classify(txt, handler=__handler__)

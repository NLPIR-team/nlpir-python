#! coding=utf-8
"""
high-level toolbox for Document Extractor
"""
import re
import typing
import nlpir
from nlpir import get_instance as __get_instance__
from nlpir import native

# class and class instance
__cls__ = native.doc_extractor.DocExtractor
__instance__: typing.Optional[native.doc_extractor.DocExtractor] = None
# Location of DLL
__lib__ = None
# Data directory
__data__ = None
# license_code
__license_code__ = None
# encode
__nlpir_encode__ = native.UTF8_CODE


class ExtractResult:
    """
    A class for retrieve result from Document Extractor's handle
    """
    #: Types map can be retrieved from DocExtractor
    retrieve_type_map: typing.Dict[str, int] = {
        "person": native.doc_extractor.DOC_EXTRACT_TYPE_PERSON,
        "location": native.doc_extractor.DOC_EXTRACT_TYPE_LOCATION,
        "organization": native.doc_extractor.DOC_EXTRACT_TYPE_ORGANIZATION,
        "keyword": native.doc_extractor.DOC_EXTRACT_TYPE_KEYWORD,
        "author": native.doc_extractor.DOC_EXTRACT_TYPE_AUTHOR,
        "media": native.doc_extractor.DOC_EXTRACT_TYPE_MEDIA,
        "country": native.doc_extractor.DOC_EXTRACT_TYPE_COUNTRY,
        "province": native.doc_extractor.DOC_EXTRACT_TYPE_PROVINCE,
        "abstract": native.doc_extractor.DOC_EXTRACT_TYPE_ABSTRACT,
        "positive": native.doc_extractor.DOC_EXTRACT_TYPE_POSITIVE,
        "negative": native.doc_extractor.DOC_EXTRACT_TYPE_NEGATIVE,
        "text": native.doc_extractor.DOC_EXTRACT_TYPE_TEXT,
        "time": native.doc_extractor.DOC_EXTRACT_TYPE_TIME,
        "user": native.doc_extractor.DOC_EXTRACT_TYPE_USER
    }

    def __init__(self, handle: int, user_retrieve_type: typing.List[str]):
        self.handle: int = handle
        # add user defined pos
        self.user_retrieve_type_map: typing.Dict[str, int] = {
            _: self.retrieve_type_map["user"] + i for i, _ in user_retrieve_type
        }
        self.retrieve_types: typing.List[int] = [
            native.doc_extractor.DOC_EXTRACT_TYPE_PERSON,
            native.doc_extractor.DOC_EXTRACT_TYPE_LOCATION,
            native.doc_extractor.DOC_EXTRACT_TYPE_ORGANIZATION,
            native.doc_extractor.DOC_EXTRACT_TYPE_KEYWORD,
            native.doc_extractor.DOC_EXTRACT_TYPE_AUTHOR,
            native.doc_extractor.DOC_EXTRACT_TYPE_MEDIA,
            native.doc_extractor.DOC_EXTRACT_TYPE_COUNTRY,
            native.doc_extractor.DOC_EXTRACT_TYPE_PROVINCE,
            native.doc_extractor.DOC_EXTRACT_TYPE_ABSTRACT,
            native.doc_extractor.DOC_EXTRACT_TYPE_POSITIVE,
            native.doc_extractor.DOC_EXTRACT_TYPE_NEGATIVE,
            native.doc_extractor.DOC_EXTRACT_TYPE_TEXT,
            native.doc_extractor.DOC_EXTRACT_TYPE_TIME,
        ]
        self.retrieve_types += self.user_retrieve_type_map.values()

        self.all_available_type_map = self.get_available_retrieve_types()
        self.__retrieve_type_reverse_map = {
            self.all_available_type_map[retrieve_type]: retrieve_type for retrieve_type in self.all_available_type_map
        }

        self.re_result = re.compile(r"(.+?)/([a-z0-9A-Z]+?)/([.\d]+?)/(\d+)?#")

    def get_available_retrieve_types(self) -> typing.Dict[str, int]:
        """
        Get a set of types_name and types available for current extraction result

        :return:
        """
        return {**self.retrieve_type_map, **self.user_retrieve_type_map}

    def set_retrieve_types(self, retrieve_type_list: typing.List[int]) -> bool:
        """
        Set what type of data want to get from :func:`get_result` , can be set multi-times

        :param retrieve_type_list: list of retrieve types
        :return:
        """
        self.retrieve_types = retrieve_type_list
        return True

    @__get_instance__
    def get_result(
            self,
            retrieve_types: typing.Optional[typing.List[int]] = None
    ) -> typing.Dict[str, typing.List[typing.Dict[str, typing.Union[str, int, float]]]]:
        """
        Get result from current result, can be retrieved multi-times.

        :param retrieve_types: option, a list of retrieve types want to get,
            default is all types can be retrieved or certain types set by :func:`set_retrieve_types`
        :return: a dict of result : ``{type_name: [result}]}`` , example

        ::

            {
            "person": [
                    {
                        "word": "卢梭",
                        "pos": "n",
                        "weight": 1.5,
                        "frq": 100
                    }
                ]
            }
        """
        if retrieve_types is not None:
            self.set_retrieve_types(retrieve_types)
        result_dict = dict()
        for retrieve_type in self.retrieve_types:
            result = __instance__.get_result(
                handle=self.handle, doc_extract_type=retrieve_type
            )
            result = self.re_result.findall(result)
            result_dict[self.__retrieve_type_reverse_map[retrieve_type]] = [
                {
                    "word": string_tuple[0],
                    "pos": string_tuple[1],
                    "weight": float(string_tuple[2]),
                    "frq": int(string_tuple[3])
                }
                for string_tuple in result
            ]
        return result_dict

    @__get_instance__
    def get_sentiment_result(self) -> int:
        """
        Get sentiment point from current extraction result

        :return:
        """
        return __instance__.get_sentiment_score(self.handle)

    @__get_instance__
    def __del__(self):
        return __instance__.release_handle(self.handle)


@__get_instance__
def get_native_instance() -> native.doc_extractor.DocExtractor:
    """
    返回原生NLPIR接口,使用更多函数

    :return: The singleton instance
    """
    return __instance__


@__get_instance__
def extract(text: str, user_define_pos: typing.List[str]) -> ExtractResult:
    """

    :param text:
    :param user_define_pos:
    :return:
    """
    handle = __instance__.pares_doc_e(text, "#".join(user_define_pos))
    return ExtractResult(handle=handle, user_retrieve_type=user_define_pos)


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

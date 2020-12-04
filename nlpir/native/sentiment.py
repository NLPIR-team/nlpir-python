# coding=utf-8
from nlpir.native.nlpir_base import NLPIRBase
from ctypes import c_bool, c_char_p, c_double, c_int, byref, create_string_buffer
import typing


class SentimentNew(NLPIRBase):
    @property
    def dll_name(self):
        return "SentimentNew"

    @NLPIRBase.byte_str_transform
    def init_lib(self, data_path: str, encode: int, license_code: str) -> int:
        """
        Call **ST_Init**

        :param data_path:
        :param encode:
        :param license_code:
        :return:
        """
        return self.get_func("ST_Init", [c_char_p, c_int, c_char_p], c_int)(data_path, encode, license_code)

    @NLPIRBase.byte_str_transform
    def exit_lib(self) -> bool:
        """
        Call **ST_Exit**

        :return:
        """
        return self.get_func("ST_Exit", None, c_int)()

    @NLPIRBase.byte_str_transform
    def get_last_error_msg(self) -> str:
        """
        Call **ST_GetLastErrMsg**

        :return:
        """
        return self.get_func("ST_GetLastErrMsg", None, c_char_p)()

    @NLPIRBase.byte_str_transform
    def get_one_object_result(self, title: str, content: str, analysis_object: str) -> str:
        """
        Call **ST_GetOneObjectResult**

        :param title:
        :param content:
        :param analysis_object:
        :return:
        """
        return self.get_func("ST_GetOneObjectResult", [c_char_p, c_char_p, c_char_p], c_char_p)(
            title,
            content,
            analysis_object
        )

    @NLPIRBase.byte_str_transform
    def get_multi_object_result(self, title: str, content: str, object_rule_file: str) -> str:
        """
        Call **ST_GetMultiObjectResult**

        :param title:
        :param content:
        :param object_rule_file: see Appendix II: Multiple Object configure sample
        :return:
        """
        return self.get_func("ST_GetMultiObjectResult", [c_char_p, c_char_p, c_char_p], c_char_p)(
            title, content, object_rule_file
        )

    @NLPIRBase.byte_str_transform
    def get_sentence_point(self, sentence: str) -> float:
        """

        Call **ST_GetSentimentPoint**

        Get multiple object sentimental result

        :param sentence:
        :return:  double,Sentimental point
        """
        return self.get_func("ST_GetSentimentPoint", [c_char_p], c_double)(sentence)

    @NLPIRBase.byte_str_transform
    def import_user_dict(self, filename: str, over_write: bool = False) -> int:
        """
        Call **ST_ImportUserDict**

        Import User-defined dictionary, same as :func:`nlpir.native.ictclas.ICTCLAS.import_user_dict`

        :param filename:
        :param over_write:
        :return:
        """
        return self.get_func("ST_ImportUserDict", [c_char_p, c_bool], c_int)(filename, over_write)


class SentimentAnalysis(NLPIRBase):
    EMOTION_HAPPY = 0
    EMOTION_GOOD = 1
    EMOTION_ANGER = 2
    EMOTION_SORROW = 3
    EMOTION_FEAR = 4
    EMOTION_EVIL = 5
    EMOTION_SURPRISE = 6

    @property
    def dll_name(self):
        return "LJSentimentAnalysis"

    @NLPIRBase.byte_str_transform
    def init_lib(self, data_path: str, encode: int, license_code: str) -> int:
        """
        Call **LJST_Inits**

        :param data_path:
        :param encode:
        :param license_code:
        :return:
        """
        return self.get_func("LJST_Inits", [c_char_p, c_int, c_char_p], c_int)(data_path, encode, license_code)

    @NLPIRBase.byte_str_transform
    def exit_lib(self) -> bool:
        """
        Call **LJST_Exits**

        :return:
        """
        return self.get_func("LJST_Exits", None, c_bool)()

    @NLPIRBase.byte_str_transform
    def get_last_error_msg(self) -> str:
        """

        :return:
        """
        return "No error function"

    @NLPIRBase.byte_str_transform
    def get_paragraph_sent(self, paragraph: str) -> typing.Tuple[bool, str]:
        """
        Call **LJST_GetParagraphSent**

        Get sentiment analyze result

        :param paragraph:
        :return:
        """
        result = create_string_buffer(10240)
        result_bool = self.get_func("LJST_GetParagraphSent", [c_char_p, c_char_p], c_bool)(paragraph, result)
        return result_bool, result.value

    @NLPIRBase.byte_str_transform
    def get_file_sent(self, filename: str) -> typing.Tuple[bool, str]:
        """
        Call **LJST_GetFileSent**

        Get sentiment analyze result

        :param filename:
        :return:
        """
        result = create_string_buffer(10240)
        result_bool = self.get_func("LJST_GetFileSent", [c_char_p, c_char_p], c_bool)(filename, byref(result))
        return result_bool, result.value

    @NLPIRBase.byte_str_transform
    def import_user_dict(self, filename: str, over_write: bool = False):
        """
        Call **LJST_ImportUserDict**

        Import User-defined dictionary, same as :func:`nlpir.native.ictclas.ICTCLAS.import_user_dict`

        :param filename:
        :param over_write:
        :return:
        """
        return self.get_func("LJST_ImportUserDict", [c_char_p, c_bool], c_int)(filename, over_write)

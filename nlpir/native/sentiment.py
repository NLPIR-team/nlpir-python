# coding=utf-8
from nlpir.native.nlpir_base import NLPIRBase, UTF8_CODE, PACKAGE_DIR
from ctypes import c_bool, c_char_p, c_double, c_int, byref, create_string_buffer
import typing
import os


class SentimentNew(NLPIRBase):
    @property
    def dll_name(self):
        return "SentimentNew"

    def __init__(
            self,
            encode: int = UTF8_CODE,
            lib_path: typing.Optional[int] = None,
            data_path: typing.Optional[str] = None,
            license_code: str = ''
    ):
        sentiment_path = os.path.join(PACKAGE_DIR, "Data/Sentiment")
        data_path = sentiment_path if data_path is None else data_path
        super().__init__(encode, lib_path, data_path, license_code)

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
        Call **ST_GetLastErrorMsg**

        :return:
        """
        return self.get_func("ST_GetLastErrorMsg", None, c_char_p)()

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
    def get_sentence_point(self, sentence: str) -> str:
        """

        Call **ST_GetSentencePoint**

        Get multiple object sentimental result

        :param sentence:
        :return:  double,Sentimental point
        """
        return self.get_func("ST_GetSentencePoint", [c_char_p], c_char_p)(sentence)

    @NLPIRBase.byte_str_transform
    def get_sentiment_point(self, sentence: str) -> float:
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

    @NLPIRBase.byte_str_transform
    def process_dir(self, path: str) -> str:
        """
        Call **ST_ProcesDir**

        批量处理指定的目录下的文本文件. 分析结果, 输出到指定的Excel文件中

        :param path:
        :return: path目录下, 自动生成 ``SentimentRankResult.xls``,返回该文件的全路径名称
        """
        return self.get_func("ST_ProcesDir", [c_char_p], c_char_p)(path)


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
        Call **LJST_Init**

        :param data_path:
        :param encode:
        :param license_code:
        :return:
        """
        return self.get_func("LJST_Init", [c_char_p, c_int, c_char_p], c_int)(data_path, encode, license_code)

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
        return self.get_func("LJST_GetLastErrorMsg", None, c_char_p)()

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

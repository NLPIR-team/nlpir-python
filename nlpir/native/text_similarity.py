# coding=utf-8
from nlpir.native.nlpir_base import NLPIRBase
from ctypes import c_char_p, c_int, c_double

SIM_MODEL_CHAR = 1  #: 字模型，速度最快，适用于相对规范的短文本
SIM_MODEL_WORD = 2  #: 词模型，速度适中，常规适用于正常规范的长文档
SIM_MODEL_KEY = 3  #: 主题词模型，速度最慢，考虑语义最多，适合于复杂文本


class TextSimilarity(NLPIRBase):

    @property
    def dll_name(self):
        return "TextSimilarity"

    @NLPIRBase.byte_str_transform
    def init_lib(self, data_path: str, encode: int, license_code: str) -> int:
        """
        Call **TS_Init**

        :param data_path:
        :param encode:
        :param license_code:
        :return:
        """
        return self.get_func("TS_Init", [c_char_p, c_int, c_char_p], c_int)(data_path, encode, license_code)

    @NLPIRBase.byte_str_transform
    def exit_lib(self) -> bool:
        """
        Call **DS_Exit**

        :return:
        """
        self.get_func("TS_Exit", None, None)()
        return True

    @NLPIRBase.byte_str_transform
    def get_last_error_msg(self) -> str:
        """
        Call **TS_GetLastErrorMsg**

        :return:
        """
        return self.get_func("TS_GetLastErrorMsg", None, c_char_p)()

    @NLPIRBase.byte_str_transform
    def compute_sim(self, text_1: str, text_2: str, model: int = SIM_MODEL_WORD) -> float:
        """
        Call **TS_ComputeSim**

        :param text_1:
        :param text_2:
        :param model:
        :return:
        """
        return self.get_func("TS_ComputeSim", [c_char_p, c_char_p, c_int], c_double)(text_1, text_2, model)

    @NLPIRBase.byte_str_transform
    def compute_sim_file(self, filename_1: str, filename_2: str, model: int = SIM_MODEL_WORD) -> float:
        """
        Call **TS_ComputeSimFile**

        :param filename_1:
        :param filename_2:
        :param model:
        :return:
        """
        return self.get_func("TS_ComputeSimFile", [c_char_p, c_char_p, c_int], c_double)(filename_1, filename_2, model)

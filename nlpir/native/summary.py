# coding=utf-8
from nlpir.native.nlpir_base import NLPIRBase
from ctypes import c_char_p, c_int, c_float, create_string_buffer


class Summary(NLPIRBase):
    load_mode = NLPIRBase.RTLD_LAZY

    @property
    def dll_name(self):
        return "LJSummary"

    @NLPIRBase.byte_str_transform
    def init_lib(self, data_path: str, encode: int, license_code: str) -> int:
        """
        Call **DS_Init**

        :param data_path:
        :param encode:
        :param license_code:
        :return:
        """
        return self.get_func("DS_Init", [c_char_p, c_int, c_char_p], c_int)(data_path, encode, license_code)

    @NLPIRBase.byte_str_transform
    def exit_lib(self) -> bool:
        """
        Call **DS_Exit**

        :return:
        """
        self.get_func("DS_Exit", None, None)()
        return True

    @NLPIRBase.byte_str_transform
    def get_last_error_msg(self) -> str:
        """
        Call **DS_GetLastErrMsg**

        :return:
        """
        return self.get_func("DS_GetLastErrorMsg", None, c_char_p)()

    @NLPIRBase.byte_str_transform
    def single_doc(self, text: str, sum_rate: float = 0.0, sum_len: int = 250, html_tag_remove: int = 0):
        """
        Call **DS_SingleDoc**

        生成单文档摘要, make summarization

        :param str text: 文档内容 text content
        :param float sum_rate: 文档摘要占原文百分比(为0.00则不限制）
            the percentage of summarization length comparing to original text (0.00 represent no limit)
        :param int sum_len: 用户限定的摘要长度(为0则不限制）The max len of summarization(0 will no limit)
        :param bool html_tag_remove: 是否需要对原文进行Html标签的去除 remove the html tag or not
        :return: 摘要字符串；出错返回空串 the summarization content, get null string if occurs error.
        """
        return self.get_func("DS_SingleDoc", [c_char_p, c_float, c_int, c_int], c_char_p)(
            text, c_float(sum_rate), sum_len, html_tag_remove
        )

    @NLPIRBase.byte_str_transform
    def single_doc_e(self, text: str, sum_rate: float = 0.0, sum_len: int = 250, html_tag_remove: int = 0):
        """
        Call **DS_SingleDocE**

        生成单文档摘要该函数支持多线程，是多线程安全的, make summarization with threading safe

        :param str text: 文档内容 text content
        :param float sum_rate: 文档摘要占原文百分比(为0.00则不限制）
            the percentage of summarization length comparing to original text (0.00 represent no limit)
        :param int sum_len: 用户限定的摘要长度(为0则不限制）The max len of summarization(0 will no limit)
        :param bool html_tag_remove: 是否需要对原文进行Html标签的去除 remove the html tag or not
        :return: 摘要字符串；出错返回空串 the summarization content, get null string if occurs error.
        """
        buffer_len = int(len(text) * 3 * (sum_rate if sum_rate > 0.0 else 1))
        buffer_len = sum_len if sum_len < buffer_len else buffer_len
        result = create_string_buffer(buffer_len * 4)
        result_2 = self.get_func("DS_SingleDocE", [c_char_p, c_char_p, c_float, c_int, c_int])(
            result, text, c_float(sum_rate), sum_len, html_tag_remove
        )
        return result.value, result_2

    @NLPIRBase.byte_str_transform
    def file_process(self, text_filename: str, sum_rate: float = 0.0, sum_len: int = 250, html_tag_remove: int = 0):
        """
        Call **DS_FileProcess**

        生成单文档摘要该函数支持多线程,是多线程安全的, make summarization from file with threading safe

        :param str text_filename: 文档文件路径 text file path
        :param float sum_rate: 文档摘要占原文百分比(为0.00则不限制）
            the percentage of summarization length comparing to original text (0.00 represent no limit)
        :param int sum_len: 用户限定的摘要长度(为0则不限制）The max len of summarization(0 will no limit)
        :param bool html_tag_remove: 是否需要对原文进行Html标签的去除 remove the html tag or not
        :return: 摘要字符串；出错返回空串 the summarization content, get null string if occurs error.
        """
        return self.get_func("DS_FileProcess", [c_char_p, c_float, c_int, c_int], c_char_p)(
            text_filename, c_float(sum_rate), sum_len, html_tag_remove)

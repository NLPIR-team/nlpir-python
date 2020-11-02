# coding=utf-8
from nlpir.native.nlpir_base import NLPIRBase
from ctypes import c_bool, c_char, c_char_p, c_double, c_int, c_uint, POINTER, Structure, byref, c_float
import typing


class Summary(NLPIRBase):

    @property
    def dll_name(self):
        return "LJSummary"

    @NLPIRBase.byte_str_transform
    def init_lib(self, data_path: str, encode: int, license_code: str) -> int:
        """
        功能：初始化
        参数：sLicenseCode - 授权码
            sPath-default path
        返回：true - 成功；false - 失败
        备注：在进程中此函数必须在其他函数之前调用（只需执行一次）

        :param data_path:
        :param encode:
        :param license_code:
        :return:
        """
        return self.get_func("DS_Init", [c_char_p, c_int, c_char_p], c_int)(data_path, encode, license_code)

    @NLPIRBase.byte_str_transform
    def exit_lib(self) -> bool:
        """

        :return:
        """
        self.get_func("DS_Exit", None, None)()
        return True

    @NLPIRBase.byte_str_transform
    def get_last_error_msg(self) -> str:
        """

        :return:
        """
        return self.get_func("DS_GetLastErrMsg", None, c_char_p)()

    @NLPIRBase.byte_str_transform
    def single_doc(self, text: str, sum_rate: float = 0.0, sum_len: int = 250, html_tag_remove: int = 0):
        """
        功能：生成单文档摘要
        参数：sText	    -[IN] 文档内容
            fSumRate	-[IN] 文档摘要占原文百分比（为0.00则不限制）
            iSumLen		-[IN] 用户限定的摘要长度  （为0则不限制）
            bHtmlTagRemove-[IN] 是否需要对原文进行Html标签的去除
        返回：摘要字符串；出错返回空串
        备注：在进程中此函数可以执行多次
        :param text:
        :param sum_rate:
        :param sum_len:
        :param html_tag_remove:
        :return:
        """
        return self.get_func("DS_SingleDoc", [c_char_p, c_float, c_int, c_int], c_char_p)(
            text, sum_rate, sum_len, html_tag_remove
        )

    @NLPIRBase.byte_str_transform
    def single_doc_e(self, text: str, sum_rate: float = 0.0, sum_len: int = 250, html_tag_remove: int = 0):
        """
        功能：生成单文档摘要该函数支持多线程，是多线程安全的
        参数：sResult    -[IN] 摘要内容
            sText	    -[IN] 文档内容
            fSumRate	-[IN] 文档摘要占原文百分比（为0.00则不限制）
            iSumLen		-[IN] 用户限定的摘要长度  （为0则不限制）
            bHtmlTagRemove-[IN] 是否需要对原文进行Html标签的去除
        返回：摘要字符串；出错返回空串
        备注：在进程中此函数可以执行多次

        :param text:
        :param sum_rate:
        :param sum_len:
        :param html_tag_remove:
        :return:
        """
        result = c_char_p()
        result_2 = self.get_func("DS_SingleDocE", [c_char_p, c_char_p, c_float, c_int, c_int])(
            byref(result), text, sum_rate, sum_len, html_tag_remove
        )
        return result, result_2

    @NLPIRBase.byte_str_transform
    def file_process(self, text_filename: str, sum_rate: float = 0.0, sum_len: int = 250, html_tag_remove: int = 0):
        """
        功能：生成单文档摘要该函数支持多线程，是多线程安全的
        参数：sTextFilename	    -[IN] 文档文件名
            fSumRate	-[IN] 文档摘要占原文百分比（为0.00则不限制）
            iSumLen		-[IN] 用户限定的摘要长度  （为0则不限制）
            bHtmlTagRemove-[IN] 是否需要对原文进行Html标签的去除
        返回：摘要字符串；出错返回空串
        备注：在进程中此函数可以执行多次
        :param text_filename:
        :param sum_rate:
        :param sum_len:
        :param html_tag_remove:
        :return:
        """
        return self.get_func("DS_FileProcess", [c_char_p, c_float, c_int, c_int], c_char_p)(
            text_filename, sum_rate, sum_len, html_tag_remove)

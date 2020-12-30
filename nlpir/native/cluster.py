# coding=utf-8
from nlpir.native.nlpir_base import NLPIRBase
from ctypes import c_bool, c_char_p, c_int
import typing


class Cluster(NLPIRBase):
    load_mode = NLPIRBase.RTLD_LAZY

    @property
    def dll_name(self):
        return "LJCluster"

    @NLPIRBase.byte_str_transform
    def init_lib(self, data_path: str, encode: int, license_code: str) -> int:
        """
        Call **CLUS_init**

        :param data_path:
        :param encode:
        :param license_code:
        :return: 1 success 0 fail
        """
        return self.get_func("CLUS_Init", [c_char_p, c_char_p, c_int], c_bool)(data_path, license_code, encode)

    @NLPIRBase.byte_str_transform
    def exit_lib(self) -> bool:
        """
        Call **CLUS_exit**

        :return: exit success or not
        """
        return self.get_func("CLUS_Exit", None, None)()

    @NLPIRBase.byte_str_transform
    def get_last_error_msg(self) -> str:
        """
        Call **CLUS_GetLastErrMsg**

        :return:
        """
        return self.get_func("CLUS_GetLastErrMsg", None, c_char_p)()

    @NLPIRBase.byte_str_transform
    def set_parameter(self, max_clus: int, max_doc: int) -> bool:
        """
        Call **CLUS_SetParameter**

        设置最大类别数以及最大输入文档数,类和类内的文档均已按照重要性和及时性排过序

        :param max_clus: 最大类别数
        :param max_doc: 最大文档数
        :return: 是否成功
        """
        return self.get_func("CLUS_SetParameter", [c_int, c_int], c_bool)(max_clus, max_doc)

    @NLPIRBase.byte_str_transform
    def add_content(self, text: str, signature: str) -> bool:
        """
        Call **CLUS_AddContent**

        追加内存内容,在进程中此函数可以在打印结果之前执行多次

        :param text: 正文
        :param signature: 唯一标识
        :return: 是否成功
        """
        return self.get_func("CLUS_AddContent", [c_char_p, c_char_p], c_bool)(text, signature)

    @NLPIRBase.byte_str_transform
    def add_file(self, filename: str, signature: str):
        """
        Call **CLUS_AddFile**

        追加文件内容,在进程中此函数可以在打印结果之前执行多次

        :param filename: 正文文件
        :param signature: 唯一标识
        :return: 是否成功
        """
        return self.get_func("CLUS_AddFile", [c_char_p, c_char_p], c_bool)(filename, signature)

    @NLPIRBase.byte_str_transform
    def get_latest_result(
            self,
            xml_filename: str,
            result_path: typing.Optional[str] = None,
    ) -> typing.Tuple[bool, str]:
        """
        Call **CLUS_GetLatestResult**

        输出结果到xml文件中

        ::

            <?xml version="1.0" encoding="gb2312" standalone="yes" ?>
            <LJCluster-Result>
            <clusnum>2</clusnum>

            <clus id="0">
                <feature>奥巴马 竞选 财务部</feature>
                <docs num="6">
                   <doc>2</doc>
                   <doc>3</doc>
                   <doc>35</doc>
                   <doc>86</doc>
                   <doc>345</doc>
                   <doc>975</doc>
                </docs>
            </clus>

            <clus id="1">
                <feature>林志玲 影视 电影 广告</feature>
                <docs num="4">
                   <doc>45</doc>
                   <doc>86</doc>
                   <doc>135</doc>
                   <doc>286</doc>
                </docs>
            </clus>
            </LJCluster-Result>

        :param xml_filename: 输出文件名
        :param result_path: 输出路径
        :return: 是否成功
        """
        status = self.get_func("CLUS_GetLatestResult", [c_char_p, c_char_p], c_bool)(xml_filename, result_path)
        return status

    @NLPIRBase.byte_str_transform
    def get_latest_result_e(self, result_path: typing.Optional[str] = None) -> str:
        """
        Call **CLUS_GetLatestResultE**

        输出xml结果到内存

        :param result_path:
        :return: xml like :func:`get_latest_result`
        """
        return self.get_func("CLUS_GetLatestResultE", [c_char_p], c_char_p)(result_path)

    @NLPIRBase.byte_str_transform
    def clean_data(self) -> None:
        """
        Call **CLUS_CleanData**

        清空历史数据

        :return:
        """
        return self.get_func("CLUS_CleanData", None, None)()

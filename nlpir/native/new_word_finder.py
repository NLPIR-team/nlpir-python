# coding=utf-8
from nlpir.native.nlpir_base import NLPIRBase
from nlpir.native import nlpir_base
from ctypes import c_bool, c_char_p, c_int, c_uint, c_ulong


class NewWordFinder(NLPIRBase):

    @property
    def dll_name(self) -> str:
        return "NewWordFinder"

    @NLPIRBase.byte_str_transform
    def init_lib(self, data_path: str, encode: int, license_code: str) -> int:
        """
        Call **NWF_Init**

        :param str data_path:
        :param int encode:
        :param str license_code:
        :return: 1 success 0 fail
        """
        return self.get_func("NWF_Init", [c_char_p, c_int, c_char_p], c_int)(data_path, encode, license_code)

    @NLPIRBase.byte_str_transform
    def exit_lib(self) -> bool:
        """
        Call **NWF_Exit**

        :return: exit success or not
        """
        return self.get_func("NWF_Exit", [None], c_bool)()

    @NLPIRBase.byte_str_transform
    def get_new_words(
            self,
            line: str,
            max_key_limit: int = 50,
            format_opt: int = nlpir_base.OUTPUT_FORMAT_SHARP
    ) -> str:
        """
        Call **NWF_GetNewWords**

        Extract New words from line

        :param str line: the input paragraph

        The input size cannot be very big(less than 60MB).
        Process large memory, recommend use NWF_NWI series functions

        :param str max_key_limit: maximum of key words, up to 50
        :param int format_opt: output format option, there three options:

            - :data:`nlpir.native.nlpir_base.OUTPUT_FORMAT_SHARP` get string split by sharp
            - :data:`nlpir.native.nlpir_base.OUTPUT_FORMAT_JSON` get json format
            - :data:`nlpir.native.nlpir_base.OUTPUT_FORMAT_EXCEL` get csv format

        :return: new words list

        ::

            Sharp format
            "科学发展观/23.80/1#屌丝/12.20/2" with weight
            Json格式如下：
            [
               {
                  "freq" : 152,
                  "pos" : "n_new",
                  "weight" : 77.884208081632579,
                  "word" : "公允价值"
               },
               {
                  "freq" : 71,
                  "pos" : "n_new",
                  "weight" : 75.102183562405372,
                  "word" : "长期股权投资"
               }
            ]

        """
        return self.get_func("NWF_GetNewWords", [c_char_p, c_int, c_bool], c_char_p)(line, max_key_limit, format_opt)

    @NLPIRBase.byte_str_transform
    def get_file_new_words(
            self,
            file_name: str,
            max_key_limit: int = 50,
            format_opt: int = nlpir_base.OUTPUT_FORMAT_SHARP
    ) -> str:
        """
        Call **NWF_GetFileNewWords**

        Extract new words from a text file

        :param str file_name: the path of text file
        :param int max_key_limit: max key want to get
        :param int format_opt: same as :func:`get_new_words`
        :return: same as :func:`get_new_words`
        """
        return self.get_func("NWF_GetFileNewWords", [c_char_p, c_int, c_bool], c_char_p)(
            file_name,
            max_key_limit,
            format_opt
        )

    """
        *  以下函数为2013版本专门针对新词发现的过程，一般建议脱机实现，不宜在线处理
        *  新词识别完成后，再自动导入到分词系统中，即可完成
        *  函数以NWF_NWI(New Word Identification)开头
    """

    @NLPIRBase.byte_str_transform
    def batch_start(self) -> bool:
        """
        Call **NWF_Batch_Start**

        启动新词识别,for very large size of data

        :return: true:success, false:fail
        """
        return self.get_func("NWF_Batch_Start", [None], c_int)()

    @NLPIRBase.byte_str_transform
    def batch_addfile(self, filename: str) -> int:
        """
        Call **NWF_Batch_AddFile**

        往新词识别系统中添加待识别新词的文本文件,需要在运行NWF_Batch_Start()之后，才有效

        :param str filename: the path of file
        :return: 1 success 0 fail
        """
        return self.get_func("NWF_Batch_AddFile", [c_char_p], c_ulong)(filename)

    @NLPIRBase.byte_str_transform
    def batch_addmen(self, text: str) -> int:
        """
        Call **NWF_Batch_AddMem**

        往新词识别系统中添加一段待识别新词的内存,需要在运行NWF_Batch_Start()之后，才有效

        :param str text: text string
        :return: 1 success 0 fail
        """
        return self.get_func("NWF_Batch_AddMem", [c_char_p], c_ulong)(text)

    @NLPIRBase.byte_str_transform
    def batch_complete(self) -> int:
        """
        Call **NWF_Batch_Complete**

        新词识别添加内容结束,需要在运行NWF_Batch_Start()之后，才有效

        :return: 1 success 0 fail
        """
        return self.get_func("NWF_Batch_Complete", None, c_int)()

    @NLPIRBase.byte_str_transform
    def batch_getresult(self, format_json: bool = False) -> str:
        """
        Call **NWF_Batch_GetResult**

        获取新词识别的结果, 需要在运行NWF_Batch_Complete()之后，才有效

        :param bool format_json: get json format or not
        :return: 输出格式为

        ::

            新词1】 【权重1】 【新词2】 【权重2】 ...
            Json格式如下：
            [
               {
                  "freq" : 152,
                  "pos" : "n_new",
                  "weight" : 77.884208081632579,
                  "word" : "公允价值"
               },
               {
                  "freq" : 71,
                  "pos" : "n_new",
                  "weight" : 75.102183562405372,
                  "word" : "长期股权投资"
               }
            ]

        """
        return self.get_func("NWF_Batch_GetResult", [c_bool], c_char_p)(format_json)

    @NLPIRBase.byte_str_transform
    def result2user_dict(self) -> int:
        """
        Call **NWF_Result2UserDict**

        将新词识别结果导入到用户词典中,需要在运行NLPIR_NWI_Complete()之后，才有效.
        如果需要将新词结果永久保存，建议在执行NLPIR_SaveTheUsrDic

        :return: bool, true:success, false:fail
        """
        return self.get_func("NWF_Result2UserDict", None, c_uint)()

    @NLPIRBase.byte_str_transform
    def get_last_error_msg(self) -> str:
        return self.get_func("NWF_GetLastErrorMsg", None, c_char_p)()

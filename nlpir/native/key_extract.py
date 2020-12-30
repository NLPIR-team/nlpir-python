# coding=utf-8
from nlpir.native.nlpir_base import NLPIRBase
from nlpir.native import nlpir_base
from ctypes import c_bool, c_char_p, c_int, c_uint, c_ulong
import typing


class KeyExtract(NLPIRBase):
    """
    A dynamic link library native class for Key Words Extract
    """

    @property
    def dll_name(self) -> str:
        return "KeyExtract"

    @NLPIRBase.byte_str_transform
    def init_lib(self, data_path: str, encode: int, license_code: str) -> int:
        """
        Call **KeyExtract_Init**

        :param str data_path:
        :param int encode:
        :param str license_code:
        :return: 1 success 0 fail
        """
        return self.get_func('KeyExtract_Init', [c_char_p, c_int, c_char_p], c_int)(data_path, encode, license_code)

    def exit_lib(self) -> bool:
        """
        Call **KeyExtract_Exit**

        :return: exit success or not
        """
        return self.get_func('KeyExtract_Exit', restype=c_bool)()

    @NLPIRBase.byte_str_transform
    def get_keywords(self, line: str, max_key_limit: int = 50, format_opt: int = nlpir_base.OUTPUT_FORMAT_SHARP) -> str:
        """
        Call **KeyExtract_GetKeyWords**

        Extract keyword from text, 从文本中获取关键词

        :param line: the input paragraph
        :param max_key_limit: maximum of key words, up to 50
        :param format_opt: output format option, there three options:

            - :data:`nlpir.native.nlpir_base.OUTPUT_FORMAT_SHARP` get string split by sharp
            - :data:`nlpir.native.nlpir_base.OUTPUT_FORMAT_JSON` get json format
            - :data:`nlpir.native.nlpir_base.OUTPUT_FORMAT_EXCEL` get csv format
        :return: the keyword with weight

        Split with ``#``:

        ::

            科学发展观/n/23.80/12#宏观经济/n/12.20/12#

        JSON形式:

        ::

            [
                {
                    'freq': 2,
                    'pos': 'n_new',
                    'weight': 7.771335980376418,
                    'word': '国家权力'
                },{
                    'freq': 7,
                    'pos': 'n',
                    'weight': 7.438759706600493,
                    'word': '权力'
                },{
                    'freq': 1,
                    'pos': 'nrf',
                    'weight': 5.280000338096665,
                    'word': '孟德斯鸠'
                },{ ...
                }, ...
            ]

        """
        return self.get_func('KeyExtract_GetKeyWords', [c_char_p, c_int, c_int], c_char_p)(
            line, max_key_limit, format_opt)

    @NLPIRBase.byte_str_transform
    def get_file_keywords(
            self,
            filename: str,
            max_key_limit: int = 50,
            format_opt: int = nlpir_base.OUTPUT_FORMAT_SHARP
    ) -> str:
        """
        Call **KeyExtract_GetKeyWords**

        Extract keyword from file, 从文本文件中获取关键词

        :param filename: the input text file
        :param max_key_limit: maximum of key words, up to 50
        :param format_opt: same as :func:`get_keywords`
        :return: the keyword with weight

        Split with ``#``

        ::

            科学发展观/n/23.80/12#宏观经济/n/12.20/12#

        JSON形式:

        ::

            [
                {
                    'freq': 2,
                    'pos': 'n_new',
                    'weight': 7.771335980376418,
                    'word': '国家权力'
                },{
                    'freq': 7,
                    'pos': 'n',
                    'weight': 7.438759706600493,
                    'word': '权力'
                },{
                    'freq': 1,
                    'pos': 'nrf',
                    'weight': 5.280000338096665,
                    'word': '孟德斯鸠'
                },{ ...
                }, ...
            ]

        """
        return self.get_func('KeyExtract_GetFileKeyWords', [c_char_p, c_int, c_int], c_char_p)(
            filename, max_key_limit, format_opt)

    @NLPIRBase.byte_str_transform
    def import_user_dict(self, filename: str, overwrite: bool = False):
        """
        Call **KeyExtract_ImportUserDict**

        Import a user dict to the system, the format of the dict file::

            word1 pos_tag
            word2 pos_tag

        If you import a user dict to the system, the user dict will save to the system (in Data directory).
        You cannot delete the word in the user dict from the system use :func:`clean_user_word` or :func:`del_usr_word`.

        :param str filename: the path of user dict file
        :param bool overwrite: overwrite the current user dict or not
        :return: import success or not  1->True 2->False
        """
        return self.get_func('KeyExtract_ImportUserDict', [c_char_p, c_bool], c_uint)(filename, overwrite)

    @NLPIRBase.byte_str_transform
    def add_user_word(self, word: str) -> int:
        """
        Call **KeyExtract_AddUserWord**

        Add a word to the user dictionary ,example::

            单词 词性

        or::

            单词 (default n)

        The added word only add in memory and will not affect the user dict, you can use :func:`clean_user_word` or
        :func:`del_usr_word` to delete the word or all the words in memory. If you want to save to the user dict ,use
        :func:`save_the_usr_dic` to save to the *Data* directory.

        :param str word:
        :return: 1,true ; 0,false
        """
        return self.get_func('KeyExtract_AddUserWord', [c_char_p], c_int)(word)

    @NLPIRBase.byte_str_transform
    def clean_user_word(self) -> int:
        """
        Call **KeyExtract_CleanUserWord**

        Clean all temporary added user words, more info see :func:`add_user_word`

        :return: 1,true ; 0,false
        """
        return self.get_func('KeyExtract_CleanUserWord', None, c_int)()

    @NLPIRBase.byte_str_transform
    def save_the_usr_dic(self) -> int:
        """
        Call **KeyExtract_SaveTheUsrDic**

        Save in-memory dict to user dict, more info see :func:`add_user_word`

        :return: 1,true; 2,false
        """
        return self.get_func('KeyExtract_SaveTheUsrDic', None, c_int)()

    @NLPIRBase.byte_str_transform
    def del_usr_word(self, word: str) -> int:
        """
        Call **KeyExtract_DelUsrWord**

         Delete a word from the user dictionary, more info see :func:`add_user_word`

        :param str word: the word to be delete
        :return: -1, the word not exist in the user dictionary; else, the handle of the word deleted
        """
        return self.get_func('KeyExtract_DelUsrWord', [c_char_p], c_int)(word)

    @NLPIRBase.byte_str_transform
    def import_key_blacklist(self, filename: str, pos_blacklist: typing.Optional[str] = None) -> int:
        """
        Call **KeyExtract_ImportKeyBlackList**

        Import keyword black list

        This function will save words to KeyBlackList.pdat , if you want to remove the words form the system
        need to backup it before use this function. Or use the function :func:`nlpir.key_extract.import_blacklist` ,
        That function will backup that file automatically and you can use :func:`nlpir.key_extract.clean_blacklist` to
        clean current blacklist and restore the origin file.

        This list of word will not affect the key word extract and segmentation

        :param filename: A word list that the words want to import to the blacklist (stop word list),
            一个停用词词表,里面为想进行屏蔽的词,也可以包括别的词,是否不进行抽取是按照词表中的词性来确定的.
        :param pos_blacklist: A list of pos that want to block in the system, 想要屏蔽的词的词性
        :return: number of words that import to the systems
        """
        return self.get_func('KeyExtract_ImportKeyBlackList', [c_char_p, c_char_p], c_uint)(filename, pos_blacklist)

    """
    /*********************************************************************
    *
    以下函数为2013版本专门针对关键词批量发现的过程，一般建议脱机实现，不宜在线处理
    *********************************************************************/
    """

    @NLPIRBase.byte_str_transform
    def batch_start(self) -> int:
        """
        Call **KeyExtract_Batch_Start**

        启动关键词识别

        :return: rue:success, false:fail
        """
        return self.get_func('KeyExtract_Batch_Start', None, c_int)()

    @NLPIRBase.byte_str_transform
    def batch_add_file(self, filename) -> int:
        """
        Call **KeyExtract_Batch_AddFile**

        往关键词识别系统中添加待识别关键词的文本文件, 需要在运行 :func:`batch_start` 之后，才有效

        :param filename: 文件名
        :return: true:success, false:fail
        """
        return self.get_func('KeyExtract_Batch_AddFile', [c_char_p], c_ulong)(filename)

    @NLPIRBase.byte_str_transform
    def batch_addmen(self, txt: str) -> bool:
        """
        Call **KeyExtract_Batch_AddMem**

        往关键词识别系统中添加一段待识别关键词的内存,需要在运行 :func:`batch_start` 之后，才有效

        :param txt: 文件名
        :return:  true:success, false:fail
        """
        return self.get_func('KeyExtract_Batch_AddMem', [c_char_p], c_bool)(txt)

    @NLPIRBase.byte_str_transform
    def batch_complete(self) -> int:
        """
        Call **KeyExtract_Batch_Complete**

        关键词识别添加内容结束,需要在运行 :func:`batch_start` 之后，才有效

        :return: true:success, false:fail
        """
        return self.get_func('KeyExtract_Batch_Complete', None, c_int)()

    @NLPIRBase.byte_str_transform
    def batch_getresult(self, weight_out: bool) -> str:
        """
        Call **KeyExtract_Batch_GetResult**

        获取关键词识别的结果,需要在运行 :func:`batch_complete` 之后，才有效

        :param weight_out: 是否需要输出每个关键词的权重参数
        :return:  输出格式为 【关键词1】 【权重1】 【关键词2】 【权重2】 ...
        """
        return self.get_func('KeyExtract_Batch_GetResult', [c_bool], str)(weight_out)

    @NLPIRBase.byte_str_transform
    def get_last_error_msg(self) -> str:
        """
        Call **KeyExtract_GetLastErrorMsg**

        :return: error message
        """
        return self.get_func("KeyExtract_GetLastErrorMsg", None, c_char_p)()

# coding=utf-8
from nlpir.native.nlpir_base import NLPIRBase
from ctypes import c_bool, c_char, c_char_p, c_double, c_int, c_uint, POINTER, Structure, byref
import typing


class ResultT(Structure):
    """The NLPIR ``result_t`` structure. copy from pynlpir"""

    _fields_ = [
        # The start position of the word in the source Chinese text string.
        ('start', c_int),

        # The detected word's length.
        ('length', c_int),

        # A string representing the word's part of speech.
        ('sPOS', c_char * 40),

        ('iPOS', c_int),

        ('word_ID', c_int),

        # If the word is found in the user's dictionary.
        ('word_type', c_int),

        # The weight of the detected word.
        ('weight', c_int)
    ]


class ICTCLAS(NLPIRBase):
    """
    A dynamic link library native class for Chinese Segmentation
    """
    POS_MAP_NUMBER = 4  # add by qp 2008.11.25
    ICT_POS_MAP_FIRST = 1  # 计算所一级标注集
    ICT_POS_MAP_SECOND = 0  # 计算所二级标注集
    PKU_POS_MAP_SECOND = 2  # 北大二级标注集
    PKU_POS_MAP_FIRST = 3  # 北大一级标注集
    POS_SIZE = 40

    @property
    def dll_name(self) -> str:
        return "NLPIR"

    @NLPIRBase.byte_str_transform
    def init_lib(self, data_path: str, encode: int, license_code: str) -> int:
        """
        Call **NLPIR_Init**

        :param str data_path:
        :param int encode:
        :param str license_code:
        :return: 1 success 0 fail
        """
        return self.get_func('NLPIR_Init', [c_char_p, c_int, c_char_p], c_int)(data_path, encode, license_code)

    def exit_lib(self) -> bool:
        """
        Call **NLPIR_Exit**

        :return: exit success or not
        """
        return self.get_func('NLPIR_Exit', restype=c_bool)()

    @NLPIRBase.byte_str_transform
    def paragraph_process(self, paragraph: str, pos_tagged: int = 1) -> str:
        """
         Call **NLPIR_ParagraphProcessing**

         Chinese word segment, segment paragraph to a string

        :param str paragraph: the string want to be segmented
        :param int pos_tagged: show the pos tag or not 1-> True, 0-> False
        :return: segmented string
        """
        return self.get_func('NLPIR_ParagraphProcess', [c_char_p, c_int], c_char_p)(paragraph, pos_tagged)

    @NLPIRBase.byte_str_transform
    def paragraph_process_a(self, paragraph: str, user_dict: bool = True) -> typing.Tuple[ResultT, int]:
        """
        Call **ParagraphProcessingA**

        Segment paragraph to an Array of ResultT, get more detail info

        :param str paragraph: the string want to be segmented
        :param bool user_dict: use user dictionary or not
        :return: a result of segment, an array of ResultT and the length of the ResultT
        """
        self.logger.warning("not recommended, use paragraph_process instead")
        result_count = c_int()
        result = self.get_func('NLPIR_ParagraphProcessA', [c_char_p, POINTER(c_int), c_bool], POINTER(ResultT))(
            paragraph,
            byref(result_count),
            user_dict
        )
        return result, result_count.value

    @NLPIRBase.byte_str_transform
    def get_paragraph_process_a_word_count(self, paragraph: str) -> int:
        raise NotImplementedError("Not recommended, use paragraph_process")

    @NLPIRBase.byte_str_transform
    def paragraph_process_aw(self, count: int, result: ResultT) -> None:
        raise NotImplementedError("Not recommended, use paragraph_process")

    @NLPIRBase.byte_str_transform
    def file_process(self, source_filename: str, result_filename: str, pos_tagged: int = 1) -> float:
        """
        Call **NLPIR_FileProcess**

        Segment a text file and save to a file.

        :param str source_filename: the path of a text file that want to be segmented
        :param str result_filename: the path to save the result of segmentation
        :param int pos_tagged: show the pos tag or not 1->True, 0->False
        """
        return self.get_func('NLPIR_FileProcess', [c_char_p, c_char_p, c_int], c_double)(
            source_filename,
            result_filename,
            pos_tagged
        )

    @NLPIRBase.byte_str_transform
    def import_user_dict(self, filename: str, overwrite: bool = False) -> int:
        """
        Call **NLPIR_ImportUserDict**

        Import a user dict to the system, the format of the dict file::

            word1 pos_tag
            word2 pos_tag

        If you import a user dict to the system, the user dict will save to the system (in Data directory).
        You cannot delete the word in the user dict from the system use :func:`clean_user_word` or :func:`del_usr_word`.

        **TODO** add more comment for clean the user dict and add the function to the high-level method

        :param str filename: the path of user dict file
        :param bool overwrite: overwrite the current user dict or not
        :return: import success or not  1->True 2->False
        """
        return self.get_func('NLPIR_ImportUserDict', [c_char_p, c_bool], c_uint)(filename, overwrite)

    @NLPIRBase.byte_str_transform
    def add_user_word(self, word: str) -> int:
        """
        Call **NLPIR_AddUserWord**

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
        return self.get_func('NLPIR_AddUserWord', [c_char_p], c_int)(word)

    @NLPIRBase.byte_str_transform
    def clean_user_word(self) -> int:
        """
        Call **NLPIR_CleanUserWord**

        Clean all temporary added user words, more info see :func:`add_user_word`
        TODO figure out the return value
        :return: 1,true ; 0,false
        """
        return self.get_func('NLPIR_CleanUserWord', None, c_int)()

    @NLPIRBase.byte_str_transform
    def save_the_usr_dic(self) -> int:
        """
        Call **NLPIR_SaveTheUsrDic**

        Save in-memory dict to user dict, more info see :func:`add_user_word`

        :return: 1,true; 2,false
        """
        return self.get_func('NLPIR_SaveTheUsrDic', None, c_int)()

    @NLPIRBase.byte_str_transform
    def del_usr_word(self, word: str) -> int:
        """
        Call **NLPIR_DelUsrWord**

        Delete a word from the user dictionary, more info see :func:`add_user_word`

        :param str word: the word to be delete
        :return: -1, the word not exist in the user dictionary; else, the handle of the word deleted
        """
        return self.get_func('NLPIR_DelUsrWord', [c_char_p], c_int)(word)

    @NLPIRBase.byte_str_transform
    def get_uni_prob(self, word) -> float:
        """
        Call **NLPIR_GetUniProb**

        Get Unigram Probability

        :param str word: input word
        :return: The unitary probability of a word.
        """

        return self.get_func("NLPIR_GetUniProb", [c_char_p], c_double)(word)

    @NLPIRBase.byte_str_transform
    def is_word(self, word: str) -> int:
        """
        Call **NLPIR_IsWord**

        Judge whether the word is included in the core dictionary

        :param str word: input word
        :return: 1: exists; 0: no exists
        """
        return self.get_func("NLPIR_IsWord", [c_char_p], c_int)(word)

    @NLPIRBase.byte_str_transform
    def is_user_word(self, word: str, is_ascii: bool = False) -> int:
        """
        Call **NLPIR_IsUserWord**

        Judge whether the word is included in the user-defined dictionary

        :param str word: input word
        :param bool is_ascii: is ascii encode or not
        :return: 1: exists; 0: no exists
        """
        return self.get_func("NLPIR_IsUserWord", [c_char_p], c_int)(word, is_ascii)

    @NLPIRBase.byte_str_transform
    def get_word_pos(self, word: str) -> str:
        """
        Call **NLPIR_GetWordPOS**

        Get the word Part-Of-Speech information

        :param str word: input word
        :return: pos tagging
        """
        return self.get_func("NLPIR_GetWordPOS", [c_char_p], c_char_p)(word)

    def set_pos_map(self, pos_map: int) -> int:
        """
        Call **NLPIR_SetPOSmap**

        Select which pos map will use:

        - :attr:`ICT_POS_MAP_FIRST`   计算所一级标注集
        - :attr:`ICT_POS_MAP_SECOND`  计算所二级标注集
        - :attr:`PKU_POS_MAP_SECOND`  北大二级标注集
        - :attr:`PKU_POS_MAP_FIRST`   北大一级标注集

        Default is :attr:`ICT_POS_MAP_SECOND`

        :param int pos_map:
        :return: 0, failed; else, success
        """
        return self.get_func("NLPIR_SetPOSmap")(pos_map)

    @NLPIRBase.byte_str_transform
    def finer_segment(self, line: str) -> str:
        """
        Call **NLPIR_FinerSegment**

        当前的切分结果过大时,如“中华人民共和国”, 需要执行该函数,将切分结果细分为“中华 人民 共和国”

        细分粒度最大为三个汉字,如果不能细分，则返回为空字符串

        :param str line: string need to be segmented
        :return: segmented string, return null string if line cannot be segmented
        """
        return self.get_func("NLPIR_FinerSegment", [c_char_p], c_char_p)(line)

    @NLPIRBase.byte_str_transform
    def get_eng_word_origin(self, word: str) -> str:
        """
        Call **NLPIR_GetEngWordOrign**

        获取各类英文单词的原型，考虑了过去分词、单复数等情况::

            driven->drive   drives->drive   drove-->drive

        :param str word: word to be stemmed
        :return: the stemmed word
        """
        return self.get_func("NLPIR_GetEngWordOrign", [c_char_p], c_char_p)(word)

    @NLPIRBase.byte_str_transform
    def word_freq_stat(self, text: str, stop_word_remove: bool = True) -> str:
        """
        Call **NLPIR_WordFreqStat**

        获取输入文本的词，词性，频统计结果，按照词频大小排序

        :param str text: 输入的文本内容
        :param bool stop_word_remove: true-去除停用词 false-不去除停用词
        :return: 返回的是词频统计结果形式如下

        ::

            张华平/nr/10#博士/n/9#分词/n/8
        """
        return self.get_func("NLPIR_WordFreqStat", [c_char_p, c_bool], c_char_p)(text, stop_word_remove)

    @NLPIRBase.byte_str_transform
    def file_word_freq_stat(self, filename: str, stop_word_remove: bool = True) -> str:
        """
        Call **NLPIR_FileWordFreqStat**

        Same as :func:`word_freq_stat`

        :param str filename: path of text file
        :param bool stop_word_remove: remove stop words or not
        :return: same as :func:`word_freq_stat`
        """
        return self.get_func("NLPIR_FileWordFreqStat", [c_char_p, c_bool], c_char_p)(filename, stop_word_remove)

    @NLPIRBase.byte_str_transform
    def get_last_error_msg(self) -> str:
        """
        Call **NLPIR_GetLastErrorMsg**

        :return: error message
        """
        return self.get_func("NLPIR_GetLastErrorMsg", None, c_char_p)()

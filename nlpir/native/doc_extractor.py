# coding=utf-8
from nlpir.native.nlpir_base import NLPIRBase
from ctypes import c_bool, c_char_p, c_int, c_uint, c_size_t


DOC_EXTRACT_TYPE_PERSON = 0  #: 人名
DOC_EXTRACT_TYPE_LOCATION = 1  #: 地名
DOC_EXTRACT_TYPE_ORGANIZATION = 2  #: 机构名
DOC_EXTRACT_TYPE_KEYWORD = 3  #: 关键词
DOC_EXTRACT_TYPE_AUTHOR = 4  #: 文章作者
DOC_EXTRACT_TYPE_MEDIA = 5  #: 媒体
DOC_EXTRACT_TYPE_COUNTRY = 6  #: 文章对应的所在国别
DOC_EXTRACT_TYPE_PROVINCE = 7  #: 文章对应的所在省份
DOC_EXTRACT_TYPE_ABSTRACT = 8  #: 文章的摘要
DOC_EXTRACT_TYPE_POSITIVE = 9  #: 文章的正面情感词
DOC_EXTRACT_TYPE_NEGATIVE = 10  #: 文章的负面情感词
DOC_EXTRACT_TYPE_TEXT = 11  #: 文章去除网页等标签后的正文
DOC_EXTRACT_TYPE_TIME = 12  #: 时间词
#: 用户自定义的词类，第一个自定义词
#: 后续的自定义词，依次序号为：:data:`DOC_EXTRACT_TYPE_USER` + 1 , :data:`DOC_EXTRACT_TYPE_USER` + 2 , ...
DOC_EXTRACT_TYPE_USER = 13

PERSON_REQUIRED = 0x0001
LOCATION_REQUIRED = 0x0002
ORGANIZATION_REQUIRED = 0x0004
KEYWORD_REQUIRED = 0x0008
AUTHOR_REQUIRED = 0x0010
MEDIA_REQUIRED = 0x0100
COUNTRY_REQUIRED = 0x0200
PROVINCE_REQUIRED = 0x0400
ABSTRACT_REQUIRED = 0x0800
SENTIWORD_REQUIRED = 0x1000
SENTIMENT_REQUIRED = 0x2000
TIME_REQUIRED = 0x4000
HTML_REMOVER_REQUIRED = 0x8000  #: 是否需要去除网页标签的功能选项
ALL_REQUIRED = 0xffff


class DocExtractor(NLPIRBase):
    """
    A dynamic link library native class for Document Extractor
    """

    DOC_EXTRACT_DELIMITER = "#"  #: 分隔符
    DOC_EXTRACT_TYPE_MAX_LENGTH = 600  # 最大长度

    @property
    def dll_name(self) -> str:
        return "DocExtractor"

    @NLPIRBase.byte_str_transform
    def init_lib(self, data_path: str, encode: int, license_code: str) -> int:
        """
        Call **DE_Init**

        :param str data_path:
        :param int encode:
        :param str license_code:
        :return: 1 success 0 fail
        """
        return self.get_func('DE_Init', [c_char_p, c_int, c_char_p], c_int)(data_path, encode, license_code)

    def exit_lib(self) -> bool:
        """
        Call **DE_Exit**

        :return: exit success or not
        """
        return self.get_func('DE_Exit', restype=c_bool)()

    @NLPIRBase.byte_str_transform
    def get_last_error_msg(self) -> str:
        """
        Call **DE_GetLastErrorMsg**

        :return: error message
        """
        return self.get_func("DE_GetLastErrorMsg", None, c_char_p)()

    @NLPIRBase.byte_str_transform
    def pares_doc_e(
            self, text: str,
            user_def_pos: str,
            summary_needed: bool = True,
            func_required: int = ALL_REQUIRED
    ) -> int:
        """
        Call **DE_ParseDocE**

        生成单文档摘要

        :param text: 文档内容
        :param user_def_pos: 用户自定义的词性标记, 最多三种（人名、地名、机构名、媒体等内置，无需设置, 不同词类之间采用#分割,
            如 ``gms#gjtgj#g``
        :param summary_needed: 是否需要计算摘要
        :param func_required:
        :return: 用于获取内容的handle, 获取内容完毕后应使用 :func:`release_handle` 释放对应资源
        """
        return self.get_func("DE_ParseDocE", [c_char_p, c_char_p, c_bool, c_uint], c_size_t)(
            text, user_def_pos, summary_needed, func_required
        )

    @NLPIRBase.byte_str_transform
    def release_handle(self, handle: int) -> None:
        """
        Call **DE_ReleaseHandle**

        释放 :func:`parse_doc_e` 结果所占据的空间

        :param handle: :func:`parse_doc_e` 执行后返回的HANDLE
        :return:
        """
        return self.get_func("DE_ReleaseHandle", [c_size_t], None)(handle)

    @NLPIRBase.byte_str_transform
    def get_result(self, handle: int, doc_extract_type: int) -> str:
        """
        Call **DE_GetResult**

        从运行完的 :func:`parse_doc_e` 结果中，获取指定抽取的结果内容

        :param handle: :func:`parse_doc_e` 执行后返回的HANDLE
        :param doc_extract_type: 获取的抽取类型，从DOC_EXTRACT_TYPE_PERSON开始的结果
        :return:
        """
        return self.get_func("DE_GetResult", [c_size_t, c_int], c_char_p)(handle, doc_extract_type)

    @NLPIRBase.byte_str_transform
    def get_sentiment_score(self, handle: int) -> int:
        """
        Call **DE_GetSentimentScore**

        从运行完的 :func:`parse_doc_e` 结果中，获取指文章的情感得分

        :param handle: :func:`parse_doc_e` 执行后返回的HANDLE
        :return: 情感正负得分
        """
        return self.get_func("DE_GetSentimentScore", [c_size_t], c_int)(handle)

    @NLPIRBase.byte_str_transform
    def compute_sentiment_doc(self, text: str) -> int:
        """
        Call **DE_ComputeSentimentDoc**

        生成单文档情感分析结果

        :param text: 文档内容
        :return:
        """
        return self.get_func("DE_ComputeSentimentDoc", [c_char_p], c_int)(text)

    @NLPIRBase.byte_str_transform
    def import_sentiment_dict(self, filename: str) -> int:
        """
        Call **DE_ImportSentimentDict**

        导入用户自定义的情感词表，每行一个词，空格后加上正负权重，如: ``语焉不详 -2``

        若导入的情感词属于新词, 需先在用户词典中导入, 否则情感识别自动跳跃

        :param filename:
        :return:
        """
        return self.get_func("DE_ImportSentimentDict", [c_size_t], c_int)(filename)

    @NLPIRBase.byte_str_transform
    def import_user_dict(self, filename: str, overwrite: bool = False) -> int:
        """
        Call **DE_ImportUserDict**

        导入用户词典, see :func:`nlpir.native.ictclas.ICTCLAS.import_user_dict`

        :param filename:
        :param overwrite:
        :return:
        """
        return self.get_func("DE_ImportUserDict", [c_char_p, c_bool], c_uint)(filename, overwrite)

    @NLPIRBase.byte_str_transform
    def add_user_word(self, word: str) -> int:
        """
        Call **DE_AddUserWord**

        Add a word to the user dictionary, see :func:`nlpir.native.ictclas.ICTCLAS.add_user_word`

        :param word:
        :return:
        """
        return self.get_func("DE_AddUserWord", [c_char_p], c_int)(word)

    @NLPIRBase.byte_str_transform
    def clean_user_word(self) -> int:
        """
        Call **DE_CleanUserWord**

        Clean all temporary added user words, see :func:`nlpir.native.ictclas.ICTCLAS.clean_user_word`

        :return:
        """
        return self.get_func("DE_CleanUserWord", None, c_int)()

    @NLPIRBase.byte_str_transform
    def save_the_usr_dic(self) -> int:
        """
        Call **DE_SaveTheUsrDic**

        Save in-memory dict to user dict, see :func:`nlpir.native.ictclas.ICTCLAS.save_the_usr_dic`
        :return:
        """
        return self.get_func("DE_SaveTheUsrDic", None, c_int)()

    @NLPIRBase.byte_str_transform
    def del_usr_word(self, word: str) -> int:
        """
        Call **DE_DelUsrWord**

        Delete a word from the user dictionary, see :func:`nlpir.native.ictclas.ICTCLAS.del_usr_word`

        :param word:
        :return:
        """
        return self.get_func("DE_DelUsrWord", [c_char_p], c_int)(word)

    @NLPIRBase.byte_str_transform
    def import_key_blacklist(self, filename: str, pos_blacklist: str) -> int:
        """
        Call **DE_ImportKeyBlackList**

        Import keyword black list, see :func:`nlpir.native.key_extract.KeyExtract.import_key_blacklist`

        :param filename:
        :param pos_blacklist:
        :return:
        """
        return self.get_func("DE_ImportKeyBlackList", [c_char_p, c_char_p], c_uint)(filename, pos_blacklist)

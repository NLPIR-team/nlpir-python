# coding=utf-8
from nlpir.native.nlpir_base import NLPIRBase
from ctypes import c_bool, c_char, c_char_p, c_double, c_int, c_uint, POINTER, Structure, byref, create_string_buffer
import typing


class SentimentNew(NLPIRBase):
    @property
    def dll_name(self):
        return "SentimentNew"

    @NLPIRBase.byte_str_transform
    def init_lib(self, data_path: str, encode: int, license_code: str) -> int:
        """
        Func Name  : ST_Init

        Description: Init ST_Init
        The function must be invoked before any operation listed as following

        Parameters : const char * sInitDirPath=NULL
        sDataPath:  Path where Data directory stored.
        the default value is NULL, it indicates the initial directory is current working directory path
        encode: encoding code;
        sLicenseCode: license code for unlimited usage. common user ignore it
        Returns    : success or fail
        Author     : Kevin Zhang
        History    :
        1.create 2013-6-8
        :param data_path:
        :param encode:
        :param license_code:
        :return:
        """
        return self.get_func("ST_Init", [c_char_p, c_int, c_char_p], c_int)(data_path, encode, license_code)

    @NLPIRBase.byte_str_transform
    def exit_lib(self) -> bool:
        """
        Func Name  : ST_Exit

        Description: Exist ST and free related buffer
        Exit the program and free memory
        The function must be invoked while you needn't any lexical anlysis
        :return:
        """
        return self.get_func("ST_Exit", None, c_int)()

    @NLPIRBase.byte_str_transform
    def get_last_error_msg(self) -> str:
        """

        :return:
        """
        return self.get_func("ST_GetLastErrMsg", None, c_char_p)()

    @NLPIRBase.byte_str_transform
    def get_one_object_result(self, title: str, content: str, analysis_object: str):
        """

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
    def get_multi_object_result(self, title: str, content: str, object_rule_file: str):
        """
        Func Name  : ST_GetMultiObjectResult

        Description: Get multiple object sentimental result

        Parameters : sTitle: document title
                   sContent: document content
                   sObjectRuleFile: see Appendix II: Multiple Object configure sample

        Returns    : const char * result buffer
                   sample see  Appendix I:Sentimental analysis result sample
        Author     : Kevin Zhang
        History    :
                  1.create 2016-3-20
        :param title:
        :param content:
        :param object_rule_file:
        :return:
        """
        return self.get_func("ST_GetMultiObjectResult", [c_char_p, c_char_p, c_char_p], c_char_p)(
            title, content, object_rule_file
        )

    @NLPIRBase.byte_str_transform
    def get_sentence_point(self, sentence: str):
        """

        Func Name  : ST_GetSentimentPoint

        Description: Get multiple object sentimental result

        Parameters : sSentence: sentence memory

        Returns    : const char * result buffer
                   sample see  Appendix I:Sentimental analysis result sample
        Author     : Kevin Zhang
        History    :
                  1.create 2016-3-20
        :param sentence:
        :return:
        """
        return self.get_func("ST_GetSentimentPoint", [c_char_p], c_double)(sentence)

    """

        Func Name  : ST_GetSentimentPoint

        Description: Get multiple object sentimental result

        Parameters : sSentence: sentence memory

        Returns    : double,Sentimental point
        Author     : Kevin Zhang  
        History    : 
                  1.create 2016-3-20

        ST_API double ST_GetSentimentPoint(const char *sSentence);
    """

    @NLPIRBase.byte_str_transform
    def import_user_dict(self, filename: str, over_write: bool = False):
        """
        Func Name  : ST_ImportUserDict

        Description: Import User-defined dictionary
        Parameters :
                    sFilename:Text filename for user dictionary
                    bOverwrite: true,  overwrite the existing dictionary
                               false, add to  the existing dictionary
        Returns    : The  number of  lexical entry imported successfully
        Author     : Kevin Zhang
        History    :
                  1.create 2014-8-3
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

        :param data_path:
        :param encode:
        :param license_code:
        :return:
        """
        return self.get_func("LJST_Inits", [c_char_p, c_int, c_char_p], c_int)(data_path, encode, license_code)

    @NLPIRBase.byte_str_transform
    def exit_lib(self) -> bool:
        """

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
    def get_paragraph_sent(self, paragraph: str):
        """

        :param paragraph:
        :return:
        """
        result = create_string_buffer(10240)
        result_bool = self.get_func("LJST_GetParagraphSent", [c_char_p, c_char_p], c_bool)(paragraph, result)
        return result_bool, result.value

    @NLPIRBase.byte_str_transform
    def get_file_sent(self, filename: str):
        """

        :param filename:
        :return:
        """
        result = c_char_p()
        result_bool = self.get_func("LJST_GetFileSent", [c_char_p, c_char_p], c_bool)(filename, byref(result))
        return result_bool, result.value

    @NLPIRBase.byte_str_transform
    def import_user_dict(self, filename: str, over_write: bool = False):
        """

        :param filename:
        :param over_write:
        :return:
        """
        return self.get_func("LJST_ImportUserDict", [c_char_p, c_bool], c_int)(filename, over_write)

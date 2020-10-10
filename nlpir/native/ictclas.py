# coding=utf-8
from nlpir.native.nlpir_base import NLPIRBase
from ctypes import c_bool, c_char, c_char_p, c_double, c_int, c_uint, POINTER, Structure, byref
import typing


class ResultT(Structure):
    """The NLPIR ``result_t`` structure."""

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
    POS_MAP_NUMBER = 4  # add by qp 2008.11.25
    ICT_POS_MAP_FIRST = 1  # 计算所一级标注集
    ICT_POS_MAP_SECOND = 0  # 计算所二级标注集
    PKU_POS_MAP_SECOND = 2  # 北大二级标注集
    PKU_POS_MAP_FIRST = 3  # 北大一级标注集
    POS_SIZE = 40

    @property
    def dll_name(self) -> str:
        return "ICTCLAS"

    @NLPIRBase.byte_str_transform
    def init_lib(self, data_path: str, encode: int, license_code: str) -> int:
        """
        所有子类都需要实现此方法用于类初始化实例时调用, 由于各个库对应初始化不同,故改变此函数名称
        /*********************************************************************
         *
         *  Func Name  : Init
         *
         *  Description: Init NLPIR
         *               The function must be invoked before any operation listed as following
         *
         *  Parameters : const char * sInitDirPath=NULL
         *               sDataPath:  Path where Data directory stored.
         *               the default value is NULL, it indicates the initial directory is current working directory path
         *               encode: encoding code;
         *               sLicenseCode: license code for unlimited usage. common user ignore it
         *  Returns    : success or fail
         *  Author     : Kevin Zhang
         *  History    :
         *               1.create 2013-6-8
         *********************************************************************/
         NLPIR_API int NLPIR_Init(const char * sDataPath=0,int encode=GBK_CODE,const char*sLicenceCode=0);
        """
        return self.get_func('NLPIR_Init', [c_char_p, c_int, c_char_p], c_int)(data_path, encode, license_code)

    def exit_lib(self) -> bool:
        """
        所有子类都需要实现此方法用于类析构(销毁)实例时调用, 由于各个库对应初始化不同,故改变此函数名称
        /*********************************************************************
         *
         *  Func Name  : NLPIR_Exit
         *
         *  Description: Exist NLPIR and free related buffer
         *               Exit the program and free memory
         *               The function must be invoked while you needn't any lexical anlysis
         *
         *  Parameters : None
         *
         *  Returns    : success or fail
         *  Author     : Kevin Zhang
         *  History    :
         *              1.create 2002-8-6
         *********************************************************************/"""
        return self.get_func('NLPIR_Exit', restype=c_bool)()

    @NLPIRBase.byte_str_transform
    def paragraph_process(self, paragraph: str, pos_tagged: int = 1) -> str:
        """
        /*********************************************************************
         *
         *  Func Name  : ParagraphProcessing
         *
         *  Description: Process a paragraph
         *
         *  Parameters : sParagraph: The source paragraph
         *               bPOStagged:Judge whether need POS tagging, 0 for no tag;default:1
         *               i.e.  张华平于1978年3月9日出生于江西省波阳县。
         *                    Result: 张华平/nr  于/p  1978年/t  3月/t  9日/t  出生于/v  江西省/ns  波阳县/ns  。/w
         *  Returns    : the result buffer pointer
         *
         *  Author     : Kevin Zhang
         *  History    :
         *               1.create 2003-12-22
         *********************************************************************/
        NLPIR_API const char * NLPIR_ParagraphProcess(const char *sParagraph,int bPOStagged=1);
        """
        return self.get_func('NLPIR_ParagraphProcess', [c_char_p, c_int], c_char_p)(paragraph, pos_tagged)

    @NLPIRBase.byte_str_transform
    def paragraph_process_a(self, paragraph: str, user_dict: bool = True) -> typing.Tuple[ResultT, int]:
        """
        /*********************************************************************
         *
         *  Func Name  : ParagraphProcessingA
         *
         *  Description: Process a paragraph
         *
         *  Parameters : sParagraph: The source paragraph
         *               pResultCount: pointer to result vector size
         *  Returns    : the pointer of result vector, it is managed by system,user cannot alloc and free it
         *  Author     : Kevin Zhang
         *  History    :
         *              1.create 2006-10-26
         *********************************************************************/
        NLPIR_API const result_t * NLPIR_ParagraphProcessA(const char *sParagraph,int *pResultCount,bool bUserDict=true);
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
        """
        /*********************************************************************
         *
         *  Func Name  : NLPIR_GetParagraphProcessAWordCount
         *
         *  Description: Get ProcessAWordCount, API for C#
         *               Get word count and it helps us prepare the proper size buffer for result_t vector
         *
         *  Parameters : sParagraph: The source paragraph
         *
         *  Returns    : result vector size
         *  Author     : Kevin Zhang
         *  History    :
         *              1.create 2007-3-15
         *********************************************************************/
         NLPIR_API int NLPIR_GetParagraphProcessAWordCount(const char *sParagraph);
        """
        raise NotImplementedError("Not recommended, use paragraph_process")

    @NLPIRBase.byte_str_transform
    def paragraph_process_aw(self, count: int, result: ResultT) -> None:
        """
        /*********************************************************************
         *
         *  Func Name  : NLPIR_ParagraphProcessAW
         *
         *  Description: Process a paragraph, API for C#
         *
         *
         *  Parameters : nCount: the paragraph word count.
         *               result_t * result: pointer to result vector size, it is allocated by the invoker
         *  Returns    : None
         *  Author     :
         *  History    :
         *              1.create 2007-3-15
         *********************************************************************/
        NLPIR_API void NLPIR_ParagraphProcessAW(int nCount,result_t * result);

        """
        raise NotImplementedError("Not recommended, use paragraph_process")

    @NLPIRBase.byte_str_transform
    def file_process(self, source_filename: str, result_filename: str, pos_tagged: bool = 1) -> float:
        """
        /*********************************************************************
         *
         *  Func Name  : NLPIR_FileProcess
         *
         *  Description: Process a text file
         *
         *  Parameters : sSourceFilename: The source file name
         *               sResultFilename: The result file name
         *               bPOStagged:Judge whether need POS tagging, 0 for no tag;default:1
         *              i.e. FileProcess("199802_Org.txt","199802_Org_cla.txt");
         *  Returns    : success:
         *               fail:
         *  Author     : Kevin Zhang
         *  History    :
         *              1.create 2005-11-22
         *********************************************************************/
        NLPIR_API double NLPIR_FileProcess(const char *sSourceFilename,const char *sResultFilename,int bPOStagged=1);
        """
        return self.get_func('NLPIR_FileProcess', [c_char_p, c_char_p, c_int], c_double)(
            source_filename,
            result_filename,
            pos_tagged
        )

    @NLPIRBase.byte_str_transform
    def import_user_dict(self, filename: str, overwrite: bool = False) -> int:
        """
        /*********************************************************************
         *
         *  Func Name  : ImportUserDict
         *
         *  Description: Import User-defined dictionary
         *  Parameters : sFilename:Text filename for user dictionary
         *               bOverwrite: true, overwrite the existing dictionary
         *               false, add to the existing dictionary
         *  Returns    : The number of lexical entry imported successfully
         *  Author     : Kevin Zhang
         *  History    :
         *              1.create 2014-8-3
         *********************************************************************/
        NLPIR_API unsigned int NLPIR_ImportUserDict(const char *sFilename,bool bOverwrite=false);
        """
        return self.get_func('NLPIR_ImportUserDict', [c_char_p], c_uint)(filename, overwrite)

    @NLPIRBase.byte_str_transform
    def add_user_word(self, word: str) -> int:
        """
        /*********************************************************************
        *
        *  Func Name  : NLPIR_AddUserWord
        *
        *  Description: add a word to the user dictionary ,example:
        *                               你好 i3s n
        *
        *  Parameters : sWord:the word added.
        *
        *  Returns    : 1,true ; 0,false
        *
        *  Author     :
        *  History    :
        *              1.create 11:10:2008
        *********************************************************************/
        NLPIR_API int NLPIR_AddUserWord(const char *sWord);

        """
        return self.get_func('NLPIR_AddUserWord', [c_char_p], c_int)(word)

    @NLPIRBase.byte_str_transform
    def clean_user_word(self) -> int:
        """
        /*********************************************************************
        *
        *  Func Name  : NLPIR_CleanUserWord
        *
        *  Description: Clean all temporary added user words
        *
        *  Parameters :
        *
        *  Returns    : 1,true ; 0,false
        *
        *  Author     :
        *  History    :
        *              1.create 2017/2/26
        *********************************************************************/
        NLPIR_API int NLPIR_CleanUserWord();

        """
        return self.get_func('NLPIR_CleanUserWord', None, c_int)()

    @NLPIRBase.byte_str_transform
    def save_the_usr_dic(self) -> int:
        """
        /*********************************************************************
        *
        *  Func Name  : Save
        *
        *  Description: Save dictionary to file
        *
        *  Parameters :
        *
        *  Returns    : 1,true; 2,false
        *
        *  Author     :
        *  History    :
        *              1.create 11:10:2008
        *********************************************************************/
        NLPIR_API int NLPIR_SaveTheUsrDic();

        """
        return self.get_func('NLPIR_SaveTheUsrDic', None, c_int)()

    @NLPIRBase.byte_str_transform
    def del_usr_word(self, word: str) -> int:
        """
        /*********************************************************************
        *
        *  Func Name  : NLPIR_DelUsrWord
        *
        *  Description: delete a word from the  user dictionary
        *
        *  Parameters : sWord:the word to be delete.
        *  Returns    : -1, the word not exist in the user dictionary; else, the handle of the word deleted
        *
        *  Author     :
        *  History    :
        *              1.create 11:10:2008
        *********************************************************************/
        NLPIR_API int NLPIR_DelUsrWord(const char *sWord);
        """
        return self.get_func('NLPIR_DelUsrWord', [c_char_p], c_int)(word)

    @NLPIRBase.byte_str_transform
    def get_uni_prob(self, word) -> float:
        """
        /*********************************************************************
        *
        *  Func Name  : NLPIR_GetUniProb
        *
        *  Description: Get Unigram Probability
        *
        *  Parameters : sWord: input word
        *  Returns    : The unitary probability of a  word.
        *  Author     : Kevin Zhang
        *  History    :
        *              1.create 2005-11-22
        *********************************************************************/
        NLPIR_API double NLPIR_GetUniProb(const char *sWord);

        """
        return self.get_func("NLPIR_GetUniProb", [c_char_p], c_double)(word)

    @NLPIRBase.byte_str_transform
    def is_word(self, word: str) -> int:
        """
        /*********************************************************************
        *
        *  Func Name  : NLPIR_IsWord
        *
        *  Description: Judge whether the word is included in the core dictionary
        *
        *  Parameters : sWord: input word
        *  Returns    :1: exists; 0: no exists
        *  Author     : Kevin Zhang
        *  History    :
        *              1.create 2005-11-22
        *********************************************************************/
        NLPIR_API int NLPIR_IsWord(const char *sWord);
        """
        return self.get_func("NLPIR_IsWord", [c_char_p], c_int)(word)

    @NLPIRBase.byte_str_transform
    def is_user_word(self, word: str) -> int:
        """
        /*********************************************************************
        *
        *  Func Name  : NLPIR_IsUserWord
        *
        *  Description: Judge whether the word is included in the user-defined dictionary
        *
        *  Parameters : sWord: input word
        *  Returns    :1: exists; 0: no exists
        *  Author     : Kevin Zhang
        *  History    :
        *              1.create 2016-12-31
        *********************************************************************/
        NLPIR_API int NLPIR_IsUserWord(const char *sWord, bool bAnsiCode=false);
        """
        return self.get_func("NLPIR_IsUserWord", [c_char_p], c_int)(word)

    @NLPIRBase.byte_str_transform
    def get_word_pos(self, word: str):
        """
        /*********************************************************************
        *
        *  Func Name  : NLPIR_GetWordPOS
        *
        *  Description: Get the word Part-Of-Speech　information
        *
        *  Parameters : sWord: input word
        *
        *  Returns    : success:
        *               fail:
        *  Author     : Kevin Zhang
        *  History    :
        *              1.create 2014-10-10
        *********************************************************************/
        NLPIR_API const char * NLPIR_GetWordPOS(const char *sWord);

        """
        return self.get_func("NLPIR_GetWordPOS", [c_char_p], c_char_p)(word)

    def set_pos_map(self, pos_map) -> int:
        """
        /*********************************************************************
        *
        *  Func Name  : NLPIR_SetPOSmap
        *
        *  Description: select which pos map will use
        *
        *  Parameters :nPOSmap, ICT_POS_MAP_FIRST  计算所一级标注集
                                ICT_POS_MAP_SECOND  计算所二级标注集
                                PKU_POS_MAP_SECOND   北大二级标注集
                                PKU_POS_MAP_FIRST       北大一级标注集
        *  Returns    : 0, failed; else, success
        *
        *  Author     :   
        *  History    : 
        *              1.create 11:10:2008
        *********************************************************************/
        NLPIR_API int NLPIR_SetPOSmap(int nPOSmap);
        """
        return self.get_func("NLPIR_SetPOSmap")(pos_map)

    @NLPIRBase.byte_str_transform
    def finer_segment(self, line: str) -> str:
        """
        /*********************************************************************
        *
        *  Func Name  : NLPIR_FinerSegment(const char *sLine)
        *
        *  Description: 当前的切分结果过大时，如“中华人民共和国”
        *                需要执行该函数，将切分结果细分为“中华 人民 共和国”
        *                细分粒度最大为三个汉字
        *  Parameters : sLine:输入的字符串
        *  Returns    : 返回的细分串，如果不能细分，则返回为空字符串""
        *
        *  Author     : Kevin Zhang
        *  History    : 
        *              1.create 2014/10/10
        *********************************************************************/
        NLPIR_API const char*  NLPIR_FinerSegment(const char *sLine);

        """
        return self.get_func("NLPIR_FinerSegment", [c_char_p], c_char_p)(line)

    @NLPIRBase.byte_str_transform
    def get_eng_word_origin(self, word: str) -> str:
        """
        /*********************************************************************
        *
        *  Func Name  : NLPIR_GetEngWordOrign(const char *sWord)
        *
        *  Description: 获取各类英文单词的原型，考虑了过去分词、单复数等情况
        *  Parameters : sWord:输入的单词
        *  Returns    : 返回的词原型形式
        *               driven->drive   drives->drive   drove-->drive
        *  Author     : Kevin Zhang
        *  History    : 
        *              1.create 2014/12/11
        *********************************************************************/
        NLPIR_API const char*  NLPIR_GetEngWordOrign(const char *sWord);
        """
        return self.get_func("NLPIR_GetEngWordOrign", [c_char_p], c_char_p)(word)

    @NLPIRBase.byte_str_transform
    def word_freq_stat(self, text: str) -> str:
        """
        /*********************************************************************
        *
        *  Func Name  : NLPIR_WordFreqStat(const char *sText)
        *
        *  Description: 获取输入文本的词，词性，频统计结果，按照词频大小排序
        *  Parameters : sText:输入的文本内容
        *                bStopRemove: true-去除停用词;false-不去除停用词
        *  Returns    : 返回的是词频统计结果形式如下：
        *                张华平/nr/10#博士/n/9#分词/n/8
        *  Author     : Kevin Zhang
        *  History    : 
        *              1.create 2014/12/11
        *********************************************************************/
        NLPIR_API const char*  NLPIR_WordFreqStat(const char *sText,bool bStopRemove=true);
        """
        return self.get_func("NLPIR_WordFreqStat", [c_char_p], c_char_p)(text)

    @NLPIRBase.byte_str_transform
    def file_word_freq_stat(self, filename: str) -> str:
        """
        /*********************************************************************
        *
        *  Func Name  : NLPIR_FileWordFreqStat(const char *sFilename)
        *
        *  Description: 获取输入文本的词，词性，频统计结果，按照词频大小排序
        *  Parameters : sFilename 文本文件的全路径
        *                bStopRemove: true-去除停用词;false-不去除停用词
        *  Returns    : 返回的是词频统计结果形式如下：
        *                张华平/nr/10#博士/n/9#分词/n/8
        *  Author     : Kevin Zhang
        *  History    : 
        *              1.create 2014/12/11
        *********************************************************************/
        NLPIR_API const char*  NLPIR_FileWordFreqStat(const char *sFilename,bool bStopRemove=true);
        """
        return self.get_func("NLPIR_FileWordFreqStat", [c_char_p], c_char_p)(filename)

    @NLPIRBase.byte_str_transform
    def get_last_error_msg(self) -> str:
        """
        /*********************************************************************
         *
         *  Func Name  : NLPIR_GetLastErrorMsg
         *
         *  Description: GetLastErrorMessage
         *    
         *  Parameters : void
         *  Returns    : the result buffer pointer
         *
         *  Author     : Kevin Zhang  
         *  History    : 
         *              1.create 2014-2-27
         *********************************************************************/
        NLPIR_API const char * NLPIR_GetLastErrorMsg();
        """
        return self.get_func("NLPIR_GetLastErrorMsg", None, c_char_p)()

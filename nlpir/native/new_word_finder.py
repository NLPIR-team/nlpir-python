# coding=utf-8
from nlpir.native.nlpir_base import NLPIRBase
from ctypes import c_bool, c_char_p, c_int, c_uint, c_ulong


class NewWordFinder(NLPIRBase):

    @property
    def dll_name(self) -> str:
        return "NewWordFinder"

    @NLPIRBase.byte_str_transform
    def init_lib(self, data_path: str, encode: int, license_code: str) -> int:
        """
            /*********************************************************************
             *
             *  Func Name  : NWF_Init
             *
             *  Description: Init NewWordFinder
             *               The function must be invoked before any operation listed as following
             *
             *  Parameters : const char * sInitDirPath=NULL
             *               sDataPath:  Path where Data directory stored.
             *               the default value is NULL, it indicates the initial directory
             *               is current working directory path
             *
             *  Returns    : success or fail
             *  Author     : Kevin Zhang
             *  History    :
             *              1.create 2013-2-6
             *********************************************************************/
            NEWWORDFINDER_API int NWF_Init(const char * sDataPath=0,int encode=GBK_CODE,const char*sLicenceCode=0);
        """
        return self.get_func("NWF_Init", [c_char_p, c_int, c_char_p], c_int)(data_path, encode, license_code)

    @NLPIRBase.byte_str_transform
    def exit_lib(self) -> bool:
        """
            /*********************************************************************
             *
             *  Func Name  : NWF_Exit
             *
             *  Description: Exist NewWordFinder and free related buffer
             *               Exit the program and free memory
             *               The function must be invoked while you needn't any lexical analysis
             *
             *  Parameters : None
             *
             *  Returns    : success or fail
             *  Author     : Kevin Zhang  
             *  History    : 
             *              1.create 2002-8-6
             *********************************************************************/
            NEWWORDFINDER_API bool NWF_Exit();
        """
        return self.get_func("NWF_Exit", [None], c_bool)()

    @NLPIRBase.byte_str_transform
    def get_new_words(self, line: str, max_key_limit: int = 50, format_json: bool = False) -> str:
        """
        /*********************************************************************
        *
        *  Func Name  : NWF_GetNewWords
        *
        *  Description: Extract New words from sLine
        *
        *  Parameters : sLine, the input paragraph;
        *               the input size cannot be very big(less than 60MB).
        *               Process large memory, recommend use NWF_NWI series functions
        *               bFormatJson: true:output is json format;otherwise xml format
        *               nMaxKeyLimit:maximum of key words, up to 50
        *  Returns    : new words list like:
        *              "科学发展观 23.80 屌丝 12.20" with weight
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
        *
        *  Author     :
        *  History    :
        *              1.create  2012/11/12
        *********************************************************************/
        NEWWORDFINDER_API const char * NWF_GetNewWords(const char *sLine,int nMaxKeyLimit=50, bool bFormatJson = false);
        """
        return self.get_func("NWF_GetNewWords", [c_char_p, c_int, c_bool], c_char_p)(line, max_key_limit, format_json)

    @NLPIRBase.byte_str_transform
    def get_file_new_words(self, file_name: str, max_key_limit: int = 50, format_json: bool = False) -> str:
        """
        /*********************************************************************
        *
        *  Func Name  : NWF_GetFileNewWords
        *
        *  Description: Extract new words from a text file
        *
        *  Parameters : sFilename, the input text file name
                        bFormatJson: true:output is json format;otherwise xml format
                        nMaxKeyLimit:maximum of key words, up to 50
        *  Returns    : keywords list like:
        *                 "科学发展观 23.80 宏观经济 12.20" with weight
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
        *
        *  Author     :
        *  History    :
        *              1.create 2012/11/12
        *********************************************************************/
        NEWWORDFINDER_API const char * NWF_GetFileNewWords(const char *sFilename,int nMaxKeyLimit=50,bool bFormatJson=false);
        """
        return self.get_func("NWF_GetFileNewWords", [c_char_p, c_int, c_bool], c_char_p)(
            file_name,
            max_key_limit,
            format_json
        )

    """
     /*********************************************************************
        *
        *  以下函数为2013版本专门针对新词发现的过程，一般建议脱机实现，不宜在线处理
        *  新词识别完成后，再自动导入到分词系统中，即可完成
        *  函数以NWF_NWI(New Word Identification)开头
        *********************************************************************/
    """

    @NLPIRBase.byte_str_transform
    def batch_start(self) -> bool:
        """
        /*********************************************************************
        *
        *  Func Name  : NWF_Batch_Start
        *
        *  Description: 启动新词识别
        *
        *  Parameters : None
        *  Returns    : bool, true:success, false:fail
        *
        *  Author     : Kevin Zhang
        *  History    :
        *              1.create 2013/11/23
        *********************************************************************/
        NEWWORDFINDER_API int NWF_Batch_Start();//New Word Indentification Start
        """
        return self.get_func("NWF_Batch_Start", [None], c_int)()

    @NLPIRBase.byte_str_transform
    def batch_addfile(self, filename: str) -> int:
        """
        /*********************************************************************
        *
        *  Func Name  : NWF_Batch_AddFile
        *
        *  Description: 往新词识别系统中添加待识别新词的文本文件
        *                需要在运行NWF_Batch_Start()之后，才有效
        *
        *  Parameters : const char *sFilename：文件名
        *  Returns    : bool, true:success, false:fail
        *
        *  Author     : Kevin Zhang
        *  History    : 
        *              1.create 20132/11/23
        *********************************************************************/
        NEWWORDFINDER_API unsigned long  NWF_Batch_AddFile(const char *sFilename);
        """
        return self.get_func("NWF_Batch_AddFile", [c_char_p], c_ulong)(filename)

    @NLPIRBase.byte_str_transform
    def batch_addmen(self, filename: str) -> int:
        """
        /*********************************************************************
        *
        *  Func Name  : NWF_Batch_AddMem
        *
        *  Description: 往新词识别系统中添加一段待识别新词的内存
        *                需要在运行NWF_Batch_Start()之后，才有效
        *
        *  Parameters : const char *sFilename：文件名
        *  Returns    : bool, true:success, false:fail
        *
        *  Author     : Kevin Zhang
        *  History    : 
        *              1.create 2013/11/23
        *********************************************************************/
        NEWWORDFINDER_API unsigned long NWF_Batch_AddMem(const char *sText);
        """
        return self.get_func("NWF_Batch_AddMem", [c_char_p], c_ulong)(filename)

    @NLPIRBase.byte_str_transform
    def batch_complete(self) -> int:
        """
        /*********************************************************************
        *
        *  Func Name  : NWF_Batch_Complete
        *
        *  Description: 新词识别添加内容结束
        *                需要在运行NWF_Batch_Start()之后，才有效
        *
        *  Parameters : None
        *  Returns    : bool, true:success, false:fail
        *
        *  Author     : Kevin Zhang
        *  History    : 
        *              1.create 2013/11/23
        *********************************************************************/
        NEWWORDFINDER_API int NWF_Batch_Complete();//文件或者内存导入结束
        """
        return self.get_func("NWF_Batch_Complete", None, c_int)()

    @NLPIRBase.byte_str_transform
    def batch_getresult(self, format_json: bool = False) -> c_char_p:
        """
        /*********************************************************************
        *
        *  Func Name  : NWF_Batch_GetResult
        *
        *  Description: 获取新词识别的结果
        *                需要在运行NWF_Batch_Complete()之后，才有效
        *
        *  Parameters :bFormatJson: true:output is json format;otherwise xml format
        *
        *  Returns    : 输出格式为
        *                【新词1】 【权重1】 【新词2】 【权重2】 ... 
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
        ]*
        *  Author     : Kevin Zhang
        *  History    : 
        *              1.create 2013/11/23
        *********************************************************************/
        NEWWORDFINDER_API const char * NWF_Batch_GetResult(bool bFormatJson=false);//输出新词识别结果
        """
        return self.get_func("NWF_Batch_GetResult", [c_bool], c_char_p)(format_json)

    @NLPIRBase.byte_str_transform
    def result2user_dict(self) -> int:
        """
        /*********************************************************************
        *
        *  Func Name  : NWF_Result2UserDict
        *
        *  Description: 将新词识别结果导入到用户词典中
        *                需要在运行NLPIR_NWI_Complete()之后，才有效
        *                如果需要将新词结果永久保存，建议在执行NLPIR_SaveTheUsrDic
        *  Parameters : None
        *  Returns    : bool, true:success, false:fail
        *
        *  Author     : Kevin Zhang
        *  History    : 
        *              1.create 2013/11/23
        *********************************************************************/
        NEWWORDFINDER_API unsigned int  NWF_Result2UserDict();//新词识别结果转为用户词典,返回新词结果数目
        """
        return self.get_func("NWF_Result2UserDict", None, c_uint)()

    @NLPIRBase.byte_str_transform
    def get_last_error_msg(self) -> str:
        """
        /*********************************************************************
         *
         *  Func Name  : KeyExtract_GetLastErrorMsg
         *
         *  Description: GetLastErrorMessage
         *    
         *
         *  Parameters : void
         *               
         *                  
         *  Returns    : the result buffer pointer 
         *
         *  Author     : Kevin Zhang  
         *  History    : 
         *              1.create 2014-2-27
         *********************************************************************/
        NEWWORDFINDER_API const char *  NWF_GetLastErrorMsg();
        
        """
        return self.get_func("NWF_GetLastErrorMsg", None, c_char_p)()

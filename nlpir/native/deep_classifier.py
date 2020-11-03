# coding=utf-8
from nlpir.native.nlpir_base import NLPIRBase
from ctypes import c_bool, c_char, c_char_p, c_double, c_int, c_uint, POINTER, Structure, byref
import typing


class DeepClassifier(NLPIRBase):
    """
    A dynamic link library native class for Classify using deep learning
    """
    FEATURE_COUNT = 1000

    @property
    def dll_name(self):
        return "DeepClassifier"

    @NLPIRBase.byte_str_transform
    def init_lib(self, data_path: str, encode: int, license_code: str) -> int:
        """
            *
            *  Func Name  : DC_Init
            *
            *  Description: Init DeepClassifier
            *               The function must be invoked before any operation listed as following
            *
            *  Parameters : const char * sInitDirPath=NULL
            *				 sDataPath:  Path where Data directory stored.
            *				 the default value is NULL, it indicates the initial directory is current working directory path
            *				 encode: encoding code;
            *				 nFeathureCount: feature count
            *				 sLicenseCode: license code for unlimited usage. common user ignore it
            *
            *  Returns    : success or fail
            *  Author     : Kevin Zhang
            *  History    :
            *              1.create 2013-6-8
            :param data_path:
            :param encode:
            :param license_code:
            :return:
        """
        return self.get_func("DC_Init", [c_char_p, c_int, c_int, c_int, c_char_p], c_int)(
            data_path,
            encode,
            self.FEATURE_COUNT,
            license_code
        )

    @NLPIRBase.byte_str_transform
    def exit_lib(self) -> bool:
        """
            *  Func Name  : DC_Init
            *
            *  Description: Init DeepClassifier
            *               The function must be invoked before any operation listed as following
            *
            *  Parameters : const char * sInitDirPath=NULL
            *				 sDataPath:  Path where Data directory stored.
            *				 the default value is NULL, it indicates the initial directory is current working directory path
            *				 encode: encoding code;
            *				 nFeathureCount: feature count
            *				 sLicenseCode: license code for unlimited usage. common user ignore it
            *
            *  Returns    : success or fail
            *  Author     : Kevin Zhang
            *  History    :
            *              1.create 2013-6-8
            :return:
        """
        return self.get_func("DC_Exit", None, c_int)()

    @NLPIRBase.byte_str_transform
    def get_last_error_msg(self) -> str:
        """
            *
            *  Func Name  : DC_GetLastErrorMsg
            *
            *  Description: GetLastErrorMessage
            *
            *
            *  Parameters : none
            *
            *
            *  Returns    : the result buffer pointer
            *
            *  Author     : Kevin Zhang
            *  History    :
            *              1.create 2014-2-27
        :return:
        """
        return self.get_func("DC_GetLastErrorMsg", None, c_char_p)()

    @NLPIRBase.byte_str_transform
    def new_instance(self, feature_count: int):
        """
            *  Func Name  : DC_NewInstance
            *
            *  Description: New a  DeepClassifier Instance
            *               The function must be invoked before mulitiple classifiers
            *
            *  Parameters : int nFeatureCount: Feature count
            *  Returns    : DC_HANDLE , DeepClassifier Handle if success; otherwise return -1;
            *  Author     : Kevin Zhang
            *  History    :
            *              1.create 2015-9-22
        :param feature_count:
        :return:
        """
        return self.get_func("DC_NewInstance", [c_int], POINTER)(feature_count)

    def delete_instance(self, instance: POINTER):
        """
        Func Name  : DC_DeleteInstance

        Description: Delete a  DeepClassifier Instance with handle
                   The function must be invoked before release a specific classifier

        Parameters : None
        Returns    : DC_HANDLE , DeepClassifier Handle
        Author     : Kevin Zhang
        History    :
                  1.create 2015-9-22
        :param instance:
        :return:
        """
        return self.get_func("DC_DeleteInstance", [POINTER], c_int)(instance)

    def add_train(self, classname: str, text: str, handler: POINTER = 0):
        """
        Func Name  : DC_AddTrain

        Description: DeepClassifier Training on given text in Memory

        Parameter:   const char * sClassName: class name
                     sText: text content
                   handle: classifier handle
        Returns    : success or fail
        Author     : Kevin Zhang
        History    :
                  1.create 2013-6-8
        :param classname:
        :param text:
        :param handler:
        :return:
        """
        return self.get_func("DC_AddTrain", [c_char_p, c_char_p, POINTER], c_bool)(classname, text, handler)

    def add_train_file(self, classname: str, filename: str, handler: POINTER = 0):
        """
        Func Name  : DC_AddTrainFile

        Description: DeepClassifier Training on given text in file

        Parameter:   const char * sClassName: class name
                     sFilename: text file name

        Returns    : success or fail
        Author     : Kevin Zhang
        History    :
                  1.create 2013-6-8
        :param classname:
        :param filename:
        :param handler:
        :return:
        """
        return self.get_func("DC_AddTrainFile", [c_char_p, c_char_p, POINTER], c_int)(classname, filename, handler)

    def train(self, handler: POINTER = 0):
        """
        Func Name  : DC_Train

        Description: DeepClassifier Training on given text in Memory
                     After training, the training result will stored.
                    Then the classifier can load it with DC_LoadTrainResult at any time(offline or online).
        Parameter:   const char * sClassName: class name
                     sFilename: text file name

        Returns    : success or fail
        Author     : Kevin Zhang
        History    :
                  1.create 2013-6-8
        :param handler:
        :return:
        """
        return self.get_func("DC_Train", [POINTER], c_int)(handler)

    def load_train_result(self, handler: POINTER = 0):
        """
        Func Name  : DC_LoadTrainResult

        Description: DeepClassifier Load already training data

        Parameter:   None

        Returns    : success or fail
        Author     : Kevin Zhang
        History    :
                  1.create 2013-6-8
        :param handler:
        :return:
        """
        return self.get_func("DC_LoadTrainResult", None, c_int)(handler)

    def export_features(self, filename: str, handler: POINTER = 0):
        """
        Func Name  : DC_ExportFeatures

        Description: DeepClassifier Exports Features after training

        Parameter:   None

        Returns    : success or fail
        Author     : Kevin Zhang
        History    :
                  1.create 2013-6-8
        :param filename:
        :param handler:
        :return:
        """
        return self.get_func("DC_ExportFeatures", None, c_int)(filename, handler)

    def classify(self, text: str, handler: POINTER = 0):
        """
        Func Name  : DC_Classify

        Description: DeepClassifier Classify on given text in Memory

        Parameter:   const char * sClassName: class name
                     sFilename: text file name

        Returns    : the best class name
        Author     : Kevin Zhang
        History    :
                  1.create 2013-6-8
        :param text:
        :param handler:
        :return:
        """
        return self.get_func("DC_Classify", [c_char_p, POINTER], c_char_p)(text, handler)

    def classify_ex(self, text: str, handler: POINTER = 0):
        """
        Func Name  : DC_ClassifyEx

        Description: DeepClassifier Classify on given text in Memory
                    return multiple class with weights, sorted by weights
        Parameter:   const char * sClassName: class name
                     sFilename: text file name

        Returns    : multiple class name with weights, sorted by weights
                   For instance: 政治/1.20##经济/1.10
                bookyzjs/7.00##bookxkfl/6.00##booktslx/5.00##bookny-xyfl/4.00##booksy/3.00##bookdwpz/2.00##booknyjj/1.00##
        Author     : Kevin Zhang
        History    :
                  1.create 2013-6-8

        DEEP_CLASSIFIER_API const char * DC_ClassifyEx(const char *sText, DC_HANDLE handle = 0);
        :param text:
        :param handler:
        :return:
        """
        return self.get_func("DC_ClassifyEx", [c_char_p, POINTER], c_char_p)(text, handler)

    def classify_file(self, filename: str, handler: POINTER = 0):
        """
        Func Name  : DC_ClassifyFile

        Description: DeepClassifier Classify on given text in file

        Parameter:   const char * sClassName: class name
                     sFilename: text file name

        Returns    : success or fail
        Author     : Kevin Zhang
        History    :
                  1.create 2013-6-8

        DEEP_CLASSIFIER_API const char * DC_ClassifyFile(const char *sFilename,DC_HANDLE handle=0);
        :param filename:
        :param handler:
        :return:
        """
        return self.get_func("DC_ClassifyFile", [c_char_p, POINTER], c_char_p)(filename, handler)

    def classify_file_ex(self, filename: str, handler: POINTER = 0):
        """
        Func Name  : DC_ClassifyExFile

        Description: DeepClassifier Classify on given text in file

        Parameter:   const char * sClassName: class name
                     sFilename: text file name

        Returns    : success or fail
        Author     : Kevin Zhang
        History    :
                  1.create 2013-6-8

        DEEP_CLASSIFIER_API const char * DC_ClassifyExFile(const char *sFilename, DC_HANDLE handle = 0);
        :param filename:
        :param handler:
        :return:
        """
        return self.get_func("DC_ClassifyExFile", [filename, handler], c_char_p)(filename, handler)

# coding=utf-8
from nlpir.native.nlpir_base import NLPIRBase
from ctypes import c_bool, c_char_p, c_int, POINTER


class DeepClassifier(NLPIRBase):
    """
    A dynamic link library native class for Classify using deep learning
    """
    FEATURE_COUNT = 800

    @property
    def dll_name(self):
        return "DeepClassifier"

    @NLPIRBase.byte_str_transform
    def init_lib(self, data_path: str, encode: int, license_code: str) -> int:
        """
        Call **DC_Init**

        Init DeepClassifier

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
        Call **DC_Init**

        :return:
        """
        return self.get_func("DC_Exit", None, c_int)()

    @NLPIRBase.byte_str_transform
    def get_last_error_msg(self) -> str:
        """
        Call **DC_GetLastErrorMsg**

        :return:
        """
        return self.get_func("DC_GetLastErrorMsg", None, c_char_p)()

    @NLPIRBase.byte_str_transform
    def new_instance(self, feature_count: int) -> int:
        """
        Call **DC_NewInstance**

        New a DeepClassifier Instance. This function must be invoked before classify,
        and need be deleted when exit the process. Delete instance can use the function
        :func:`delete_instance`

        :param feature_count: Feature count
        :return: DeepClassifier Handle if success; otherwise return -1;
        """
        return self.get_func("DC_NewInstance", [c_int], POINTER(c_int))(feature_count)

    @NLPIRBase.byte_str_transform
    def delete_instance(self, instance: int) -> int:
        """
        Call **DC_DeleteInstance**

        Delete a DeepClassifier Instance with handle. The function must be invoked before
        release a specific classifier. The instance can be retrieve by :func:`new_instance`

        :param instance: DeepClassifier Handle
        :return:
        """
        return self.get_func("DC_DeleteInstance", [POINTER(c_int)], c_int)(instance)

    @NLPIRBase.byte_str_transform
    def add_train(self, classname: str, text: str, handler: int = 0) -> bool:
        """
        Call **DC_AddTrain**

        DeepClassifier add train dataset on given text in Memory

        :param classname: class name
        :param text: text content
        :param handler: classifier handler
        :return: add success or not
        """
        return self.get_func("DC_AddTrain", [c_char_p, c_char_p, POINTER(c_int)], c_bool)(classname, text, handler)

    @NLPIRBase.byte_str_transform
    def add_train_file(self, classname: str, filename: str, handler: int = 0) -> int:
        """
        Call **DC_AddTrainFile**

        DeepClassifier add train dataset on given text in file

        :param classname: class name
        :param filename: text file name
        :param handler: classifier handler
        :return: success or fail
        """
        return self.get_func("DC_AddTrainFile", [c_char_p, c_char_p, POINTER(c_int)], c_int)(
            classname, filename, handler)

    @NLPIRBase.byte_str_transform
    def train(self, handler: int = 0) -> int:
        """
        Call **DC_Train**

        DeepClassifier Training on given text in Memory.
        After training, the training result will stored.
        Then the classifier can load it with :func:`load_train_result` (offline or online).

        :param handler: classifier handler
        :return: success or not
        """
        return self.get_func("DC_Train", [POINTER(c_int)], c_int)(handler)

    @NLPIRBase.byte_str_transform
    def load_train_result(self, handler: int = 0) -> int:
        """
        Call **DC_LoadTrainResult**

        DeepClassifier Load already training data

        :param handler: classifier handler
        :return: success or not
        """
        return self.get_func("DC_LoadTrainResult", None, c_int)(handler)

    @NLPIRBase.byte_str_transform
    def export_features(self, filename: str, handler: int = 0) -> int:
        """
        Call **DC_ExportFeatures**

        DeepClassifier Exports Features after training

        :param filename: save path
        :param handler: classifier handler
        :return: success or not
        """
        return self.get_func("DC_ExportFeatures", None, c_int)(filename, handler)

    @NLPIRBase.byte_str_transform
    def classify(self, text: str, handler: int = 0) -> str:
        """
        Call **DC_Classify**

        DeepClassifier Classify on given text in Memory

        :param text: text
        :param handler: classifier handler
        :return: classify result , a class name
        """
        return self.get_func("DC_Classify", [c_char_p, POINTER(c_int)], c_char_p)(text, handler)

    @NLPIRBase.byte_str_transform
    def classify_ex(self, text: str, handler: POINTER(c_int) = 0):
        """
        Call **DC_ClassifyEx**

        DeepClassifier Classify on given text in Memory,
        return multiple class with weights, sorted by weights

        :param text: text
        :param handler: classifier handler
        :return: result with weight, For instance: ``政治/1.20##经济/1.10,``
            ``bookyzjs/7.00##bookxkfl/6.00##booktslx/5.00##bookny-xyfl/4.00##``
        """
        return self.get_func("DC_ClassifyEx", [c_char_p, POINTER(c_int)], c_char_p)(text, handler)

    @NLPIRBase.byte_str_transform
    def classify_file(self, filename: str, handler: int = 0):
        """
        Call **DC_ClassifyFile**

        DeepClassifier Classify on given text in file

        :param filename: file name of text
        :param handler: classifier handler
        :return: result same as :func:`classify`
        """
        return self.get_func("DC_ClassifyFile", [c_char_p, POINTER(c_int)], c_char_p)(filename, handler)

    @NLPIRBase.byte_str_transform
    def classify_file_ex(self, filename: str, handler: int = 0):
        """
        Call **DC_ClassifyExFile**

        DeepClassifier Classify on given text in file

        :param filename: file name of text
        :param handler: classifier handler
        :return: result same as :func:`classify_ex`
        """
        return self.get_func("DC_ClassifyExFile", [filename, handler], c_char_p)(filename, handler)

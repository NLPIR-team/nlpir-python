# coding=utf-8
from nlpir.native.nlpir_base import NLPIRBase
from ctypes import c_bool, c_char_p, c_int, POINTER, Structure, c_float


class StDoc(Structure):
    __fields__ = [
        ("sTitle", c_char_p),
        ("sContent", c_char_p),
        ("sAuthor", c_char_p),
        ("sBoard", c_char_p),
        ("sDatatype", c_char_p)
    ]


class Classifier(NLPIRBase):
    @property
    def dll_name(self):
        return "LJClassifier"

    @NLPIRBase.byte_str_transform
    def init_lib(self, data_path: str, encode: int, license_code: str) -> int:
        """
        Call **classifier_init**

        :param data_path:
        :param encode:
        :param license_code:
        :return: 1 success 0 fail
        """
        return self.get_func("classifier_init", [c_char_p, c_char_p, c_char_p], c_bool)("rulelist.xml", data_path,
                                                                                        license_code)

    @NLPIRBase.byte_str_transform
    def exit_lib(self) -> bool:
        """
        Call **classifier_exit**

        :return: exit success or not
        """
        return self.get_func("classifier_exit", None, None)()

    @NLPIRBase.byte_str_transform
    def get_last_error_msg(self) -> str:
        return self.get_func("classifier_GetLastErrorMsg", None, c_char_p)()

    @NLPIRBase.byte_str_transform
    def exec_1(self, data: StDoc, out_type: int = 0):
        """
        Call **classifier_exec1**

        对输入的文章结构进行分类

        :param data: 文章结构
        :param out_type: 输出是否包括置信度, 0 没有置信度 1 有置信度
        :return:  主题类别串  各类之间用\t隔开，类名按照置信度从高到低排序
            举例：“要闻	敏感	诉讼”, “要闻 1.00	敏感 0.95	诉讼 0.82”
        """
        return self.get_func("classifier_exec1", [POINTER(StDoc), c_int], c_char_p)(data, out_type)

    @NLPIRBase.byte_str_transform
    def exec(self, title: str, content: str, out_type: int):
        """
        Call **classifier_exec**

        对输入的文章进行分类

        :param title: 文章标题
        :param content: 文章内容
        :param out_type: 输出知否包括置信度,同 :func:`exec_1`
        :return: 同 :func:`exec_1`
        """
        return self.get_func("classifier_exec")([c_char_p, c_char_p, c_int], c_char_p)(title, content, out_type)

    @NLPIRBase.byte_str_transform
    def detail(self, classname: str):
        """
        Call **classifier_detail**

        对于当前文档，输入类名，取得结果明细

        :param classname: 结果类名
        :return: 结果明细 例如:

        ::

            RULE3:
            SUBRULE1: 内幕 1
            SUBRULE2: 股市 1	基金 3	股票 8
            SUBRULE3: 书摘 2
        """
        return self.get_func("classifier_detail", [c_char_p], c_char_p)(classname)

    @NLPIRBase.byte_str_transform
    def set_sim_thresh(self, sim: float):
        """
        Call **classifier_setsimthresh**

        设置阈值

        :param sim: 阈值
        :return:
        """
        return self.get_func("classifier_setsimthresh", [c_float])(sim)

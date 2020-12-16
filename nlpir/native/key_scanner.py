# coding=utf-8
from nlpir.native.nlpir_base import NLPIRBase
from ctypes import c_bool, c_char_p, c_int, c_float

#: UTF8编码转换过程中自动繁简转换处理，扫描过滤功能建议使用
ENCODING_UTF8_FJ = 5
#: 正常扫描模式
SCAN_MODE_NORMAL = 0
#: 形变扫描模式
SCAN_MODE_SHAPE = 1
#: 拼音扫描模式
SCAN_MODE_PINYIN = 2
#: 校对扫描模式
SCAN_MODE_CHECK = 3


class KeyScanner(NLPIRBase):
    """
    A dynamic link library native class for Keyword Scan
    """

    @property
    def dll_name(self) -> str:
        return "KeyScanAPI"

    @NLPIRBase.byte_str_transform
    def init_lib(self, data_path: str, encode: int, license_code: str) -> int:
        """
        Call **KS_Init**

        :param str data_path:
        :param int encode:
        :param str license_code:
        :return: 1 success 0 fail
        """
        return self.get_func('KS_Init', [c_char_p, c_int, c_char_p], c_int)(
            data_path, encode, license_code)

    def exit_lib(self) -> bool:
        """
        Call **KS_Exit**

        :return: exit success or not
        """
        return self.get_func('KS_Exit', restype=c_bool)()

    @NLPIRBase.byte_str_transform
    def get_last_error_msg(self) -> str:
        """
        Call **KS_GetLastErrorMsg**

        :return: error message
        """
        return self.get_func("KS_GetLastErrorMsg", None, c_char_p)()

    @NLPIRBase.byte_str_transform
    def new_instance(self, filter_type_index: int = 0) -> int:
        """
        Call **KS_NewInstance**

        Get a instance from system for executing other functions.
        The function must be invoked before multiple keyword scan filter.
        This function will alloc memory , it need to be free memory by
        using :func:`delete_instance` after finish all executions from
        this handle.

        :param filter_type_index: which No of filter want to be used in this instance.
            The filter file will save into `Data/KeyScanner/filter{no}*`
        :return: a handle from system if success; otherwise return -1;
        """
        return self.get_func("KS_NewInstance", [c_int], c_int)(filter_type_index)

    @NLPIRBase.byte_str_transform
    def delete_instance(self, handle: int) -> int:
        """
        Call **KS_DeleteInstance**

        Delete handle created by :func`new_instance`. Once delete handle
        from system, this handle cannot be used in any situation or will
        invoke critical errors.

        :param handle: the handle want to be deleted
        :return: success or not
        """
        return self.get_func("KS_DeleteInstance", [c_int], c_int)(handle)

    @NLPIRBase.byte_str_transform
    def import_user_dict(
            self,
            filename: str,
            over_write: bool = False,
            pinyin_abbrev_needed: bool = False,
            handle=0
    ) -> int:
        """
        Call **ImportUserDict**

        Import User-defined dictionary 导入用户词典, 此操作为全局操作会影响其他 instance 的过滤

        文本文件每行的格式为: ``词条 词类 权重`` (注意，最多定义255个类别), 例::

            AV电影 色情 2
            六合彩 涉赌 8 1

        复杂过滤条件: 支持与或非处理 ;表示或关系，+表示与关系，-表示否
        格式如下::

            {key11;key12;key13;...;key1N}+{key21;key22;key23;...;key2N}+...+{keyM1;keyM2;keyM3;...;keyMN}-{keyN}

        示例::

            {中国;中华;中华人民共和国;中国共产党;中共}+{伟大;光荣;正确}-{中华民国;国民党}  政治类 5

        表示的是文本内容中包含 ``中国;中华;中华人民共和国;中国共产党;中共`` 中的一种，
        同时出现 ``伟大;光荣;正确`` 中的一个，但不能出现 ``中华民国;国民党`` 的任何一个

        :param filename: path of user dictionary
        :param pinyin_abbrev_needed:
        :param over_write: true将覆盖系统已经有的词表；否则将采用追加的方式追加不良词表
        :param handle: handle of KeyScanner
        :return: success or not
        """
        return self.get_func("KS_ImportUserDict", [c_char_p, c_bool, c_bool, c_int], c_int)(
            filename, over_write, pinyin_abbrev_needed, handle)

    @NLPIRBase.byte_str_transform
    def delete_user_dic(self, text: str, handle: int) -> int:
        """
        Call **DeleteUserDict**

        Delete User-defined dictionary 删除用户词典, 此操作为全局操作, 会删除词典文件并影响所有 instance

        文本文件每行的格式为: ``词条`` , 例如::

            AV电影
            习近平

        :param text: Text of user dictionary
        :param handle: handle of KeyScanner
        :return: The number of lexical entry deleted successfully 成功删除的词典条数
        """
        return self.get_func("KS_DeleteUserDict", [c_char_p, c_int], c_int)(text, handle)

    @NLPIRBase.byte_str_transform
    def delete_user_dic_from_file(self, filename: str, handle: int) -> int:
        """
        Call **DeleteUserDict**

        Delete User-defined dictionary 删除用户词典, 此操作为全局操作, 会删除词典文件并影响所有 instance

        文本文件每行的格式为: ``词条`` , 例如::

            AV电影
            习近平

        :param filename: Text filename for user dictionary
        :param handle: handle of KeyScanner
        :return: The number of lexical entry deleted successfully 成功删除的词典条数
        """
        return self.get_func("KS_DeleteUserDict", [c_char_p, c_int], c_int)(filename, handle)

    @NLPIRBase.byte_str_transform
    def scan(self, content: str, handle: int = 0) -> str:
        """
        Call **KS_Scan**

        扫描输入的文本内容

        :param content: 文本内容
        :param handle: handle of KeyScanner
        :return: 涉及不良的所有类别与权重，按照权重排序。如: ``色情/10#暴力/1#`` , ``政治反动/2#FLG/1#涉领导人/1#`` ,
            ``""`` : 表示无扫描命中结果
        """
        return self.get_func("KS_Scan", [c_char_p, c_int], c_char_p)(content, handle)

    @NLPIRBase.byte_str_transform
    def scan_detail(self, content: str, scan_mode: int = SCAN_MODE_NORMAL, handle: int = 0) -> str:
        """
        Call **KS_ScanDetail**

        扫描输入的文本内容,获得详细结果

        :param scan_mode: 扫描模式
        :param content: 文本内容
        :param handle: handle of KeyScanner
        :return: 返回包含了扫描结果的内容，扫描结果明细:

        ::

            {
                "Details": ["chou傻逼xi禁评"],
                "Rules": ["傻逼","xi禁评"],
                "filename": "",
                "illegal" :{
                    "classes":[
                        {
                            "freq":1,
                            "word":"粗言秽语"
                        },{
                            "freq":1,
                            "word":"污言秽语"
                        },{
                            "freq":1,
                            "word":"新华社禁用"
                        },{
                            "freq":1,"word":"一号首长"
                        }
                    ],
                    "hit_count":4,
                    "keys":["傻逼","xi禁评"],
                    "scan_val":13.333333333333332
                },
                "legal": {
                    "hit_count":0,
                    "scan_val":0.0
                },
                "line_id":0,
                "org_file":"",
                "score":13.333333333333332
            }
        """
        return self.get_func("KS_ScanDetail", [c_char_p, c_int, c_int], c_char_p)(content, scan_mode, handle)

    @NLPIRBase.byte_str_transform
    def scan_file(self, filename: str, handle: int = 0) -> str:
        """
        Call **KS_ScanFile**

        扫描输入的文本文件内容

        :param filename: 文本文件名
        :param handle: handle of KeyScanner
        :return: same as :func:`scan`
        """
        return self.get_func("KS_ScanFile", [c_char_p, c_int], c_char_p)(filename, handle)

    @NLPIRBase.byte_str_transform
    def scan_file_detail(self, filename: str, handle: int = 0) -> str:
        """
        Call **KS_ScanFileDetail**

        扫描输入的文本文件内容

        :param filename: 文本文件名
        :param handle: handle of KeyScanner
        :return: same as :func:`scan_detail`
        """
        return self.get_func("KS_ScanFileDetail", [c_char_p, c_int], c_char_p)(filename, handle)

    @NLPIRBase.byte_str_transform
    def scan_line(
            self,
            filename: str,
            result_filename: str,
            handle: int = 0,
            encrypt: int = 0,
            scan_mode: int = SCAN_MODE_NORMAL
    ) -> int:
        """
        Call **KS_ScanLine**

        按行扫描输入的文本文件内容

        :param filename: 输入的文本文件名
        :param result_filename: 输出的结果文件名
        :param handle: handle of KeyScanner
        :param encrypt: 0 不加密；1，加密
        :param scan_mode:
        :return: same as :func:`scan_detail`
        """
        return self.get_func("KS_ScanLine", [c_char_p, c_char_p, c_int, c_int, c_int], c_int)(
            filename, result_filename, handle, encrypt, scan_mode
        )

    @NLPIRBase.byte_str_transform
    def scan_stat(self, result_file, handle: int = 0) -> int:
        """
        Call **KS_ScanStat**

        输出扫描结果的命中统计报告，利于进一步的分析核查

        :param result_file: 输出结果的文件文件
        :param handle: handle of KeyScanner
        :return: 成功扫描到问题的文件数
        """
        return self.get_func("KS_ScanStat", [c_char_p, c_int], c_int)(result_file, handle)

    @NLPIRBase.byte_str_transform
    def scan_dir(
            self,
            input_dir_path: str,
            result_path: str,
            filter: str,
            thread_count: int = 10,
            encrypt: bool = False,
            scan_mode: int = SCAN_MODE_NORMAL
    ) -> int:
        """
        Call **KS_ScanDir**

        多线程扫描按行扫描输入的文本夹文件内容

        :param input_dir_path: 输入的文件夹路径
        :param result_path: 输出结果的文件夹路径
        :param filter: 输入的文件后缀名
        :param thread_count: 线程数，默认10个
        :param encrypt: 0 不加密；1，加密
        :param scan_mode:
        :return: 成功扫描到问题的文件数
        """
        return self.get_func("KS_ScanDir", [c_char_p, c_char_p, c_char_p, c_int, c_int, c_int], c_int)(
            input_dir_path, result_path, filter, thread_count, encrypt, scan_mode
        )

    @NLPIRBase.byte_str_transform
    def merge_result(self, path: str) -> None:
        """
        Merge多线程的扫描结果

        :param path:
        :return:
        """
        return self.get_func("KS_MergeResult", [c_char_p], None)(path)

    @NLPIRBase.byte_str_transform
    def scan_add_stat(self, result_file: str, handle: int) -> int:
        """
        将handle线程扫描结果归并到0线程

        :param result_file:
        :param handle:
        :return:
        """
        return self.get_func("KS_ScanAddStat", [c_char_p, c_int], c_int)(result_file, handle)

    @NLPIRBase.byte_str_transform
    def stat_result_filter(self, input_filename: str, result_filename: str, threshold: float = 5.0) -> int:
        """
        Call **KS_StatResultFilter**

        对扫描的统计结果进行过滤分析

        :param input_filename: 输入的结果文件名
        :param result_filename: 输出结果的文件名
        :param threshold: 不良得分的阈值
        :return: 成功扫描到问题的文件数
        """
        return self.get_func("KS_StatResultFilter", [c_char_p, c_char_p, c_float], c_int)(
            input_filename, result_filename, c_float(threshold))

    @NLPIRBase.byte_str_transform
    def scan_result_filter(self, input_filename: str, result_filename: str, threshold: float = 9.0) -> int:
        """
        Call **KS_ScanResultFilter**

        对扫描的详细结果文件进行过滤分析

        :param input_filename: 输入的结果文件名
        :param result_filename: 输出结果的文件名
        :param threshold: 不良得分的阈值
        :return: 成功扫描到问题的文件数
        """
        return self.get_func("KS_ScanResultFilter", [c_char_p, c_char_p, c_float], c_int)(
            input_filename, result_filename, c_float(threshold))

    @NLPIRBase.byte_str_transform
    def decrypt(self, input_dir_path: str, result_path: str) -> int:
        """
        Call **KS_Decrypt**

        多线程转换扫描结果

        :param input_dir_path: 输入的文件夹路径
        :param result_path: 输出结果的文件夹路径
        :return:
        """
        return self.get_func("KS_Decrypt", [c_char_p, c_char_p], c_int)(input_dir_path, result_path)

    @NLPIRBase.byte_str_transform
    def export_dict(self, filename: str, handle: int = 0) -> int:
        """
        Call **KS_ExportDict**

        ExportDict dictionary 导出已经定义的不良词词典, 为保护知识产权，该功能仅局限于管理员内部调度使用

        文本文件的格式为: ``词条 词类 权重`` (注意，最多定义255个类别)
        例如::

            AV电影 色情 2
            六合彩 涉赌 8 1

        :param filename: Text filename for user dictionary
        :param handle: handle of KeyScanner
        :return: The number of lexical entry imported successfully  成功导入的词典条数
        """
        return self.get_func("KS_ExportDict", [c_char_p, c_int], c_int)(filename, handle)

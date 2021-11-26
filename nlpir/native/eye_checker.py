# coding=utf-8
import os
import typing
from ctypes import c_bool, c_char_p, c_int, c_size_t

from nlpir.native import nlpir_base
from nlpir.native.nlpir_base import NLPIRBase, UTF8_CODE, PACKAGE_DIR

RPT_UNSPECIFIC = 0  # No Specific type
RPT_JIAYOUZHAN = 1  # 加油站报告
RPT_ANPING = 2  # 安评报告
RPT_CONTRACT = 3  # 合同
RPT_LEGAL = 4  # 法律法规
RPT_OFFICIAL_DOC = 5  # 公文
RPT_PAPER = 6  # 学术论文
RPT_DISSERTATION = 7  # 毕业论文
RPT_ARGUMENT = 8  # 标准参数
RPT_IPO = 9  # IPO金融上市文档
RPT_INSURANCE = 10  # 保险文档

RESULT_TYPE_CHECK = 0  # 获取核查结果内容
RESULT_TYPE_KG = 1  # 获取知识图谱内容
RESULT_TYPE_CONTENT = 2  # 获取目录内容
RESULT_TYPE_TEXT = 3  # 获取正文内容
RESULT_TYPE_FIGURE = 4  # 获取图片内容
RESULT_TYPE_TABLE = 5  # 获取图片内容
RESULT_TYPE_SINGLE_KEY = 6  # 获取单个知识
RESULT_TYPE_TUPLE = 7  # 获取元组
RESULT_TYPE_ENTITY = 8  # 获取命名实体


class EyeChecker(nlpir_base.NLPIRBase):
    """
    TODO report_type or doc_type

    A dynamic link library native class for 09 Eys Checker
    """

    DOC_EXTRACT_DELIMITER = "#"  #: 分隔符
    DOC_EXTRACT_TYPE_MAX_LENGTH = 600  # 最大长度
    load_mode = nlpir_base.NLPIRBase.RTLD_LAZY

    def __init__(
            self,
            encode: int = UTF8_CODE,
            lib_path: typing.Optional[int] = None,
            data_path: typing.Optional[str] = None,
            license_code: str = ''
    ):
        kgb_path = os.path.join(PACKAGE_DIR, "Data/KGB")
        data_path = kgb_path if data_path is None else data_path
        super().__init__(encode, lib_path, data_path, license_code)

    @property
    def dll_name(self) -> str:
        return "EyeCheckerAPI"

    @nlpir_base.NLPIRBase.byte_str_transform
    def init_lib(self, data_path: str, encode: int, license_code: str) -> int:
        """
        Call **NERICS_Init**

        :param str data_path:
        :param int encode:
        :param str license_code:
        :return: 1 success 0 fail
        """
        return self.get_func('NERICS_Init', [c_char_p, c_char_p], c_int)(data_path, license_code)

    def exit_lib(self) -> bool:
        """
        Call **NERICS_Exit**

        :return: exit success or not
        """
        return self.get_func('NERICS_Exit', restype=c_bool)()

    @nlpir_base.NLPIRBase.byte_str_transform
    def get_last_error_msg(self) -> str:
        """
        Call **DE_GetLastErrorMsg**

        :return: error message
        """
        return self.get_func("NERICS_GetLastErrorMsg", None, c_char_p)()

    @nlpir_base.NLPIRBase.byte_str_transform
    def import_field_dict(self, field_dict_file: str, pinyin_abbrev_needed: bool = False,
                          overwrite: bool = True) -> int:
        """
        Import field dictionary

        :param field_dict_file:
        :param pinyin_abbrev_needed:
        :param overwrite:
        :return:
        """
        return self.get_func("NERICS_ImportFieldDict", [c_char_p, c_bool, c_bool], c_int)(
            field_dict_file, pinyin_abbrev_needed, overwrite
        )

    @nlpir_base.NLPIRBase.byte_str_transform
    def new_instance(self) -> int:
        """
       Description: New a  NERICS Instance
               The function must be invoked before mulitiple keyword scan filter

      Parameters :
      Returns    : NERICS_HANDLE: KeyScan Handle if success; otherwise return -1;
      Author     : Kevin Zhang
      History    :
              1.create 2016-11-15
        :return:
        """
        return self.get_func("NERICS_NewInstance", [], c_int)()

    @nlpir_base.NLPIRBase.byte_str_transform
    def delete_instance(self, handle: int) -> int:
        """

        :param handle:
        :return:
        """
        return self.get_func("NERICS_DeleteInstance", [c_int], c_int)(handle)

    @nlpir_base.NLPIRBase.byte_str_transform
    def import_doc(self, report_file: str, url_prefix: str = "", handle: int = 0) -> str:
        """
          Func Name  : NERICS_ImportDoc

          Description: Read a Report file  and save the result in file with XML format


          Parameters : sReportFile: Report File
                        sURLPrefix: URL前缀路径
                        handle: NERICS handle, generated by NERICS_NewInstance
          Returns    : Return result file name: sXMLFile: XML file stored
          Author     : Kevin Zhang
          History    :
              1.create 2018-5-4
        :param report_file:
        :param url_prefix:
        :param handle:
        :return:
        """
        return self.get_func("NERICS_ImportDoc", [c_char_p, c_char_p, c_int], c_char_p)(
            report_file, url_prefix, handle
        )

    @nlpir_base.NLPIRBase.byte_str_transform
    def load_doc_result(self, result_xml_file: str, handle: int = 0) -> int:
        """
          Func Name  : NERICS_LoadDocResult

          Description: Read a result XML file  and save the result in file with XML format


          Parameters : sReportFile: Report File
                        sURLPrefix: URL前缀路径
                        handle: NERICS handle, generated by NERICS_NewInstance
          Returns    : Return result file name: sXMLFile: XML file stored
          Author     : Kevin Zhang
          History    :
              1.create 2018-5-4
        :param result_xml_file:
        :param handle:
        :return:
        """
        return self.get_func("NERICS_LoadDocResult", [c_char_p, c_int], c_size_t)(
            result_xml_file, handle
        )

    @nlpir_base.NLPIRBase.byte_str_transform
    def check_report_f(
            self,
            report_file: str,
            url_prefix: str = "",
            organization: str = "",
            report_type: int = RPT_UNSPECIFIC,
            format_opt: int = nlpir_base.OUTPUT_FORMAT_JSON,
            handle: str = 0) -> str:
        """

                Func Name  : NERICS_CheckReportF

        Description: Check a Report file  and save the result in file with XML format



        Parameters : sReportFile: Report File: 支持doc,docx,xml文件
                    sURLPrefix: URL前缀路径
                    nType: Report Type, Default is RPT_UNSPECIFIC
                    handle: NERICS handle, generated by NERICS_NewInstance
                    int  nResultFormat：0: XML; 1:Jason
        Returns    : Return result file name: sXMLFile: XML file stored

        Author     : Kevin Zhang
        History    :
                  1.create 2018-5-4

        :param report_file:
        :param url_prefix:
        :param organization:
        :param report_type:
        :param format_opt:
        :param handle:
        :return:
        """
        return self.get_func("NERICS_CheckReportF", [c_char_p, c_char_p, c_char_p, c_int, c_int, c_int], c_char_p)(
            report_file,
            url_prefix,
            organization,
            report_type,
            format_opt,
            handle
        )

    @nlpir_base.NLPIRBase.byte_str_transform
    def check_report_m(
            self,
            report_text: str,
            url_prefix: str = "",
            organization: str = "",
            report_type: int = RPT_UNSPECIFIC,
            format_opt: int = nlpir_base.OUTPUT_FORMAT_JSON,
            handle: str = 0) -> str:
        """

                Func Name  : NERICS_CheckReportM

        Description: Check a Report text memory  and save the result in file with XML format



        Parameters : sReportFile: Report File: 支持doc,docx,xml文件
                    sURLPrefix: URL前缀路径
                    nType: Report Type, Default is RPT_UNSPECIFIC
                    handle: NERICS handle, generated by NERICS_NewInstance
                    int  nResultFormat：0: XML; 1:Jason
        Returns    : Return result file name: sXMLFile: XML file stored

        Author     : Kevin Zhang
        History    :
                  1.create 2018-5-4

        :param report_text:
        :param url_prefix:
        :param organization:
        :param report_type:
        :param format_opt:
        :param handle:
        :return:
        """
        return self.get_func("NERICS_CheckReportM", [c_char_p, c_char_p, c_char_p, c_int, c_int, c_int], c_char_p)(
            report_text,
            url_prefix,
            organization,
            report_type,
            format_opt,
            handle
        )

    @nlpir_base.NLPIRBase.byte_str_transform
    def extract_knowledge(
            self,
            report_text: str,
            report_type: int = RPT_UNSPECIFIC
    ) -> str:
        """

        Func Name  : NERICS_ExtractKnowledge

        Description: Extract Knowledge from a text， given a configure string with XML format
        nType: Report Type, Default is RPT_UNSPECIFIC


        Parameters : sReportFile: Report File: 支持doc,docx,xml文件
                    sURLPrefix: URL前缀路径
                    nType: Report Type, Default is RPT_UNSPECIFIC
                    handle: NERICS handle, generated by NERICS_NewInstance
                    int  nResultFormat：0: XML; 1:Jason
        Returns    : Return result file name: sXMLFile: XML file stored

        Author     : Kevin Zhang
        History    :
                  1.create 2018-5-4

        :param report_text:
        :param report_type:
        :return:
        """
        return self.get_func("NERICS_ExtractKnowledge", [c_char_p, c_int], c_char_p)(
            report_text,
            report_type,
        )

    @nlpir_base.NLPIRBase.byte_str_transform
    def get_result(self, result_type: int, handle: int = 0) -> str:
        """
        Func Name  : NERICS_GetResult

        Description: 获取分析结果，默认为JSON格式



        Parameters : result_type:
                    handle: NERICS handle, generated by NERICS_NewInstance

        Returns    : Return result file name: sXMLFile: XML file stored

        Author     : Kevin Zhang
        History    :
                  1.create 2018-5-4
        :param result_type:
        :param handle:
        :return:
        """
        return self.get_func("NERICS_GetResult", [c_char_p, c_int], c_char_p)(result_type, handle)

    @nlpir_base.NLPIRBase.byte_str_transform
    def add_audit_rule(self, audit_rule: str, report_type: int = RPT_UNSPECIFIC) -> int:
        """
        Func Name  : NERICS_AddAuditRule

        Description: Add Audit Rule



        Parameters : sAuditRule: Audit rule,需要遵循KGB Audit语法规则
                    nType: Report Type, Default is RPT_UNSPECIFIC

        Returns    : int: 1: success, other: failed. Get error message via NERICS_GetLastErrorMsg()

        Author     : Kevin Zhang
        History    :
                  1.create 2018-9-19
        :param audit_rule:
        :param report_type:
        :return:
        """
        return self.get_func("NERICS_AddAuditRule", [c_char_p, c_int], c_int)(audit_rule, report_type)

    @nlpir_base.NLPIRBase.byte_str_transform
    def check_report_dir(
            self,
            report_dir: str,
            organization: str,
            report_type: int = RPT_UNSPECIFIC,
            format_opt: int = nlpir_base.OUTPUT_FORMAT_JSON,
            thread_count: int = 10
    ) -> str:
        """
        Func Name  : NERICS_CheckReportDir

        Description: Scan a dir and  Check all doc files


        Parameters : sReportDir: Report File Directory

                    nType: Report Type, Default is RPT_UNSPECIFIC
                    handle: NERICS handle, generated by NERICS_NewInstance
        Returns    : Return result file name: sXMLFile: XML file stored
        Author     : Kevin Zhang
        History    :
                  1.create 2018-6-5
        :param report_dir:
        :param organization:
        :param report_type:
        :param format_opt:
        :param thread_count:
        :return:
        """
        return self.get_func("NERICS_CheckReportDir", [c_char_p, c_char_p, c_int, c_int, c_int], c_size_t)(
            report_dir, organization, report_type, format_opt, thread_count
        )

    @nlpir_base.NLPIRBase.byte_str_transform
    def revise_report_f(self, revise_xml_file: str, handle: int = 0) -> str:
        """
        Func Name  : NERICS_ReviseReportF

        Description: Revised a Report file
                    and revised information stored in file


        Parameters : sReviseXMLFile: Revised information file with XML format
                    nType: Report Type, Default is RPT_UNSPECIFIC
                    handle: NERICS handle, generated by NERICS_NewInstance
        Returns    : Return : new docx file name with path； return "" if failed!

        Author     : Kevin Zhang
        History    :
                  1.create 2018-5-4
        :param revise_xml_file:
        :param handle:
        :return:
        """
        return self.get_func("NERICS_ReviseReportF", [c_char_p, c_int], c_char_p)(revise_xml_file, handle)

    @nlpir_base.NLPIRBase.byte_str_transform
    def show_html_error(self, revise_xml_file: str, handle: int = 0) -> str:
        """
               Description: Revised a Report file
                    and revised information stored in file


        Parameters : sReviseXMLFile: Revised information file with XML format
                    nType: Report Type, Default is RPT_UNSPECIFIC
                    handle: NERICS handle, generated by NERICS_NewInstance
        Returns    : Return : new docx file name with path； return "" if failed!

        Author     : Kevin Zhang
        History    :
                  1.create 2018-5-4
        :param revise_xml_file:
        :param handle:
        :return:
        """
        return self.get_func("NERICS_ShowHtmlError", [c_char_p, c_int], c_char_p)(revise_xml_file, handle)

    @nlpir_base.NLPIRBase.byte_str_transform
    def import_template(
            self,
            template_file: str,
            report_type: int = RPT_UNSPECIFIC,
            org: str = "",
            area: str = "",
            argument: str = ""
    ) -> int:
        """
        Func Name  : NERICS_ImportTemplate

        Description: Import a document Template


        Parameters : sTemplateFile: Template file using doc or docx format
                    nType: document type
                    sOrg: organization
                    sArgumemt: arguments
        Returns    : Return status: int
                    1: success

        Author     : Kevin Zhang
        History    :
                  1.create 2018-5-8
                   2.modified in 2018-11-20
        :param template_file:
        :param report_type:
        :param org:
        :param area:
        :param argument:
        :return:
        """
        return self.get_func("NERICS_ImportTemplate", [c_char_p, c_int, c_char_p, c_char_p, c_char_p])(
            template_file, report_type, org, area, argument
        )

    @nlpir_base.NLPIRBase.byte_str_transform
    def edit_template(
            self,
            template_id: int,
            template_file: str,
            report_type: int = RPT_UNSPECIFIC,
            org: str = "",
            area: str = "",
            argument: str = ""
    ) -> int:
        """
        Func Name  : NERICS_EditTemplate

        Description: Edit a document Template


        Parameters : sTemplateFile: Template file using doc or docx format
                    nType: document type
                    sOrg: organization
                    sArgumemt: arguments
        Returns    : Return status: int
                    1: success

        Author     : Kevin Zhang
        History    :
                  1.create 2018-5-8
                   2.modified in 2018-11-20


        :param template_id:
        :param template_file:
        :param report_type:
        :param argument:
        :param area:
        :param org:
        :return:
        """
        return self.get_func("NERICS_EditTemplate", [c_int, c_char_p, c_int, c_char_p, c_char_p, c_char_p], c_int)(
            template_id, template_file, report_type, org, area, argument
        )

    @nlpir_base.NLPIRBase.byte_str_transform
    def find_template(self, report_type: int = RPT_UNSPECIFIC, org: str = "", area: str = "",
                      argument: str = "") -> int:
        """
        Func Name  : NERICS_FindTemplate

        Description: Find a document Template


        Parameters :
                    nType: document type
                    sOrg: organization
                    sArgumemt: arguments
        Returns    : Return status: int
                    1: success

        Author     : Kevin Zhang
        History    :
                  1.create 2018-5-8

        :param report_type:
        :param org:
        :param area:
        :param argument:
        :return:
        """
        return self.get_func("NERICS_FindTemplate", [c_int, c_char_p, c_char_p, c_char_p], c_int)(
            report_type, org, area, argument
        )

    @nlpir_base.NLPIRBase.byte_str_transform
    def delete_template(self, template_id: int) -> int:
        """
        Func Name  : NERICS_DeleteTemplate

        Description: delete a document Template


        Parameters : nTempID: template ID
        Returns    : Return : int

        Author     : Kevin Zhang
        History    :
                  1.create 2018-11-20
        :param template_id:
        :return:
        """
        return self.get_func("NERICS_DeleteTemplate", [c_int], c_int)(template_id)

    @nlpir_base.NLPIRBase.byte_str_transform
    def get_template(self, template_id: int) -> str:
        """
        Func Name  : NERICS_GetTemplate

        Description: Get a document Template


        Parameters : nTempID: template ID
        Returns    : Return status: const char* :template data

        Author     : Kevin Zhang
        History    :
                  1.create 2018-11-20

        :param template_id:
        :return:
        """
        return self.get_func("NERICS_GetTemplate", [c_int], c_char_p)(template_id)

    @nlpir_base.NLPIRBase.byte_str_transform
    def get_template_count(self, template_id: int) -> str:
        """
        Func Name  : NERICS_GetTemplateCount

        Description: Get  document Template count


        Parameters : nTempID: template ID
        Returns    : Return status: const char* :template data

        Author     : Kevin Zhang
        History    :
                  1.create 2018-11-20

        :param template_id:
        :return:
        """
        return self.get_func("NERICS_GetTemplateCount", [c_int], c_size_t)(template_id)

    @nlpir_base.NLPIRBase.byte_str_transform
    def get_current_template_info(self, handle: int = 0) -> str:
        """
        Func Name  : NERICS_GetCurTemplateInfo

        Description: Get current document Template information


        Parameters :
        Returns    : Return status: const char* :template information using Jason format

        Author     : Kevin Zhang
        History    :
                  1.create 2018-12-5
        :param handle:
        :return:
        """
        return self.get_func("NERICS_GetCurTemplateInfo", [c_int], c_char_p)(handle)

    @nlpir_base.NLPIRBase.byte_str_transform
    def get_template_list(self, doc_type: int, organization: str) -> c_char_p:
        """
        Func Name  : NERICS_GetTemplateList

        Description: Get  Template information


        Parameters :	docType: docType;
                    sOrgnization: organization name
        Returns    : Return status: const char* :template information using Jason format

        Author     : Kevin Zhang
        History    :
                  1.create 2018-12-5

        :param doc_type:
        :param organization:
        :return:
        """
        return self.get_func("NERICS_GetTemplateList", [c_int, c_char_p], c_char_p)(doc_type, organization)

    @nlpir_base.NLPIRBase.byte_str_transform
    def re_check_format(
            self,
            check_xml: str,
            template_id: int,
            format_opt: int = nlpir_base.OUTPUT_FORMAT_JSON,
            handle: int = 0

    ) -> str:
        """
        Func Name  : NERICS_ReCheckFormat

        Description: ReCheck a format

        Parameters : sReportFile: Report File: 支持doc,docx,xml文件
                    sURLPrefix: URL前缀路径
                    nType: Report Type, Default is RPT_UNSPECIFIC
                    handle: NERICS handle, generated by NERICS_NewInstance
                    int  nResultFormat：0: XML; 1:Jason
        Returns    : Return result file name: sXMLFile: XML file stored

        Author     : Kevin Zhang
        History    :
                  1.create 2018-11-27

        :param check_xml:
        :param template_id:
        :param format_opt:
        :param handle:
        :return:
        """
        return self.get_func("NERICS_ReCheckFormat", [c_char_p, c_int, c_int, c_int], c_char_p)(
            check_xml, template_id, format_opt, handle
        )

    @nlpir_base.NLPIRBase.byte_str_transform
    def import_kgb_rules(self, rule_file: str, overwrite: bool = False, report_type: int = RPT_UNSPECIFIC) -> c_int:
        """
        Func Name  : NERICS_ImportKGBRules

        Description: 针对报告类型nType导入相应的KGB规则集合


        Parameters : sTemplateFile: Template file using doc or docx format
        Returns    : Return status: int
                    1: success

        Author     : Kevin Zhang
        History    :
                  1.create 2018-5-8

        :param rule_file:
        :param overwrite:
        :param report_type:
        :return:
        """
        return self.get_func("NERICS_ImportKGBRules", [c_char_p, c_bool, c_int], c_int)(
            rule_file,
            overwrite,
            report_type
        )

    @nlpir_base.NLPIRBase.byte_str_transform
    def import_kgb_rules_from_mem(self, rule_text: str, overwrite: bool = False,
                                  report_type: int = RPT_UNSPECIFIC) -> int:
        """
        Func Name  : NERICS_ImportKGBRulesFromMem

        Description: 针对报告类型nType导入相应的KGB规则集合


        Parameters : sTemplateFile: Template file using doc or docx format
        Returns    : Return status: int
                    1: success

        Author     : Kevin Zhang
        History    :
                  1.create 2018-5-8

        :param rule_text
        :param overwrite:
        :param report_type:
        :return:
        """
        return self.get_func("NERICS_ImportKGBRulesFromMem", [c_char_p, c_bool, c_int], c_int)(
            rule_text,
            overwrite,
            report_type
        )

    @nlpir_base.NLPIRBase.byte_str_transform
    def import_error_msg(self, error_list_file: str) -> int:
        """
        Func Name  : NERICS_ImportErrorMsg

        Description: Import a error message table


        Parameters : sErrorListFile: Template file using doc or docx format
        Returns    : Return status: int
                    1: success

        Author     : Kevin Zhang
        History    :
                  1.create 2018-5-8
        :param error_list_file:
        :return:
        """
        return self.get_func("NERICS_ImportErrorMsg", [c_char_p], c_int)(error_list_file)

    @nlpir_base.NLPIRBase.byte_str_transform
    def import_sim_dict(self, sim_dict_file: str) -> c_int:
        """
        Func Name  : NERICS_ImportSimDict

        Description: Import simary dictionary


        Parameters : sErrorListFile: Template file using doc or docx format
        Returns    : Return status: int
                    1: success

        Author     : Kevin Zhang
        History    :
                  1.create 2018-5-8

        :param sim_dict_file:
        :return:
        """
        return self.get_func("NERICS_ImportSimDict", [c_char_p], c_int)(sim_dict_file)

    @nlpir_base.NLPIRBase.byte_str_transform
    def import_spell_error_dict(self, spell_error_dict: str) -> int:
        """
        Func Name  : NERICS_ImportSpellErrorDict

        Description: Import Spelling Error dictionary


        Parameters : sSpellErrorDict: Spelling Error dictionary
        Returns    : Return status: int
                    1: success

        Author     : Kevin Zhang
        History    :
                  1.create 2018-5-8
        :param spell_error_dict:
        :return:
        """
        return self.get_func("NERICS_ImportSpellErrorDict", [c_char_p], c_int)(spell_error_dict)

    @nlpir_base.NLPIRBase.byte_str_transform
    def import_user_dict(self, user_dict: str):
        """
        Func Name  : NERICS_ImportUserDict

        Description: Import Spelling Error dictionary


        Parameters : sUserDict: User defined dictionary
        Returns    : Return status: int
                    1: success

        Author     : Kevin Zhang
        History    :
                  1.create 2019-12-3

        :param user_dict:
        :return:
        """
        return self.get_func("NERICS_ImportUserDict", [c_char_p], c_int)(user_dict)

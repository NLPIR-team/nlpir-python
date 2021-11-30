#! coding=utf-8
"""
KGB
"""
import json
import os
import re
import typing
from enum import Enum
from pathlib import Path

from pydantic import BaseModel

import nlpir
from nlpir import get_instance as __get_instance__
from nlpir import native

# class and class instance
__cls__ = native.eye_checker.EyeChecker
__instance__: typing.Optional[native.eye_checker.EyeChecker] = None
# Location of DLL
__lib__ = None
# Data directory
__data__ = None
# license_code
__license_code__ = None
# encode
__nlpir_encode__ = native.UTF8_CODE


class KGBItem(BaseModel):
    attribute: str
    id: int
    key_value: str
    name: str
    offset: int
    org_para_text: str
    para_id: str
    rule_used: str


class KGBSingleKeyResult(BaseModel):
    key_value: typing.List[KGBItem]


class KGBTableResult(BaseModel):
    pass


class KGBTupleResult(BaseModel):
    index: int
    tuple: typing.List[KGBItem]


class KGBResult(BaseModel):
    single_key_result: KGBSingleKeyResult = None
    tables: typing.List[KGBTableResult] = None
    tuples: typing.List[KGBTupleResult] = None


@__get_instance__
def get_native_instance() -> native.eye_checker.EyeChecker:
    """
    返回原生NLPIR接口,使用更多函数

    :return: The singleton instance
    """
    return __instance__


@__get_instance__
def import_kgb_rules(rule_text: str, overwrite: bool, report_type: int) -> int:
    """

    """
    return __instance__.import_kgb_rules_from_mem(rule_text, overwrite, report_type)


@__get_instance__
def extract_knowledge(
        report_text: str,
        report_type: int
) -> KGBResult:
    extract_result_text = __instance__.extract_knowledge(report_text, report_type)
    extract_result_dict = json.loads(extract_result_text) if extract_result_text is not None else dict()

    single_key_result = extract_result_dict.pop("SingleKey_result", dict())
    single_key_result["key_value"] = single_key_result.pop("KeyVals", list())
    extract_result_dict["single_key_result"] = single_key_result

    tuple_result = extract_result_dict.pop("Tuples", list())
    for i, _ in enumerate(tuple_result if tuple_result is not None else list()):
        tuple_result[i]["index"] = tuple_result[i].pop("Index")
        tuple_result[i]["tuple"] = tuple_result[i].pop("Tuple")
    extract_result_dict["tuples"] = tuple_result

    table_result = extract_result_dict.pop("Tables", list())
    # table_result = table_result if table_result is not None else list()
    extract_result_dict["tables"] = table_result
    return KGBResult(**extract_result_dict)


__kgb_rule_file_re__ = re.compile(r"KGB_(\d+)\..+")


@__get_instance__
def list_rules() -> typing.Set[int]:
    rule_set = set()
    for file in os.listdir(os.path.join(__instance__.data_path, "Data")):
        result = __kgb_rule_file_re__.search(file)
        if result is not None:
            rule_set.add(int(result.group(1)))
    return rule_set


@__get_instance__
def delete_rules(rule: int):
    kgb_path = os.path.join(__instance__.data_path, "Data")
    for file in os.listdir(kgb_path):
        result = __kgb_rule_file_re__.search(file)
        if result is not None:
            if int(result.group(1)) == rule:
                os.remove(os.path.join(kgb_path, file))

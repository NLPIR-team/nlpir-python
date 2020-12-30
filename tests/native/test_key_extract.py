# coding=utf-8
"""
Tested function:

- :func:`nlpir.native.key_extract.KeyExtract.init_lib`
- :func:`nlpir.native.key_extract.KeyExtract.exit_lib`
- :func:`nlpir.native.key_extract.KeyExtract.get_keywords`
- :func:`nlpir.native.key_extract.KeyExtract.import_user_dict`
- :func:`nlpir.native.key_extract.KeyExtract.add_user_word`
- :func:`nlpir.native.key_extract.KeyExtract.clean_user_word`
- :func:`nlpir.native.key_extract.KeyExtract.save_the_usr_dict`
- :func:`nlpir.native.key_extract.KeyExtract.del_usr_word`
- :func:`nlpir.native.key_extract.KeyExtract.get_last_error_msg`
"""
from nlpir.native import KeyExtract
from nlpir import native, PACKAGE_DIR, clean_logs
import os
import re
import json
import logging
import pytest
from ..strings import test_str, test_str_2nd, user_dict_path

json_out = native.OUTPUT_FORMAT_JSON


def get_key_extract(encode=native.UTF8_CODE):
    return KeyExtract(encode=encode)


@pytest.mark.run(order=-1)
def test_init_exit():
    key_extract = get_key_extract()
    key_extract.exit_lib()
    clean_logs(include_current=True)


def test_extract_keys():
    key_extract = get_key_extract()
    match_tag = re.compile(r"(.+?)/([a-z0-9A-Z]+)/([.\d]+)/(\d+)#")
    assert match_tag.findall(key_extract.get_keywords(test_str, 50, format_opt=native.OUTPUT_FORMAT_SHARP))
    assert json.loads(key_extract.get_keywords(test_str, 50, format_opt=json_out))

    assert len(json.loads(key_extract.get_keywords(test_str, 5, format_opt=json_out))) >= 5
    clean_logs(include_current=True)


@pytest.mark.run(order=-3)
def test_import_user_dict():
    # test add and delete single word
    key_extract = get_key_extract()
    assert "孟德斯鸠" not in [i["word"] for i in json.loads(key_extract.get_keywords(test_str, 50, format_opt=json_out))]
    key_extract.add_user_word("孟德斯鸠")
    assert "孟德斯鸠" in [i["word"] for i in json.loads(key_extract.get_keywords(test_str, 500, format_opt=json_out))]
    key_extract.del_usr_word("孟德斯鸠")
    assert "孟德斯鸠" not in [i["word"] for i in json.loads(key_extract.get_keywords(test_str, 50, format_opt=json_out))]
    key_extract.add_user_word("孟德斯鸠")
    assert "孟德斯鸠" in [i["word"] for i in json.loads(key_extract.get_keywords(test_str, 50, format_opt=json_out))]
    key_extract.clean_user_word()
    assert "孟德斯鸠" not in [i["word"] for i in json.loads(key_extract.get_keywords(test_str, 50, format_opt=json_out))]

    # test add and delete multi word with import_user_dict
    user_dict = """卢梭 user\n社会契约论 user\n"""
    with open(user_dict_path, "w", encoding="utf-8") as f:
        f.write(user_dict)
    assert "卢梭" not in [i["word"] for i in json.loads(key_extract.get_keywords(test_str_2nd, 50, format_opt=json_out))]
    # 导入词典对应文件为FieldDict.pdat FieldDict.pos 初始状态下位空,可以删除 这里测试是导入测试后将其删除
    key_extract.import_user_dict(user_dict_path, True)
    assert "卢梭" not in [i["word"] for i in json.loads(key_extract.get_keywords(test_str_2nd, 50, format_opt=json_out))]

    try:
        os.remove(user_dict_path)
        os.remove(os.path.join(PACKAGE_DIR, "Data/FieldDict.pdat"))
        os.remove(os.path.join(PACKAGE_DIR, "Data/FieldDict.pos"))
        os.remove(os.path.join(PACKAGE_DIR, "Data/UserDefinedDict.lst"))
        os.remove(os.path.join(PACKAGE_DIR, "Data/UserDict.pdat"))
    except FileNotFoundError as e:
        logging.warning(e)
    clean_logs(include_current=True)


def test_last_error_msg():
    msg = get_key_extract().get_last_error_msg()
    assert msg is not None
    clean_logs(include_current=True)

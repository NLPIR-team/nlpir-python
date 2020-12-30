# coding=utf-8
"""
Tested Function:

- :func:`nlpir.native.ictclas.ICTCLAS.exit_lib`
- :func:`nlpir.native.ictclas.ICTCLAS.paragraph_process`
- :func:`nlpir.native.ictclas.ICTCLAS.ictclas.paragraph_process_a`
- :func:`nlpir.native.ictclas.ICTCLAS.file_process`
- :func:`nlpir.native.ictclas.ICTCLAS.add_user_word`
- :func:`nlpir.native.ictclas.ICTCLAS.del_usr_word`
- :func:`nlpir.native.ictclas.ICTCLAS.clean_user_word`
- :func:`nlpir.native.ictclas.ICTCLAS.import_user_dict`
- :func:`nlpir.native.ictclas.ICTCLAS.get_uni_prob`
- :func:`nlpir.native.ictclas.ICTCLAS.is_word`
- :func:`nlpir.native.ictclas.ICTCLAS.is_user_word`
- :func:`nlpir.native.ictclas.ICTCLAS.get_word_pos`
- :func:`nlpir.native.ictclas.ICTCLAS.set_pos_map`
- :func:`nlpir.native.ictclas.ICTCLAS.finer_segment`
- :func:`nlpir.native.ictclas.ICTCLAS.word_freq_stat`
- :func:`nlpir.native.ictclas.ICTCLAS.file_word_freq_stat`
- :func:`nlpir.native.ictclas.ICTCLAS.get_eng_word_origin`
- :func:`nlpir.native.ictclas.ICTCLAS.get_last_error_msg`
"""
from nlpir.native import ICTCLAS
from nlpir import native, PACKAGE_DIR, clean_logs
import os
import re
import logging
from ..strings import test_str, test_str_1st, test_str_2nd, test_source_filename, test_result_filename, user_dict_path
import pytest


def get_ictclas(encode=native.UTF8_CODE):
    return ICTCLAS(encode=encode)


@pytest.mark.run(order=-1)
def test_init_exit():
    ictclas = get_ictclas()
    ictclas.exit_lib()
    clean_logs(include_current=True)


def test_paragraph_process():
    ictclas = get_ictclas()
    test_str_seg_pos = '法国/nsf 启蒙/vn 思想家/n 孟德斯/nrf 鸠/n 曾/d 说/v 过/uguo ：/wm “/wyz 一切/rz 有/vyou 权力/n ' \
                       '的/ude1 人/n 都/d 容易/ad 滥用/v 权力/n ，/wd 这/rzv 是/vshi 一/m 条/q 千古/n 不/d 变/v 的/ude1 经' \
                       '验/n 。/wj 有/vyou 权力/n 的/ude1 人/n 直到/v 把/pba 权力/n 用到/v 极限/n 方可/d 休止/vi 。/wj ”/wyy' \
                       ' 另/rz 一/m 法国/nsf 启蒙/vn 思想家/n 卢/nr1 梭/ng 从/p 社会/n 契约/n 论/k 的/ude1 观点/n 出发/vi ' \
                       '，/wd 认为/v 国家/n 权力/n 是/vshi 公民/n 让/v 渡/v 其/rz 全部/m “/wyz 自然/n 权利/n ”/wyy 而/cc ' \
                       '获得/v 的/ude1 ，/wd 他/rr 在/p 其/rz 名著/n 《/wkz 社会/n 契约/n 论/v 》/wky 中/f 写道/v ：/wm ' \
                       '“/wyz 任何/rz 国家/n 权力/n 无不/d 是/vshi 以/p 民众/n 的/ude1 权力/n （/wkz 权利/n ）/wky 让/v ' \
                       '渡/v 与/p 公众/n 认可/vi 作为/p 前提/n 的/ude1 ”/wyy 。/wj '

    test_str_seg = '法国 启蒙 思想家 孟德斯 鸠 曾 说 过 ： “ 一切 有 权力 的 人 都 容易 滥用 权力 ， 这 是 一 条 千古 不 变 的' \
                   ' 经验 。 有 权力 的 人 直到 把 权力 用到 极限 方可 休止 。 ” 另 一 法国 启蒙 思想家 卢 梭 从 社会 契约' \
                   ' 论 的 观点 出发 ， 认为 国家 权力 是 公民 让 渡 其 全部 “ 自然 权利 ” 而 获得 的 ， 他 在 其 名' \
                   '著 《 社会 契约 论 》 中 写道 ： “ 任何 国家 权力 无不 是 以 民众 的 权力 （ 权利 ） 让 渡 与 公众' \
                   ' 认可 作为 前提 的 ” 。 '

    assert test_str_seg == ictclas.paragraph_process(test_str, 0)
    assert test_str_seg_pos == ictclas.paragraph_process(test_str, 1)
    clean_logs(include_current=True)


def test_paragraph_process_a():
    ictclas = get_ictclas()
    result, result_count = ictclas.paragraph_process_a(test_str, True)
    assert result_count == 110
    clean_logs(include_current=True)


def test_file_process():
    ictclas = get_ictclas()
    ictclas.file_process(
        os.path.abspath(test_source_filename),
        os.path.abspath(test_result_filename) + ".native.test_ictclas.test_file_process",
        1
    )
    os.remove(test_result_filename + ".native.test_ictclas.test_file_process")
    clean_logs(include_current=True)


@pytest.mark.run(order=-3)
def test_import_user_dict():
    # test add and delete single word
    test_str_seg = '法国/nsf 启蒙/vn 思想家/n 孟德斯/nrf 鸠/n 曾/d 说/v 过/vf '
    test_str_seg_with_dict = '法国/nsf 启蒙/vn 思想家/n 孟德斯鸠/n 曾/d 说/v 过/vf '
    ictclas = get_ictclas()
    assert test_str_seg == ictclas.paragraph_process(test_str_1st)
    ictclas.add_user_word("孟德斯鸠")
    assert test_str_seg_with_dict == ictclas.paragraph_process(test_str_1st)
    ictclas.del_usr_word("孟德斯鸠")
    assert test_str_seg == ictclas.paragraph_process(test_str_1st)
    ictclas.add_user_word("孟德斯鸠")
    assert test_str_seg_with_dict == ictclas.paragraph_process(test_str_1st)
    ictclas.clean_user_word()
    assert test_str_seg == ictclas.paragraph_process(test_str_1st)

    # test add and delete multi word with import_user_dict
    test_str_seg = '另/rz 一/m 法国/nsf 启蒙/vn 思想家/n 卢/nr1 梭/ng 从/p 社会/n 契约/n 论/k 的/ude1 观点/n 出发/vi ，/wd' \
                   ' 认为/v 国家/n 权力/n 是/vshi 公民/n 让/v 渡/v 其/rz 全部/m “/wyz 自然/n 权利/n ”/wyy 而/cc 获得/v 的/ude1 '
    test_str_seg_with_dict = '另/rz 一/m 法国/nsf 启蒙/vn 思想家/n 卢梭/user 从/p 社会契约论/user 的/ude1 观点/n 出发/vi ，/wd' \
                             ' 认为/v 国家/n 权力/n 是/vshi 公民/n 让/v 渡/v 其/rz 全部/m “/wyz 自然/n 权利/n ”/wyy 而/cc 获得/v 的/ude1 '
    user_dict = """卢梭 user\n社会契约论 user\n"""
    with open(user_dict_path, "w", encoding="utf-8") as f:
        f.write(user_dict)
    assert test_str_seg == ictclas.paragraph_process(test_str_2nd)
    # 导入词典对应文件为FieldDict.pdat FieldDict.pos 初始状态下位空,可以删除 这里测试是导入测试后将其删除
    ictclas.import_user_dict(user_dict_path, True)
    assert test_str_seg_with_dict == ictclas.paragraph_process(test_str_2nd)
    try:
        os.remove(user_dict_path)
        os.remove(os.path.join(PACKAGE_DIR, "Data/FieldDict.pdat"))
        os.remove(os.path.join(PACKAGE_DIR, "Data/FieldDict.pos"))
        os.remove(os.path.join(PACKAGE_DIR, "Data/UserDefinedDict.lst"))
    except FileNotFoundError as e:
        logging.warning(e)
    clean_logs(include_current=True)


def test_user_dict():
    ictclas = get_ictclas()
    test_str_seg = ictclas.paragraph_process(test_str_2nd)
    # 不可以传空字符串, is_word会出错 TODO 加入文档
    test_word_list = re.split(r"/[a-z0-9]+ ", test_str_seg)[:-1]
    for word in test_word_list:
        ictclas.get_uni_prob(word)
        ictclas.is_word(word)
        ictclas.is_user_word(word)
        ictclas.get_word_pos(word)
    clean_logs(include_current=True)


def test_pos_map():
    test_str_pku_1st = '另/r 一/m 法国/n 启蒙/v 思想家/n'
    test_str_pku_2nd = '另/r 一/m 法国/ns 启蒙/vn 思想家/n'
    test_str_ict_1st = '另/r 一/m 法国/n 启蒙/v 思想家/n'
    test_str_ict_2nd = '另/rz 一/m 法国/nsf 启蒙/vn 思想家/n'
    ictclas = get_ictclas()
    ictclas.set_pos_map(ICTCLAS.PKU_POS_MAP_FIRST)
    assert test_str_pku_1st in ictclas.paragraph_process(test_str_2nd)
    ictclas.set_pos_map(ICTCLAS.PKU_POS_MAP_SECOND)
    assert test_str_pku_2nd in ictclas.paragraph_process(test_str_2nd)
    ictclas.set_pos_map(ICTCLAS.ICT_POS_MAP_FIRST)
    assert test_str_ict_1st in ictclas.paragraph_process(test_str_2nd)
    ictclas.set_pos_map(ICTCLAS.ICT_POS_MAP_SECOND)
    assert test_str_ict_2nd in ictclas.paragraph_process(test_str_2nd)
    clean_logs(include_current=True)


def test_finer_segment():
    test_str_seg = '另 一 法国 启蒙 思想家 卢 梭 从 社会 契约 论 的 观点 出发 ， 认为 国家 权力 是 公民 让 渡 其 全部 “ 自然 权利 ” 而 获得 的 '
    ictclas = get_ictclas()
    assert test_str_seg == ictclas.finer_segment(test_str_2nd)
    clean_logs(include_current=True)


def test_frq_count():
    ictclas = get_ictclas()
    assert re.match(r".+?/[0-9]+#", ictclas.word_freq_stat(test_str))
    assert re.match(r".+?/[0-9]+#", ictclas.file_word_freq_stat(test_source_filename))
    clean_logs(include_current=True)


def test_get_eng_word_origin():
    test_str_eng = "We hold these truths to be self-evident, that all men are created equal, that they are endowed " \
                   "by their Creator with certain unalienable Rights, that among these are Life, Liberty and the " \
                   "pursuit of Happiness."
    test_str_eng_result = "we hold this truth to be self-evident, that all man be create equal, that they be endow" \
                          " by their creator with certain unalienable rights, that among this be life, liberty and" \
                          " the pursuit of happiness."
    ictclas = get_ictclas()
    for w, r in zip(test_str_eng.split(), test_str_eng_result.split()):
        assert r == ictclas.get_eng_word_origin(w)
    clean_logs(include_current=True)


def test_last_error_msg():
    msg = get_ictclas().get_last_error_msg()
    logging.info(msg)
    assert msg is not None
    clean_logs(include_current=True)

# coding=utf-8
from nlpir.native import ICTCLAS
from nlpir import native, PACKAGE_DIR
import os
import re
import logging

test_str = "法国启蒙思想家孟德斯鸠曾说过：“一切有权力的人都容易滥用权力，这是一条千古不变的经验。有权力的人直到把权力用到" \
           "极限方可休止。”另一法国启蒙思想家卢梭从社会契约论的观点出发，认为国家权力是公民让渡其全部“自然权利”而获得的，" \
           "他在其名著《社会契约论》中写道：“任何国家权力无不是以民众的权力（权利）让渡与公众认可作为前提的”。"
test_str_1st = "法国启蒙思想家孟德斯鸠曾说过"
test_str_2nd = "另一法国启蒙思想家卢梭从社会契约论的观点出发，认为国家权力是公民让渡其全部“自然权利”而获得的"
test_source_filename = "native/test.txt"


def get_ictclas(encode=native.UTF8_CODE):
    return ICTCLAS(encode=encode)


def test_init_exit():
    ictclas = get_ictclas()
    ictclas.exit_lib()


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

    # ictclas.paragraph_process_a(test_str, result_count, user_dict)
    # ictclas.get_paragraph_process_a_word_count(paragraph)
    # ictclas.paragraph_process_aw(count, result)


def test_paragraph_process_a():
    ictclas = get_ictclas()
    result, result_count = ictclas.paragraph_process_a(test_str, True)
    assert result_count == 110


def test_file_process():
    ictclas = get_ictclas()
    test_result_filename = "native/test_result.txt"
    ictclas.file_process(os.path.abspath(test_source_filename), os.path.abspath(test_result_filename), 1)
    os.remove(test_result_filename)


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
    user_dict_path = "native/tmp_user_dict.txt"
    with open("native/tmp_user_dict.txt", "w") as f:
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


def test_user_dict():
    ictclas = get_ictclas()
    test_str_seg = ictclas.paragraph_process(test_str_2nd)
    # 不可以传空字符串, is_word会出错 TODO 加入文档
    test_word_list = re.split(r"/[a-z0-9]+ ", test_str_seg)[:-1]
    for word in test_word_list:
        ictclas.get_uni_prob(word)
        ictclas.is_word(word)
        # ictclas.is_user_word(word)
        ictclas.get_word_pos(word)


def test_pos_map():
    test_str_pku_1st = '另/r 一/m 法国/n 启蒙/v 思想家/n 卢/n 梭/g 从/p 社会/n 契约/n 论/k 的/u 观点/n 出发/v ，/w 认为/v ' \
                       '国家/n 权力/n 是/v 公民/n 让/v 渡/v 其/r 全部/m “/w 自然/n 权利/n ”/w 而/c 获得/v 的/u '
    test_str_pku_2nd = '另/r 一/m 法国/ns 启蒙/vn 思想家/n 卢/nr 梭/g 从/p 社会/n 契约/n 论/k 的/u 观点/n 出发/v ，/w 认为/v ' \
                       '国家/n 权力/n 是/v 公民/n 让/v 渡/v 其/r 全部/m “/w 自然/n 权利/n ”/w 而/cc 获得/v 的/u '
    test_str_ict_1st = '另/r 一/m 法国/n 启蒙/v 思想家/n 卢/n 梭/n 从/p 社会/n 契约/n 论/k 的/u 观点/n 出发/v ，/w 认为/v ' \
                       '国家/n 权力/n 是/v 公民/n 让/v 渡/v 其/r 全部/m “/w 自然/n 权利/n ”/w 而/c 获得/v 的/u '
    test_str_ict_2nd = '另/rz 一/m 法国/nsf 启蒙/vn 思想家/n 卢/nr1 梭/ng 从/p 社会/n 契约/n 论/k 的/ude1 观点/n 出发/vi' \
                       ' ，/wd 认为/v 国家/n 权力/n 是/vshi 公民/n 让/v 渡/v 其/rz 全部/m “/wyz 自然/n 权利/n ”/wyy 而/cc 获得/v 的/ude1 '
    ictclas = get_ictclas()
    ictclas.set_pos_map(ICTCLAS.PKU_POS_MAP_FIRST)
    assert test_str_pku_1st == ictclas.paragraph_process(test_str_2nd)
    ictclas.set_pos_map(ICTCLAS.PKU_POS_MAP_SECOND)
    assert test_str_pku_2nd == ictclas.paragraph_process(test_str_2nd)
    ictclas.set_pos_map(ICTCLAS.ICT_POS_MAP_FIRST)
    assert test_str_ict_1st == ictclas.paragraph_process(test_str_2nd)
    ictclas.set_pos_map(ICTCLAS.ICT_POS_MAP_SECOND)
    assert test_str_ict_2nd == ictclas.paragraph_process(test_str_2nd)


def test_finer_segment():
    test_str_seg = '另 一 法国 启蒙 思想家 卢 梭 从 社会 契约 论 的 观点 出发 ， 认为 国家 权力 是 公民 让 渡 其 全部 “ 自然 权利 ” 而 获得 的 '
    ictclas = get_ictclas()
    assert test_str_seg == ictclas.finer_segment(test_str_2nd)


def test_frq_count():
    test_str_frq = '权力/n/7#是/vshi/3#思想家/n/2#权利/n/2#渡/v/2#让/v/2#有/vyou/2#法国/nsf/2#人/n/2#国家/n/2#契约/n/2#' \
                   '启蒙/vn/2#一/m/2#社会/n/2#变/v/1#经验/n/1#直到/v/1#用到/v/1#极限/n/1#休止/vi/1#卢/nr1/1#梭/ng/1#千古/n/1#' \
                   '滥用/v/1#观点/n/1#出发/vi/1#认为/v/1#容易/ad/1#公民/n/1#说/v/1#鸠/n/1#全部/m/1#自然/n/1#孟德斯/nrf/1#' \
                   '获得/v/1#名著/n/1#论/v/1#写道/v/1#民众/n/1#公众/n/1#认可/vi/1#前提/n/1#'

    ictclas = get_ictclas()
    assert test_str_frq == ictclas.word_freq_stat(test_str)
    assert ictclas.file_word_freq_stat(test_source_filename)


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


def test_last_error_msg():
    msg = get_ictclas().get_last_error_msg()
    logging.info(msg)
    assert msg is not None

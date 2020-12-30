from nlpir import ictclas
import nlpir
import pytest


def test_segment():
    from tests.strings import test_str
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
    # 1st segment string
    assert test_str_seg.split(" ") == ictclas.segment(test_str, pos_tagged=False, post_process=ictclas.process_to_list)
    # 2nd segment string with tagging
    assert tuple(test_str_seg_pos[:6].split("/")) == ictclas.segment(
        test_str,
        pos_tagged=True,
        post_process=ictclas.process_to_list
    )[0]
    # 3rd segment string to iterator
    for i in ictclas.segment(test_str, pos_tagged=False, post_process=ictclas.process_to_generator):
        assert i == test_str_seg.split(" ")[0]
        break
    # 4th segment string to iterator with tagging
    for i in ictclas.segment(test_str, pos_tagged=True, post_process=ictclas.process_to_list):
        assert i == tuple(test_str_seg_pos[:6].split("/"))
        break
    # 5th segment with multiprocess
    from multiprocessing import Pool
    with Pool(16) as pool:
        result = pool.map(ictclas.segment, [test_str] * 100)
        assert result
    # 6th segment to string
    assert test_str_seg == ictclas.segment(test_str, pos_tagged=False, post_process=lambda t, _: t)
    assert test_str_seg_pos == ictclas.segment(test_str, pos_tagged=True, post_process=lambda t, _: t)
    nlpir.clean_logs(include_current=True)


@pytest.mark.run(order=-2)
def test_dict():
    from tests.strings import test_str_1st, test_str_2nd
    # test add and delete single word
    test_str_seg = '法国/nsf 启蒙/vn 思想家/n 孟德斯/nrf 鸠/n 曾/d 说/v 过/vf '
    test_str_seg_with_dict = '法国/nsf 启蒙/vn 思想家/n 孟德斯鸠/n 曾/d 说/v 过/vf '
    assert test_str_seg == ictclas.segment(test_str_1st, pos_tagged=True, post_process=lambda t, _: t)
    ictclas.import_dict(["孟德斯鸠"])
    assert test_str_seg_with_dict == ictclas.segment(test_str_1st, pos_tagged=True, post_process=lambda t, _: t)
    ictclas.delete_user_word(["孟德斯鸠"])
    assert test_str_seg == ictclas.segment(test_str_1st, pos_tagged=True, post_process=lambda t, _: t)
    ictclas.import_dict(["孟德斯鸠"])
    assert test_str_seg_with_dict == ictclas.segment(test_str_1st, pos_tagged=True, post_process=lambda t, _: t)
    ictclas.clean_user_dict()
    assert test_str_seg == ictclas.segment(test_str_1st, pos_tagged=True, post_process=lambda t, _: t)

    # test add and delete multi word with import_user_dict
    test_str_seg = '另/rz 一/m 法国/nsf 启蒙/vn 思想家/n 卢/nr1 梭/ng 从/p 社会/n 契约/n 论/k 的/ude1 观点/n 出发/vi ，/wd' \
                   ' 认为/v 国家/n 权力/n 是/vshi 公民/n 让/v 渡/v 其/rz 全部/m “/wyz 自然/n 权利/n ”/wyy 而/cc 获得/v 的/ude1 '
    test_str_seg_with_dict = '另/rz 一/m 法国/nsf 启蒙/vn 思想家/n 卢梭/user 从/p 社会契约论/user 的/ude1 观点/n 出发/vi ，/wd' \
                             ' 认为/v 国家/n 权力/n 是/vshi 公民/n 让/v 渡/v 其/rz 全部/m “/wyz 自然/n 权利/n ”/wyy 而/cc 获得/v 的/ude1 '
    user_dict = ["卢梭 user", "社会契约论 user"]
    assert test_str_seg == ictclas.segment(test_str_2nd, pos_tagged=True, post_process=lambda t, _: t)
    ictclas.import_dict(user_dict)
    assert test_str_seg_with_dict == ictclas.segment(test_str_2nd, pos_tagged=True, post_process=lambda t, _: t)
    assert ictclas.clean_saved_user_dict()
    nlpir.clean_logs(include_current=True)


def test_file_segment():
    from tests.strings import test_source_filename, test_result_filename
    import os
    ictclas.file_segment(
        os.path.abspath(test_source_filename),
        os.path.abspath(test_result_filename) + ".test_ictclas.test_file_segment"
    )
    os.remove(test_result_filename + ".test_ictclas.test_file_segment")
    nlpir.clean_logs(include_current=True)

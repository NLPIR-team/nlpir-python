#! coding=utf-8
"""
high-level toolbox for Chinese Word Segmentation
"""
import re
import typing
import nlpir
from nlpir import get_instance as __get_instance__
from nlpir import native

# class and class instance
__cls__ = native.ictclas.ICTCLAS
__instance__: typing.Optional[native.ictclas.ICTCLAS] = None
# Location of DLL
__lib__ = None
# Data directory
__data__ = None
# license_code
__license_code__ = None
# encode
__nlpir_encode__ = native.UTF8_CODE


@__get_instance__
def get_native_instance() -> native.ictclas.ICTCLAS:
    """
    返回原生NLPIR接口,使用更多函数

    :return: The singleton instance
    """
    return __instance__


match_tag = re.compile(r"(.+?)/([a-z0-9A-Z]+) ")


def process_to_list(txt: str, pos_tag: bool) -> list:
    """
    Default function for ``post_process`` arg in :func:`nlpir.ictclas.segment`,
    which get list of tuple if it has POS tag, or get list of words

    函数 :func:`nlpir.ictclas.segment` 的 ``post_process`` 的默认参数, 使得分词函数
    的输出为一个列表, 列表中的内容在进行词性标注时为 tuple, 内容为词和词性. 不进行词性标注时
    直接为分词后的词.

    **本函数不可直接调用,仅作为 :func:`nlpir.ictclas.segment` 的参数才有意义**


    :param txt: Segmented string
    :param pos_tag: The segmented string has POS tag or not
    :return: list of tuple of list of word

    Without POS tag::

        [
            '法国', '启蒙', '思想家', '孟德斯', '鸠', '曾', '说', '过', '：', '“', '一切', '有', '权力',
            '的', '人', '都', '容易', '滥用', '权力', '，', '这', '是', '一', '条', '千古', '不', '变',
            '的', '经验', '。'
        ]

    With POS tag::

        [
            ('法国', 'nsf'), ('启蒙', 'vn'), ('思想家', 'n'), ('孟德斯', 'nrf'), ('鸠', 'n'), ('曾', 'd'),
            ('说', 'v'), ('过', 'uguo'), ('：', 'wm'), ('“', 'wyz'), ('一切', 'rz'), ('有', 'vyou'),
            ('权力', 'n'), ('的', 'ude1'), ('人', 'n'), ('都', 'd'), ('容易', 'ad'), ('滥用', 'v'),
            ('权力', 'n'), ('，', 'wd'), ('这', 'rzv'), ('是', 'vshi'), ('一', 'm'), ('条', 'q'), ('千古', 'n'),
            ('不', 'd'), ('变', 'v'), ('的', 'ude1'), ('经验', 'n'), ('。', 'wj'), ('有', 'vyou'), ('权力', 'n'),
            ('的', 'ude1'), ('人', 'n'), ('直到', 'v'), ('把', 'pba'), ('权力', 'n'), ('用到', 'v'),
            ('极限', 'n'), ('方可', 'd'), ('休止', 'vi'), ('。', 'wj')
        ]

    """
    if pos_tag:
        return match_tag.findall(txt)
    else:
        return txt.split(" ")


def process_to_generator(text: str, pos_tag: bool) -> typing.Generator:
    """
    Same as :func:`process_to_list` ,return an iterator, save memory if the string is very large

    :func:`nlpir.ictclas.segment` 的内置的处理函数, 非默认值. 本函数可以替换 :func:`process_to_list`, 输出的结果
    为迭代器,用于获取较大长度的文本

    :param text:
    :param pos_tag:
    :return:
    """
    if pos_tag:
        for i in match_tag.finditer(text):
            yield i.groups()
    else:
        re_split = re.compile(r"[^ ]+")
        for i in re_split.finditer(text):
            yield i.group()


@__get_instance__
def import_dict(word_list: list) -> list:
    """
    See :func:`nlpir.import_dict`

    :param word_list: list of words want to add to NLPIR
    :return: the word fail to add to the NLPIR
    """
    return nlpir.import_dict(word_list=word_list, instance=__instance__)


@__get_instance__
def clean_user_dict() -> bool:
    """
    See :func:`nlpir.clean_user_dict`

    :return: success or not
    """
    return nlpir.clean_user_dict(instance=__instance__)


@__get_instance__
def delete_user_word(word_list: list):
    """
    See :func:`nlpir.delete_user_word`

    :param word_list: list of words want to delete
    """
    return nlpir.delete_user_word(word_list=word_list, instance=__instance__)


@__get_instance__
def save_user_dict() -> bool:
    """
    See :func:`nlpir.save_user_dict`

    :return: Success or not
    """
    return nlpir.save_user_dict(instance=__instance__)


@__get_instance__
def clean_saved_user_dict():
    """
    See :func:`nlpir.clean_saved_user_dict`

    :return: Delete success or not
    """
    return nlpir.clean_saved_user_dict()


@__get_instance__
def segment(txt: str, pos_tagged: bool = False, post_process: callable = process_to_list) -> typing.Any:
    """
    中文分词函数,将字符串进行分词,支持多线程和多进程分词:

    Example::

        from multiprocessing import Pool
        test_str = "法国启蒙思想家孟德斯鸠曾说过：“一切有权力的人都容易滥用权力，这是一条千古不变的经验。有权力的人直到把权力用到" \
               "极限方可休止。”另一法国启蒙思想家卢梭从社会契约论的观点出发，认为国家权力是公民让渡其全部“自然权利”而获得的，" \
               "他在其名著《社会契约论》中写道：“任何国家权力无不是以民众的权力（权利）让渡与公众认可作为前提的”。"
        with Pool(16) as pool:
            result = pool.map(ictclas.segment, [data]*100)

    默认只进行分词不进行分词标注,返回为list,可使用其他或者自行创建需要的post_process函数改变最终输出,
    post_process的输入为字符串,格式如下,分别为进行词性标注和不进行词性标注的::

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

    默认的post_process是直接将上述结果变成列表形式,若想获得字符串形式,可以使用简单的lambda表达式使post_process直接返回::

        segment(txt, pas_tagged, post_process=lambda t, _ : t)

    默认使用的标注集为 :attr:`nlpir.native.ictclas.ICTCLAS.ICT_POS_MAP_SECOND` 计算所二级标注集

    若需要进行标注集修改,使用 :func:`nlpir.native.ictclas.ICTCLAS.set_pos_map` 进行修改

    :param txt: The string want to be segmented
    :param pos_tagged: POS tagging or not
    :param post_process: The post process function, in order to get different result
    """
    return post_process(__instance__.paragraph_process(txt, pos_tagged=1 if pos_tagged else 0), pos_tagged)


@__get_instance__
def file_segment(src_path: str, tgt_path: str, pos_tagged: bool = False) -> float:
    """

    :param src_path: path of txt file
    :param tgt_path: path of result
    :param pos_tagged: POS tagging or not
    :return: time to process
    """
    return __instance__.file_process(source_filename=src_path, result_filename=tgt_path, pos_tagged=pos_tagged)

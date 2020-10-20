Tutorial
********

本文提供了本模块的基本调用方式,主要为 :mod:`nlpir` 下的各个模块的使用.除必要引用,不对 :mod:`nlpir.native`
下的内容进行介绍. :mod:`nlpir.native` 为直接调用NLPIR各个模块的方法,熟悉NLPIR调用的用户可以直接配合对应
文档使用.

:mod:`nlpir` 下的各个模块是整合了NLPIR各个模块功能,并提供一些工具方法.方便用户以更Python的方法使用NLPIR模块.

=================
Download License
=================

NLPIR本身为收费共享软件,对于科研和个人用户提供免费使用.
但是需要在 `NLPIR repo <https://github.com/NLPIR-team/NLPIR>`_ 中下载对应的license文件,这里
提供工具方法直接更新::

    from nlpir import tools
    tools.update_license()

=====================
Custom init config
=====================

本模块提供了一次性的对NLPIR各个模块的初始化方法,若不进行此操作,则直接使用默认配置进行初始化.

**note**: 初始化必须在调用各个模块函数之前进行,否则配置是不能生效的.而且初始化配置只能调用一次.

E.g::

    import nlpir
    data_path = "/home/nlpir/Data"
    lib_path = "/home/nlpir/lib"
    nlpir.init_setting(
        nlpir.ictclas,
        encode=nlpir.native.nlpir_base.BIG5_CODE,
        lib_path=lib_path,
        data_path=data_path
    )

上述初始化设置的代码,初始化设置了 :mod:`nlpir.ictclas` 模块的设置.这里每个模块的初始化设置都是分开的.
修改 :mod:`ictclas` 设置并不影响 :mod:`nlpir.new_words_finder` 的设置.

``data_path`` 是指定一个NLPIR的 ``Data`` 文件夹,默认为Module内部的 ``Data`` 文件夹,若指定别的
文件夹(可以先复制包的文件夹出来),则对其进行的各种设置和词表的修改不会影响本Module本身.且可以拷
贝此文件夹到其他机器,共享配置.

``lib_path`` 是指定一个NLPIR的调用DLL文件,可以用于需要制定外部DLL的情况,如使用Docker时保持DLL
库更新,可以使用Docker的volume设置DLL文件.


====================================
Chinese word segmentation (ICTCLAS)
====================================

基本分词功能
================

分词的基本功能是使用 :func:`nlpir.ictclas.segment` 进行的, 该函数提供对字符串进行分词,以及是否进行词性标注以及最终的后处理方式.
默认的后处理方式会返回一个列表,内容为单词和词性.若没有进行词性标注则直接返回单词的列表.

::

    from nlpir import ictclas
    test_str = "法国启蒙思想家孟德斯鸠曾说过：“一切有权力的人都容易滥用" \
               "权力，这是一条千古不变的经验。有权力的人直到把权力用到" \
               "极限方可休止。”另一法国启蒙思想家卢梭从社会契约论的观点" \
               "出发，认为国家权力是公民让渡其全部“自然权利”而获得的，" \
               "他在其名著《社会契约论》中写道：“任何国家权力无不是以民" \
               "众的权力（权利）让渡与公众认可作为前提的”。"

    for word, pos in ictclas.segment(test_str, pos_tagged=True):
        print(word, pos)

ICTCLAS的原始输出为字符串,譬如在进行Seq2Seq训练的语料的前处理上,需要的是分词后的字符串内容,得到列表得不偿失,这里可以修改后处理的回调
函数,使用lambda表达式直接获取字符串输出,也可以自己编写回调后处理函数直接接入训练的Pipline中.

获得字符串结果::

    segment(txt, pas_tagged, post_process=lambda t, _ : t)

其他配置
========

1. 标注集修改
-------------

默认使用的标注集为 :attr:`nlpir.native.ictclas.ICTCLAS.ICT_POS_MAP_SECOND` 计算所二级标注集,
若需要进行标注集修改,使用 :func:`nlpir.native.ictclas.ICTCLAS.set_pos_map` 进行修改

2. 词典使用
-----------

ICTCLAS支持两种词典添加方式,一种是直接持久化的添加方式保存为用户词典,程序关闭后再次调用的时候依然会导入此用户此件.
另一种为临时用户词典添加入内存中,程序关闭后消失.

添加词典
^^^^^^^^

使用 :func:`nlpir.ictclas.import_dict` 添加临时词典

::

    nlpir.ictclas.import_dict(["孟德斯鸠"])

默认添加词典词性为`n`,若增加词的词性为其他的时候,使用 ``nlpir.ictclas.import_dict(["孟德斯鸠 name"])`` 的
形式进行添加

词典删除
^^^^^^^^^^^^^

使用 :func:`nlpir.ictclas.clean_user_dict` 删除所有内存中的词, 仅想删除部分词时使用 :func:`delete_user_word`
此函数传入参数为想要删除的词的列表

词典保存
^^^^^^^^

内存中的词典可以保存在磁盘中,保存于Data文件夹下,在程序下次使用时直接使用,内存中的词典可以使用
:func:`nlpir.ictclas.save_user_dict` 保存在磁盘中, 也可以直接使用
:func:`nlpir.native.ictclas.ICTCLAS.import_user_dict` 添加文件形式的词典(不推荐)

持久化词典的删除
^^^^^^^^^^^^^^^^^^^^^^^

删除已经持久化的用户词典的方法为 :func:`clean_saved_user_dict` 此方法将会删除保存在Data文件夹下的用户词典,
但是此方法只能一次性删除所有,不能仅删除部分单词.所以,请谨慎使用.



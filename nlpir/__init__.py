# coding : utf-8
import os
import typing
import re
import logging
import sys
import functools
from .exception import NLPIRException

__version__ = "0.0.7.2"
PACKAGE_DIR = os.path.abspath(os.path.dirname(__file__))
logger = logging.getLogger("nlpir")


def clean_logs(data_path: typing.Optional[str] = None, include_current: bool = False):
    """
    Clean logs

    :param data_path: the cus
    :param include_current: include current directory or not
    """
    if data_path is None:
        data_path = os.path.join(PACKAGE_DIR, "Data")
    delete_list = [data_path]
    if include_current:
        delete_list.append(os.path.abspath("./"))
    delete_file_list = []
    for path in delete_list:
        for filename in os.listdir(path):
            if re.match(r'\d{8}\.log|err', filename):
                delete_file_list.append(os.path.abspath(os.path.join(path, filename)))
    logger.info("The following file will be deleted: \n\t{}".format("\n\t".join(delete_file_list)))
    for f in delete_file_list:
        try:
            os.remove(f)
        except OSError as e:
            logger.error(e)


def get_instance(func: callable) -> callable:
    """
    A wrapper to init instance when call the function

    直接使用单层装饰器时,此装饰器会在import module的时候直接被调用,
    生成对应的函数,导致对应的类实例过早初始化.
    为了让类实例真正在函数调用时才初始化,使用下面的 :func:`functions.warps`,
    此方法在直接import的时候不会被调用(因为初始化时仅仅为函数没有函数参数),故使用
    这种方式.

    让函数在真正执行时才进行类实例初始化的原因是为了使 :func:`init_setting` 可以被使用,
    类似于 :func:logging.basicConfig 方法,可以在import对应module后可以有一次修改初始化
    参数的可能.

    """

    @functools.wraps(func)
    def wraps(*args, **kwargs):
        """

        """
        module = sys.modules[func.__module__]
        module = init_setting(module) if module.__instance__ is None else module
        module.__instance__ = module.__cls__(
            encode=module.__nlpir_encode__,
            lib_path=module.__lib__,
            data_path=module.__data__,
            license_code=module.__license_code__
        ) if module.__instance__ is None else module.__instance__
        return func(*args, **kwargs)

    return wraps


def init_setting(
        init_module,
        encode: typing.Optional[int] = None,
        lib_path: typing.Optional[int] = None,
        data_path: typing.Optional[str] = None,
        license_code: str = ''
):
    """
    Init the NLPIR module for custom usage.

    **Only can init it , before call any process function in that module**


    :param ModuleType init_module: The high-level module want to use
    :param int encode: same as in :class:`nlpir.native.nlpir_base.NLPIRBase()`
    :param str lib_path: same as in :class:`nlpir.native.nlpir_base.NLPIRBase()`
    :param str data_path: same as in :class:`nlpir.native.nlpir_base.NLPIRBase()`
    :param str license_code: same as in :class:`nlpir.native.nlpir_base.NLPIRBase()`
    :raise: NLPIRException
    :return: init module
    """
    if init_module.__instance__ is not None:
        raise NLPIRException("Already have a instance can not change the setting")
    init_module.__nlpir_encode__ = encode if encode is not None else init_module.__nlpir_encode__
    init_module.__lib__ = lib_path if lib_path is not None else init_module.__lib__
    init_module.__data__ = data_path if data_path is not None else init_module.__data__
    init_module.__license_code__ = license_code if license_code is not None else init_module.__license_code__
    init_module.__cls__(
        encode=init_module.__nlpir_encode__,
        lib_path=init_module.__lib__,
        data_path=init_module.__data__,
        license_code=init_module.__license_code__
    )
    return init_module


def import_dict(word_list: list, instance) -> list:
    """
    Temporary add word as dictionary, will loss it when restart the Program.
    Can use :func:`save_user_dict` to make persistence, :func:`clean_user_dict` to
    delete all temporary words or :func:`delete_user_word` to delete part of them.

    The persistent dict cannot be clean by using method above. :func:`clean_saved_user_dict`
    will be used in this situation. But it will delete all user dict include saved dict in the past.

    Every word in `word_list` can be a single word and the POS will be `n`. The custom POS can be added
    as `word pos` in `word_list`.

    :param instance: instance to execute the function
    :param word_list: list of words want to add to NLPIR
    :return: the word fail to add to the NLPIR
    """
    if not hasattr(instance, "add_user_word"):
        raise NLPIRException("This instance not support this method")
    fail_list = list()
    for word in word_list:
        if 0 != instance.add_user_word(word):
            fail_list.append(word_list)
    return fail_list


def clean_user_dict(instance) -> bool:
    """
    Clean all temporary dictionary, more information shows in :func:`import_dict`

    :param instance: instance to execute the function
    :return: success or not
    """
    if not hasattr(instance, "clean_user_word"):
        raise NLPIRException("This instance not support this method")
    return instance.clean_user_word() == 0


def delete_user_word(word_list: list, instance):
    """
    Delete words in temporary dictionary, more information shows in :func:`import_dict`

    :param instance: instance to execute the function
    :param word_list: list of words want to delete
    """
    if not hasattr(instance, "del_usr_word"):
        raise NLPIRException("This instance not support this method")
    for word in word_list:
        instance.del_usr_word(word)


def save_user_dict(instance) -> bool:
    """
    Save temporary dictionary to Data, more information shows in :func:`import_dict`

    :param instance: instance to execute the function
    :return: Success or not
    """
    if not hasattr(instance, "save_the_usr_dic"):
        raise NLPIRException("This instance not support this method")
    return 1 == instance.save_the_usr_dic()


def clean_saved_user_dict():
    """
    Delete user dict from disk, which is :

    1. ``Data/FieldDict.pdat``
    2. ``Data/FieldDict.pos``
    3. ``Data/FieldDict.wordlist``
    4. ``Data/UserDefinedDict.lst``

    :return: Delete success or not
    """
    try:
        # for ictclas
        with open(os.path.join(PACKAGE_DIR, "Data/FieldDict.pdat"), 'w') as f:
            f.write("")
        with open(os.path.join(PACKAGE_DIR, "Data/FieldDict.pos"), 'w') as f:
            f.write("")
        with open(os.path.join(PACKAGE_DIR, "Data/FieldDict.wordlist"), 'w') as f:
            f.write("")
        with open(os.path.join(PACKAGE_DIR, "Data/UserDefinedDict.lst"), 'w') as f:
            f.write("")
        # for key_extract
        with open(os.path.join(PACKAGE_DIR, "Data/UserDict.pdat"), 'w') as f:
            f.write("")
        return True
    except OSError:
        return False


# noinspection PyTypeChecker
def import_blacklist(instance, filename: str, pos_blacklist=typing.List[str]) -> bool:
    """
    Import Blacklist to system

    This function will permanently import blacklist words to system not to the memory .
    If you want to delete the blacklist words, you should run :func:`clean_blacklist` to delete
    blacklist form system .

    此函数将会把词永久性保存在NLPIR中,和保存用户词典类似.这里删除使用的是 :func:`clean_blacklist` .

    停用词表,Format of stop word::
        word1 n1
        word2 n2
        word3 n3

    若 `pos_blacklist` 为: ``['n1', 'n2']`` 则 `word1`, `word2` 将会进入屏蔽列表

    If `pos_blacklist` : ``['n1', 'n2']`` Then `word1`, `word2` will be in the blacklist

    :param instance: instance to execute the function
    :param filename: A word list that the words want to import to the blacklist (stop word list),
        一个停用词词表,里面为想进行屏蔽的词,也可以包括别的词,是否不进行抽取是按照词表中的词性来确定的.
    :param pos_blacklist: A list of pos that want to block in the system, 想要屏蔽的词的词性
    :return: 是否成功导入
    """
    if not hasattr(instance, "import_key_blacklist"):
        raise NLPIRException("This instance not support this method")
    try:
        os.rename(
            os.path.join(PACKAGE_DIR, "Data/KeyBlackList.pdat"),
            os.path.join(PACKAGE_DIR, "Data/KeyBlackList.pdat.bak")
        )
    except OSError:
        pass
    return_result = instance.import_key_blacklist(
        filename=filename,
        pos_blacklist="#".join(pos_blacklist)
    )
    if return_result > 0:
        return True
    else:
        clean_blacklist()
        return False


def __rename__(src, dst):
    if os.path.isfile(dst):
        os.remove(dst)
    os.rename(src, dst)


def clean_blacklist() -> bool:
    """
    清除黑名单词表, 会将对应的文件进行重命名, 之后可以通过 :func:`recover_blacklist`
    进行恢复,但仅可以进行一次,若重复调用本函数则恢复函数不起作用

    :return: clean success or not
    """
    black_dir = os.path.join(PACKAGE_DIR, "Data/KeyBlackList.pdat")
    black_dir_bak = os.path.join(PACKAGE_DIR, "Data/KeyBlackList.pdat.bak")
    try:
        __rename__(black_dir, black_dir_bak)
        return True
    except OSError:
        return False


def recover_blacklist() -> bool:
    """
    恢复黑名单词表,仅在被重命名的词表存在时才起作用

    :return:
    """
    black_dir = os.path.join(PACKAGE_DIR, "Data/KeyBlackList.pdat")
    black_dir_bak = os.path.join(PACKAGE_DIR, "Data/KeyBlackList.pdat.bak")
    try:
        __rename__(black_dir_bak, black_dir)
        return True
    except OSError:
        return False

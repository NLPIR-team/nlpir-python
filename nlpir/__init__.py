# coding : utf-8
import os
import typing
import re
import logging
import sys
import functools
from .exception import NLPIRException

__version__ = "0.0.1"
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
    return init_module

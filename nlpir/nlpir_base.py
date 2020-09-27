# coding=utf-8
"""Provides a low-level Python interface to NLPIR.

Most of code in this model is copy/inspired from pynlpir
"""
import os
import logging
import sys
import ctypes
import typing

from ctypes import (c_bool, c_char, c_char_p, c_double, c_int, c_uint,
                    c_ulong, c_void_p, cdll, POINTER, Structure)
from nlpir import PACKAGE_DIR

logger = logging.getLogger('nlpir.api')


class NLPIRBase:
    LIB_DIR = os.path.join(PACKAGE_DIR, 'lib')
    # 如果是各种编码混合，设置为-1，系统自动检测，并内部转换。会多耗费时间，不推荐使用
    UNKNOWN_CODE = -1
    # 默认支持GBK编码
    GBK_CODE = 0
    # UTF8编码
    UTF8_CODE = 1
    # BIG5编码
    BIG5_CODE = 2
    # GBK编码，里面包含繁体字
    GBK_FANTI_CODE = 3
    # UTF8编码
    UTF8_FANTI_CODE = 4

    def __init__(self):
        self.lib_nlpir = self.load_library(sys.platform)
        # TODO give the statue, remove the hard code
        self.init_lib("nlpir".encode("utf-8"), self.UTF8_CODE, "")

    def __del__(self):
        # TODO if not exit properly
        self.exit_lib()

    @property
    def dll_name(self):
        raise NotImplementedError

    def init_lib(self, data_path: bytes, encode: int, license_code: bytes) -> bool:
        """
        所有子类都需要实现此方法用于类初始化实例时调用, 由于各个库对应初始化不同,故改变此函数名称
        /*********************************************************************
         *
         *  Func Name  : Init
         *
         *  Description: Init NLPIR
         *               The function must be invoked before any operation listed as following
         *
         *  Parameters : const char * sInitDirPath=NULL
         *				 sDataPath:  Path where Data directory stored.
         *				 the default value is NULL, it indicates the initial directory is current working directory path
         *				 encode: encoding code;
         *				 sLicenseCode: license code for unlimited usage. common user ignore it
         *  Returns    : success or fail
         *  Author     : Kevin Zhang
         *  History    :
         *              1.create 2013-6-8
         *********************************************************************/
        """
        return self.get_func('NLPIR_Init', [c_char_p, c_int, c_char_p], c_bool)(data_path, encode, license_code)

    def exit_lib(self) -> bool:
        """
        所有子类都需要实现此方法用于类析构(销毁)实例时调用, 由于各个库对应初始化不同,故改变此函数名称
        /*********************************************************************
         *
         *  Func Name  : NLPIR_Exit
         *
         *  Description: Exist NLPIR and free related buffer
         *               Exit the program and free memory
         *				 The function must be invoked while you needn't any lexical anlysis
         *
         *  Parameters : None
         *
         *  Returns    : success or fail
         *  Author     : Kevin Zhang
         *  History    :
         *              1.create 2002-8-6
         *********************************************************************/"""
        return self.get_func('NLPIR_Exit', restype=c_bool)()

    def get_dll_path(self, platform, lib_dir, is_64bit):

        def get_dll_prefix(prefix, suffix):
            return os.path.join(lib_dir, prefix + self.dll_name + suffix)

        if platform.startswith('win') and is_64bit:
            lib = get_dll_prefix("", "64")
        elif platform.startswith('win'):
            lib = get_dll_prefix("", "32")
        elif platform.startswith('linux') and is_64bit:
            lib = get_dll_prefix("lib", "64.so")
        elif platform.startswith('linux'):
            lib = get_dll_prefix("lib", "32.so")
        elif platform == 'darwin':
            lib = get_dll_prefix("lib", "darwin.so")
            # lib = get_dll_prefix("lib", ".dylib")
        else:
            raise RuntimeError("Platform '{}' is not supported.".format(
                platform))
        logger.debug("Using {} file for {}".format(lib, platform))
        return lib

    def load_library(self, platform, is_64bit=None, lib_dir=LIB_DIR) -> ctypes.CDLL:
        """Loads the NLPIR library appropriate for the user's system.
        This function is called automatically when create a instance.
        :param str platform: The platform identifier for the user's system.
        :param bool is_64bit: Whether or not the user's system is 64-bit.
        :param str lib_dir: The directory that contains the library files
            (defaults to :data:`LIB_DIR`).
        :return: a dynamic lib object

        :raises RuntimeError: The user's platform is not supported by NLPIR.
        """
        logger.debug("Loading NLPIR library file from '{}'".format(lib_dir))
        if is_64bit is None:
            is_64bit = sys.maxsize > 2 ** 32
        lib = self.get_dll_path(platform, lib_dir, is_64bit)
        lib_nlpir = ctypes.cdll.LoadLibrary(lib)
        logger.debug("{} library file '{}' loaded.".format(self.dll_name, lib))
        return lib_nlpir

    def get_func(self, name, argtypes=None, restype: typing.Any = c_int):
        """Retrieves the corresponding NLPIR function.
        :param str name: The name of the NLPIR function to get.
        :param list argtypes: A list of :mod:`ctypes` data types that correspond
            to the function's argument types.
        :param restype: A :mod:`ctypes` data type that corresponds to the
            function's return type (only needed if the return type isn't
            :class:`ctypes.c_int`).
        :returns: The exported function. It can be called like any other Python
            callable.
        """
        logger.debug("Getting NLPIR API function: 'name': '{}', 'argtypes': '{}',"
                     " 'restype': '{}'.".format(name, argtypes, restype))
        func = getattr(self.lib_nlpir, name)
        if argtypes is not None:
            func.arg_types = argtypes
        if restype is not c_int:
            func.restype = restype
        logger.debug("NLPIR API function '{}' retrieved.".format(name))
        return func


class LicenseError(Exception):
    """A custom exception for missing/invalid license errors."""
    pass

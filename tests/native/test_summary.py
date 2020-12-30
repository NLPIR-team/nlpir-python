# coding=utf-8
"""
Tested Function:

- :func:`nlpir.native.summary.Summary.exit_lib`
- :func:`nlpir.native.summary.Summary.get_last_error_msg`
- :func:`nlpir.native.summary.Summary.single_doc`
- :func:`nlpir.native.summary.Summary.single_doc_e`
- :func:`nlpir.native.summary.Summary.file_process`
- :func:`nlpir.native.summary.Summary.get_last_error_msg`

"""
from nlpir.native import Summary
from nlpir import native, clean_logs
from ..strings import test_str, test_source_filename
import pytest


def get_summary(encode=native.UTF8_CODE):
    return Summary(encode=encode)


@pytest.mark.run(order=-1)
def test_init_exit():
    summary = get_summary()
    summary.exit_lib()
    clean_logs(include_current=True)


def test_summary_string():
    summary = get_summary()
    assert summary.single_doc(text=test_str, sum_rate=0.3, sum_len=50, html_tag_remove=True)
    assert summary.single_doc_e(text=test_str, sum_rate=0.3, sum_len=50, html_tag_remove=True)


def test_summary_file():
    summary = get_summary()
    assert summary.file_process(text_filename=test_source_filename, sum_rate=0.1, sum_len=300, html_tag_remove=True)


def test_get_last_error_msg():
    summary = get_summary()
    msg = summary.get_last_error_msg()
    assert msg is not None
    clean_logs(include_current=True)

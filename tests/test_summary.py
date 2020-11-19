from nlpir import summary


def test_summarization():
    from tests.strings import test_str
    summary.summarization(content=test_str, sum_rate=0.3, sum_len=50, html_tag_remove=True)

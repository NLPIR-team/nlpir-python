import pytest

from nlpir import eye_checker


@pytest.mark.run(order=0)
def test_extract():
    from tests.strings import test_kgb_test_text, test_kgb_rules
    assert eye_checker.import_kgb_rules(rule_text=test_kgb_rules, report_type=1, overwrite=True)
    assert eye_checker.extract_knowledge(report_text=test_kgb_test_text, report_type=1)
    assert eye_checker.extract_knowledge(report_text="", report_type=1)
    # will get Segmentation fault
    # assert eye_checker.extract_knowledge(report_text="", report_type=999)


@pytest.mark.run(order=1)
def test_rule_manage():
    from tests.strings import test_kgb_test_text, test_kgb_rules
    rule_set = {1, 2, 3, 4, 6, 7, 9}
    for rule in rule_set:
        assert eye_checker.import_kgb_rules(rule_text=test_kgb_rules, report_type=rule, overwrite=True)
    assert rule_set.issubset(eye_checker.list_rules())

    for rule in eye_checker.list_rules():
        eye_checker.delete_rules(rule)

    assert len(eye_checker.list_rules()) == 0

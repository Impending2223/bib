"""A Chinese name written without characters, family name first (sources/name-order.yaml; the owner, Nov. 25, 2026)."""
from tools.bib import works


def test_a_listed_chinese_name_is_read_as_written():
    own, sur, given, _, _ = works.name_parts("Chen Jian")
    assert own and sur == "Chen Jian" and not given
    assert works.name_parts("Qiang Zhai")[1] == "Zhai"            # written given name first: as other names
    assert works.name_parts("Gordon H. Chang")[1] == "Chang"


def test_check_asks_about_a_name_in_neither_list():
    assert works.name_order_doubt("Chen Newname")
    assert not works.name_order_doubt("Chen Jian")                # own
    assert not works.name_order_doubt("Shu Guang Zhang")          # western
    assert not works.name_order_doubt("Michael R. Beschloss")
    assert not works.name_order_doubt("Yang Jisheng 杨继绳")       # characters tell it already

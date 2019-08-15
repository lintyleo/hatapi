import pytest

from base.helper import parse_digit

_param_dict_list = [
    {
        "input_param": "1",
        "expected": 1
    }, {
        "input_param": "1.1",
        "expected": 1.1
    }, {
        "input_param": "-1.1",
        "expected": -1.1
    }, {
        "input_param": "-1.10",
        "expected": -1.1
    }, {
        "input_param": "0",
        "expected": 0.0
    }
]

_param_invalid_list = ["a123", "-123a", "123a"]


@pytest.mark.parametrize("dt", _param_dict_list)
def test_parse_digit(dt):
    """
    单元测试： parse digit
    :type dt: dict
    :return:
    """
    expected = dt["expected"]
    actual = parse_digit(dt["input_param"])
    assert expected == actual, \
        "test_parse_digit 失败, input： %r, expected: %r, actual: %r" % (dt["input_param"], expected, actual)


@pytest.mark.parametrize("el", _param_invalid_list)
def test_parse_digit_invalid(el):
    """
    单元测试： parse digit 非法输入
    :param el:
    :return:
    """
    actual = parse_digit(el)
    assert el == actual, \
        "test_parse_digit_invalid 失败, input： %r, expected: %r, actual: %r" % (el, el, actual)

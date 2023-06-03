import pytest

from promptgen.dataclass import DataClass, DictLike


@pytest.fixture
def dataclass() -> DataClass:
    class TmpDataClass(DataClass):
        test_input_parameter_name: str
        test_input_parameter_name_2: str

    return TmpDataClass(
        test_input_parameter_name='test input parameter value',
        test_input_parameter_name_2='test input parameter value 2'
    )


def test_dict_like_from_dict():
    assert DictLike.from_dict({
        'test_input_parameter_name': 'test input parameter value',
        'test_input_parameter_name_2': 'test input parameter value 2'
    }) == DictLike(
        test_input_parameter_name='test input parameter value',
        test_input_parameter_name_2='test input parameter value 2'
    )



def test_dict_like_from_dataclass(dataclass: DataClass):
    assert DictLike.from_dataclass(dataclass) == DictLike(
        test_input_parameter_name='test input parameter value',
        test_input_parameter_name_2='test input parameter value 2'
    )

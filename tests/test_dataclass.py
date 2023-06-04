from pydantic import BaseModel
import pytest

from promptgen.dataclass import DictLike



@pytest.fixture
def dataclass() -> BaseModel:
    class TmpBaseModel(BaseModel):
        test_input_parameter_name: str
        test_input_parameter_name_2: str

    return TmpBaseModel(
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



def test_dict_like_from_BaseModel(dataclass: BaseModel):
    assert DictLike.from_dataclass(dataclass) == DictLike(
        test_input_parameter_name='test input parameter value',
        test_input_parameter_name_2='test input parameter value 2'
    )

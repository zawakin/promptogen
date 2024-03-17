import pytest
from promptogen.model.dataclass import DataClass


class TmpDataClass(DataClass):
    name: str
    description: str


@pytest.fixture
def dataclass() -> DataClass:
    return TmpDataClass(
        name="test name",
        description="test description",
    )


def test_dataclass_to_dict(dataclass: DataClass):
    assert dataclass.to_dict() == {
        "name": "test name",
        "description": "test description",
    }


def test_dataclass_copy(dataclass: DataClass):
    assert dataclass.copy_me() == dataclass


def test_dataclass_update(dataclass: DataClass):
    assert dataclass.update(name="new name") == TmpDataClass(
        name="new name",
        description="test description",
    )


def test_dataclass_update_invalid_key(dataclass: DataClass):
    with pytest.raises(ValueError):
        dataclass.update(invalid_key="invalid value")


def test_dataclass_from_dict():
    assert TmpDataClass.from_dict({
        "name": "test name",
        "description": "test description",
    }) == TmpDataClass(
        name="test name",
        description="test description",
    )


def test_dataclass_from_json_string():
    assert TmpDataClass.from_json_string('{"name": "test name", "description": "test description"}') == TmpDataClass(
        name="test name",
        description="test description",
    )

"""Test that we can create basic pydantic models using units of measurement."""

import pytest
from stuom.duration import Seconds

try:
    from pydantic import BaseModel  # type: ignore

except (ImportError, ModuleNotFoundError):
    pytest.skip(allow_module_level=True)


def test_duration_fields_work_in_pydantic_models():
    """This ensures that one can construct pydantic `BaseModel`s with the `Duration` units of
    measurement.
    """

    class TestModel(BaseModel):
        duration: Seconds

    TestModel(duration=Seconds(2))

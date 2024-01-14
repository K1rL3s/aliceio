import contextvars

import pytest

from aliceio.utils.mixins import ContextInstanceMixin, DataMixin


class ContextObject(ContextInstanceMixin["ContextObject"]):
    pass


class DataObject(DataMixin):
    pass


class TestDataMixin:
    def test_store_value(self):
        obj = DataObject()
        obj["foo"] = 42

        assert "foo" in obj
        assert obj["foo"] == 42
        assert len(obj.data) == 1

    def test_remove_value(self):
        obj = DataObject()
        obj["foo"] = 42
        del obj["foo"]

        assert "key" not in obj
        assert len(obj.data) == 0

    def test_getter(self):
        obj = DataObject()
        obj["foo"] = 42

        assert obj.get("foo") == 42
        assert obj.get("bar") is None
        assert obj.get("baz", "test") == "test"


class TestContextInstanceMixin:
    def test_empty(self):
        obj = ContextObject()

        assert obj.get_current(no_error=True) is None
        with pytest.raises(LookupError):
            assert obj.get_current(no_error=False)

    def test_set_current_valid_input(self):
        obj = ContextObject()
        value = ContextObject()

        token = obj.set_current(value)

        assert obj.get_current() == value
        assert isinstance(token, contextvars.Token)

    def test_set_current_multiple_times(self):
        obj = ContextObject()
        value1 = ContextObject()
        value2 = ContextObject()

        token1 = obj.set_current(value1)
        token2 = obj.set_current(value2)

        assert obj.get_current() == value2
        assert isinstance(token1, contextvars.Token)
        assert isinstance(token2, contextvars.Token)

    def test_set_current_returns_token(self):
        obj = ContextObject()
        value = ContextObject()

        token = obj.set_current(value)

        assert isinstance(token, contextvars.Token)

    def test_set_wrong_type(self):
        obj = ContextObject()

        with pytest.raises(
            TypeError,
            match=r"Value should be instance of 'ContextObject' not '.+'",
        ):
            obj.set_current(42)

    def test_reset_current_valid_token(self):
        class MyClass(ContextInstanceMixin):
            pass

        instance = MyClass()
        token = MyClass.set_current(instance)

        MyClass.reset_current(token)

        assert MyClass.get_current() is None

    def test_reset_current_wrong_type_error(self):
        class MyClass(ContextInstanceMixin):
            pass

        instance = MyClass()
        MyClass.set_current(instance)

        wrong_type_token = "wrong_type"

        with pytest.raises(TypeError):
            MyClass.reset_current(wrong_type_token)

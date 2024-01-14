from aliceio.exceptions import AliceAPIError, ClientDecodeError, DetailedAliceioError
from aliceio.methods import Status


class TestDetailedAliceioError:
    def test_message_no_url(self):
        error = DetailedAliceioError("test")
        assert error.message == "test"

        assert error.url is None
        assert str(error) == "test"
        assert repr(error) == "DetailedAliceioError('test')"

    def test_message_and_url(self):
        error = DetailedAliceioError("test")
        error.url = "http://example.com"

        assert error.message == "test"
        assert error.url == "http://example.com"
        assert str(error) == "test\n(background on this error at: http://example.com)"
        assert (
            repr(error) == "DetailedAliceioError('test\n"
            "(background on this error at: http://example.com)')"
        )


class TestAliceAPIError:
    def test_init(self):
        method = Status()
        message = "test"
        error = AliceAPIError(method, message)

        assert error.message == message
        assert error.method == method
        assert str(error) == f"Alice's server says - {message}"


class TestClientDecodeError:
    def test_instance_creation_with_attributes(self):
        message = "test"
        original = ValueError("test original")
        data = {"key": "value"}

        error = ClientDecodeError(message, original, data)

        expected_str = (
            f"{message}\n"
            f"Caused from error: "
            f"{type(original).__module__}.{type(original).__name__}: {original}\n"
            f"Content: {data}"
        )

        assert error.message == message
        assert error.original == original
        assert error.data == data
        assert str(error) == expected_str

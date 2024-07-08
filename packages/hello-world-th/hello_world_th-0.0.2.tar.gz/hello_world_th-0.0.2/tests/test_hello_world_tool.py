import pytest
import unittest

from promptflow.connections import CustomConnection
from hello_world.tools.hello_world_tool import get_greeting_messagename


@pytest.fixture
def my_custom_connection() -> CustomConnection:
    my_custom_connection = CustomConnection(
        {
            "api-key" : "my-api-key",
            "api-secret" : "my-api-secret",
            "api-url" : "my-api-url"
        }
    )
    return my_custom_connection


class TestTool:
    def test_get_greeting_messagename(self, my_custom_connection):
        result = get_greeting_messagename(my_custom_connection, input_text="Microsoft")
        assert result == "Hello Microsoft"


# Run the unit tests
if __name__ == "__main__":
    unittest.main()
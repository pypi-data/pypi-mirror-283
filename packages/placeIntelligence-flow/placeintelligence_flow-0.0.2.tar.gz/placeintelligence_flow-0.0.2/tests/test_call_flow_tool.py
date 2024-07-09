import pytest
import unittest

from promptflow.connections import CustomConnection
from call_flow.tools.call_flow_tool import allowSelfSignedHttps
from call_flow.tools.call_flow_tool import get_place_intelligence_flow_api


@pytest.fixture
def my_custom_connection() -> CustomConnection:
    my_custom_connection = CustomConnection(
        {
            "api-key": "my-api-key",
            "api-secret": "my-api-secret",
            "api-url": "my-api-url",
        }
    )
    return my_custom_connection


class TestTool:
    def test_allowSelfSignedHttps(self):
        result = allowSelfSignedHttps(allowed=True)
        assert result

    def test_get_place_intelligence_flow_api(self):
        result = get_place_intelligence_flow_api(
            chat_input={"message": "양양에 있는 매장 추천해줘", "image": ""}
        )
        assert result


# Run the unit tests
if __name__ == "__main__":
    unittest.main()

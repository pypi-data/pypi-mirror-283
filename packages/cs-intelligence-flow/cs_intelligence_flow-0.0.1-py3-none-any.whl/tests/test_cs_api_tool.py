import pytest
import unittest

from promptflow.connections import CustomConnection
from cs.tools.cs_api_tool import get_cs_intelligence_flow_api


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
    def test_get_cs_intelligence_flow_api(self):
        result = get_cs_intelligence_flow_api(
            allowed=True,
            chat_input={"message": "갤럭시 S23 액정 수리비 알려줘", "image": ""},
            end_point="https://cs-intelligence-endpoint.eastus.inference.ml.azure.com/score",
            api_key="85q3uwkhCU7hMGmHZms7b1iQ3cG16Jto",
            deployment_name="cs-intelligence-endpoint-10",
        )
        assert result


# Run the unit tests
if __name__ == "__main__":
    unittest.main()

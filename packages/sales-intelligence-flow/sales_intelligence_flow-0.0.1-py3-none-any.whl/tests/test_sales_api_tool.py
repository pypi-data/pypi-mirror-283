import pytest
import unittest

from promptflow.connections import CustomConnection
from sales.tools.sales_api_tool import get_sales_intelligence_flow_api


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
    def test_get_sales_intelligence_flow_api(self):
        result = get_sales_intelligence_flow_api(
            allowed=True,
            chat_input={"message": "갤럭시 S23 판매가 알려줘", "image": ""},
            end_point="https://sales-intelligence-endpoint.eastus.inference.ml.azure.com/score",
            api_key="6hD80yxsmIx2fCXvY5qqmLqbCZZ052Cx",
            deployment_name="sales-intelligence-endpoint-7",
        )
        assert result


# Run the unit tests
if __name__ == "__main__":
    unittest.main()

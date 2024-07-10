import pytest
import unittest

from promptflow.connections import CustomConnection
from product.tools.product_api_tool import get_product_intelligence_flow_api


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
    def test_get_product_intelligence_flow_api(self):
        result = get_product_intelligence_flow_api(
            allowed=True,
            chat_input={"message": "갤럭시 S23 초기 구매 혜택 알려줘", "image": ""},
            end_point="https://product-intelligence-endpoint.eastus.inference.ml.azure.com/score",
            api_key="IbcBa3u51njEHgEsP0KbN6f3MzUz34At",
            deployment_name="product-intelligence-endpoint-5",
        )
        assert result


# Run the unit tests
if __name__ == "__main__":
    unittest.main()

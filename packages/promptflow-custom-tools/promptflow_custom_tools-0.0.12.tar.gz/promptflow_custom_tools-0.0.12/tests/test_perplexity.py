import pytest
import unittest
from unittest.mock import patch
from promptflow.connections import CustomConnection
from promptflow_custom_tools.tools.perplexity import query_perplexity

@pytest.fixture
def my_custom_connection() -> CustomConnection:
    return CustomConnection(
        {
            "api_key": "API_KEY",
            "api_base": "https://api.perplexity.ai"
        }
    )

class TestTool(unittest.TestCase):

    @patch('requests.post')
    def test_query_perplexity(self, mock_post):
        mock_response = {
            'choices': [
                {'message': {'content': 'The weather in New York today is sunny.'}}
            ]
        }
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response

        # Use the fixture to get the connection object
        my_custom_connection = CustomConnection(
            {
                "api_key": "API_KEY",
                "api_base": "https://api.perplexity.ai"
            }
        )

        prompt_template = {
            "template": """
{
    "system_content": "{{ system_content }}",
    "user_content": "{{ user_content }}"
}
"""
        }
        result = query_perplexity(
            connection=my_custom_connection,
            prompt_template=prompt_template,
            model="llama-3-sonar-large-32k-online",
            temperature=1.0,
            max_tokens=4096,
            user_content="How many stars are there in our galaxy?",
            system_content="Be precise and concise."
        )
        self.assertEqual(result, 'The weather in New York today is sunny.')

# Run the unit tests
if __name__ == "__main__":
    unittest.main()

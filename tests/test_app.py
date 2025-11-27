import pytest
from unittest.mock import patch, Mock
from app import app

class TestApp:
    def test_home(self):
        with app.test_client() as client:
            response = client.get('/')
            assert response.status_code == 200
            assert b"Hello, AI Flask App" in response.data

    def test_generate_success(self):
        mock_response = Mock()
        mock_choice = Mock()
        mock_choice.text = "Generated text"
        mock_response.choices = [mock_choice]

        with patch('openai.Completion.create', return_value=mock_response):
            with app.test_client() as client:
                response = client.post('/generate', json={'prompt': 'Test prompt'})
                assert response.status_code == 200
                data = response.get_json()
                assert 'response' in data
                assert data['response'] == "Generated text"

    def test_generate_no_prompt(self):
        with app.test_client() as client:
            response = client.post('/generate', json={})
            assert response.status_code == 400
            data = response.get_json()
            assert 'error' in data
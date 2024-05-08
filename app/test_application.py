from fastapi.testclient import TestClient
import hashlib
import pytest
import json

from .application import fastapi_app


class TestAPP:
    @pytest.fixture
    def test_client(self):
        client = TestClient(fastapi_app)
        yield client

    def test_healthcheck_no_input(self, test_client):
        response = test_client.get("/healthcheck")
        assert response.status_code == 200
        assert response._content == b""

    def test_healthcheck_with_input(self, test_client):
        response = test_client.get("/healthcheck?inp=abc&out=adad")
        assert response.status_code == 200
        assert response._content == b""

    def test_hash_no_input(self, test_client):
        response = test_client.post("/hash", content="{}")
        assert response.status_code == 400
        assert "validation_errors" in response.json()

    def test_hash_wrong_input(self, test_client):
        response = test_client.post(
            "/hash", content=json.dumps({"nice": "cool", "not_nice": "not_cool"})
        )
        assert response.status_code == 400
        assert "validation_errors" in response.json()

    def test_hash_wrong_input_format(self, test_client):
        response = test_client.post(
            "/hash", content=json.dumps({"string": 123, "not_nice": "not_cool"})
        )
        assert response.status_code == 400
        assert "validation_errors" in response.json()

    def test_hash_right_input_format(self, test_client):
        response = test_client.post(
            "/hash", content=json.dumps({"string": "to_hash", "not_nice": "not_cool"})
        )

        response_data = response.json()
        assert response.status_code == 200
        assert "hash_string" in response_data
        assert (
            response_data["hash_string"]
            == hashlib.sha256("to_hash".encode("UTF-8")).hexdigest()
        )

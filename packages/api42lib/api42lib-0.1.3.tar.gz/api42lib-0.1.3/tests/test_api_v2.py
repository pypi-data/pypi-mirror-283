from datetime import datetime, timedelta, timezone

import pytest
from api42lib import IntraAPIClient


@pytest.fixture
def ic():
    client = IntraAPIClient()
    client.progress_bar_disable()
    return client


def test_v2_url_1(ic):
    response = ic.get("https://api.intra.42.fr/v2/users/dstud")
    assert response.status_code == 200
    assert "id" in response.json()


def test_v2_url_2(ic):
    response = ic.get("/v2/users/dstud")
    assert response.status_code == 200
    assert "id" in response.json()


def test_v2_url_3(ic):
    response = ic.get("v2/users/dstud")
    assert response.status_code == 200
    assert "id" in response.json()


def test_v2_url_4(ic):
    response = ic.get("users/dstud")
    assert response.status_code == 200
    assert "id" in response.json()


def test_v2_url_5(ic):
    response = ic.get("    users/dstud    ")
    assert response.status_code == 200
    assert "id" in response.json()


def test_invalid_token_v2(ic):
    ic.token_v2.access_token = "21314"
    response = ic.get("https://api.intra.42.fr/v2/users/dstud")
    assert response.status_code == 200


def test_expired_token_v2(ic):
    ic.token_v2.expires_at = datetime.now(timezone.utc) - timedelta(seconds=5000)
    response = ic.get("https://api.intra.42.fr/v2/users/dstud")
    assert response.status_code == 200


def test_pages_v2(ic):
    params = {"filter[pool_month]": "october"}
    response = ic.pages("https://api.intra.42.fr/v2/campus/berlin/users", params=params)
    assert isinstance(response, list) and len(response) > 0


def test_pages_threaded_v2(ic):
    params = {"filter[pool_month]": "october"}
    response = ic.pages("https://api.intra.42.fr/v2/campus/berlin/users", params=params)
    assert isinstance(response, list) and len(response) > 0

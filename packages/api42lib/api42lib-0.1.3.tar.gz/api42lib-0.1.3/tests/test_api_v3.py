from datetime import datetime, timedelta, timezone

import pytest
from api42lib import IntraAPIClient


@pytest.fixture
def ic():
    client = IntraAPIClient()
    client.progress_bar_disable()
    return client


def test_v3_url_1(ic):
    response = ic.get("/v3/freeze/v2/freezes").json()
    assert "items" in response


def test_v3_url_2(ic):
    response = ic.get("v3/freeze/v2/freezes").json()
    assert "items" in response


def test_v3_url_3(ic):
    response = ic.get("freeze/v2/freezes").json()
    assert "items" in response


def test_v3_url_4(ic):
    response = ic.get("https://freeze.42.fr/api/v2/freezes").json()
    assert "items" in response


def test_v3_url_5(ic):
    response = ic.get("   freeze/v2/freezes   ").json()
    assert "items" in response


def test_invalid_token_v3(ic):
    ic.token_v3.access_token = "21314"
    response = ic.get("/v3/freeze/v2/freezes")
    assert response.status_code == 200


def test_expired_token_v3(ic):
    ic.token_v3.expires_at = datetime.now(timezone.utc) - timedelta(seconds=5000)
    response = ic.get("/v3/freeze/v2/freezes")
    assert response.status_code == 200


def test_pages_v3(ic):
    response = ic.pages("/v3/freeze/v2/freezes")
    assert isinstance(response, list) and len(response) > 0


def test_pages_threaded_v3(ic):
    response = ic.pages_threaded("/v3/freeze/v2/freezes")
    assert isinstance(response, list) and len(response) > 0

import pytest
from fastapi import FastAPI
from pytest_mock import MockerFixture
from fastapi.testclient import TestClient

from app.models import OAuthProvider
from app.routes import Routes


TEST_REDIRECT_URI = "https://example.com/oauth"

@pytest.fixture
def mock_oauth(mocker: MockerFixture) -> OAuthProvider:
  mock = mocker.MagicMock(spec=OAuthProvider)

  mock.get_redirect_url.return_value = TEST_REDIRECT_URI

  return mock

@pytest.fixture
def client(mock_oauth: OAuthProvider) -> TestClient:
  app = FastAPI()
  
  routes = Routes(mock_oauth)
  app.include_router(routes.router())

  return TestClient(app)


def test_login_redirects_to_auth(client: TestClient):
  response = client.get("/login", follow_redirects=False)

  assert response.status_code == 307
  assert response.headers["location"] == TEST_REDIRECT_URI

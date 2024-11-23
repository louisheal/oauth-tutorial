import pytest
from fastapi import FastAPI
from pytest_mock import MockerFixture
from fastapi.testclient import TestClient

from app.models import OAuthProvider
from app.routes import Routes


TEST_REDIRECT_URI = "https://example.com/oauth"
TEST_AUTH_CODE = "test auth code"
TEST_ACCESS_TOKEN = "test access token"

@pytest.fixture
def mock_oauth(mocker: MockerFixture) -> OAuthProvider:
  mock = mocker.MagicMock(spec=OAuthProvider)

  mock.get_redirect_url.return_value = TEST_REDIRECT_URI
  mock.get_access_token.return_value = TEST_ACCESS_TOKEN

  return mock

@pytest.fixture
def client(mock_oauth: OAuthProvider) -> TestClient:
  app = FastAPI()
  
  routes = Routes(mock_oauth)
  app.include_router(routes.router())

  return TestClient(app)


def test_login_redirects(client: TestClient, mock_oauth: OAuthProvider):
  response = client.get("/login", follow_redirects=False)

  assert response.status_code == 307
  assert response.headers["location"] == TEST_REDIRECT_URI
  mock_oauth.get_redirect_url.assert_called_once()

def test_callback_uses_auth_code(client: TestClient, mock_oauth: OAuthProvider):
  response = client.get("/callback", params={'code': TEST_AUTH_CODE})

  assert response.status_code == 200
  mock_oauth.get_access_token.assert_called_once()
  mock_oauth.get_access_token.assert_any_call(TEST_AUTH_CODE)

def test_callback_returns_user_data(client: TestClient, mock_oauth: OAuthProvider):
  response = client.get("/callback", params={'code': TEST_AUTH_CODE})

  assert response.status_code == 200
  mock_oauth.get_user_data.assert_called_once()
  mock_oauth.get_user_data.assert_any_call(TEST_ACCESS_TOKEN)

def test_login_uses_state(client: TestClient):
  response = client.get("/login", follow_redirects=False)

  assert response.status_code == 307
  assert response.cookies['state'] is not None

def test_login_passes_state(client: TestClient, mock_oauth: OAuthProvider):
  response = client.get("/login", follow_redirects=False)
  state = response.cookies['state']

  assert response.status_code == 307
  mock_oauth.get_redirect_url.assert_any_call(state)
  
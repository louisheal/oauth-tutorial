from fastapi import APIRouter

from app.models import OAuthProvider


class Routes():
  
  def __init__(self, oauth_provider: OAuthProvider) -> None:
    self._router = APIRouter()
    self.oauth = oauth_provider

    @self._router.get('/login')
    async def get_login():
      pass

    @self._router.get('/callback')
    async def get_callback():
      pass
    
  def router(self) -> APIRouter:
    return self._router

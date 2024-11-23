from fastapi import APIRouter, Request, Response
from fastapi.responses import RedirectResponse
import secrets

from app.models import OAuthProvider


class Routes():
  
  def __init__(self, oauth_provider: OAuthProvider) -> None:
    self._router = APIRouter()
    self._oauth = oauth_provider

    @self._router.get("/login")
    async def get_login():

      # Write your code here #
      ...
      ########################

    @self._router.get("/callback")
    async def get_callback(request: Request, code: str, state: str):
      
      # Write your code here #
      ...
      ########################
    
  def router(self) -> APIRouter:
    return self._router

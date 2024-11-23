import abc


class AccessToken:
  pass


class UserData:
  pass


class OAuthProvider(abc.ABC):
  
  @abc.abstractmethod
  def get_redirect_url(self, state: str | None = None) -> None:
    pass
  
  @abc.abstractmethod
  def get_access_token(self, code: str) -> AccessToken:
    pass
  
  @abc.abstractmethod
  def get_user_data(self, access_token: str) -> UserData:
    pass

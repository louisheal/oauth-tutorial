import abc


class AccessToken:
  pass


class UserData:
  pass


class OAuthProvider(abc.ABC):
  
  @abc.abstractmethod
  def request_user_data(self, state: str) -> None:
    pass
  
  @abc.abstractmethod
  def get_access_token(self, code: str) -> AccessToken:
    pass
  
  @abc.abstractmethod
  def get_user_data(self, access_token: str) -> UserData:
    pass

# OAuth Tutorial
Learn how OAuth works by implementing it yourself!

## Installation

### Clone this repository
```bash
git clone git@github.com:louisheal/oauth-tutorial.git
cd oauth-tutorial
```

### Create virtual environment
#### On MacOS and Windows:
```bash
python -m venv venv
```
#### On Linux:
```bash
python3 -m venv venv
```

### Activate the virtual environment
#### On MacOS and Linux:
```bash
source venv/bin/activate
```
#### On Windows:
```bash
./venv/Scripts/activate
```

### Install the requirements
```bash
pip install -r requirements.txt
```

## Tutorial

### Running tests

You can use our pytest test suite to check your code after each step:
```bash
pytest
```

### app/routes.py
All of your code will be written within the `login` and `callback` routes within `app/routes.py`. You do not need to make any additional imports or change the type signatures of the route methods.


### 1 - Redirect to redirect uri
Within the `login` endpoint, use FastAPI's `RedirectResponse` to redirect the user to the redirect url returned by `OAuthProvider`'s `get_redirect_uri` method.

<details>
  <summary>Answer</summary>

  ```python
  async def get_login():
    redirect_url = self._oauth.get_redirect_url()
    return RedirectResponse(redirect_url)
  ```
</details>

### 2 - Retrieve access token
Within the `callback` endpoint, pass the query parameter `code` to `OAuthProvider`'s `get_access_token` method.

<details>
  <summary>Answer</summary>

  ```python
  async def get_callback(request: Request, code: str, state: str):
    token = self._oauth.get_access_token(code)
  ```
</details>

### 3 - Return user data
Use the access token you just retrieved in order to get the user's data and return it. This can be done using `OAuthProvider`'s `get_user_data` method.

<details>
  <summary>Answer</summary>

  ```python
  async def get_callback(request: Request, code: str, state: str):
    token = self._oauth.get_access_token(code)
    return self._oauth.get_user_data(token)
  ```
</details>

### 4 - Set state cookie
Within the login callback, set state within a secure, http only cookie. State should be a randomly generated, cryptographically secure string (you can use `secrets.token_hex(16)`).

<details>
  <summary>Answer</summary>

  ```python
  async def get_login():
    redirect_url = self._oauth.get_redirect_url()
    response = RedirectResponse(redirect_url)

    state = secrets.token_hex(16)
    response.set_cookie('state', state, httponly=True, secure=True)

    return response
  ```
</details>

### 5 - Send state to redirect
Pass the state variable you generated into the `get_redirect_url` function.

<details>
  <summary>Answer</summary>

  ```python
  async def get_login():
    state = secrets.token_hex(16)
    redirect_url = self._oauth.get_redirect_url(state)

    response = RedirectResponse(redirect_url)
    response.set_cookie('state', state, httponly=True, secure=True)

    return response
  ```
</details>

### 6 - Check state matches
In the `callback` endpoint, check that the state cookie in the request matches the state query parameter. Return a 403 (forbidden) response if the two states do not match.

<details>
  <summary>Answer</summary>

  ```python
  async def get_callback(request: Request, code: str, state: str):
    if request.cookies['state'] != state:
      return Response(status_code=403)

    token = self._oauth.get_access_token(code)
    return self._oauth.get_user_data(token)
  ```
</details>

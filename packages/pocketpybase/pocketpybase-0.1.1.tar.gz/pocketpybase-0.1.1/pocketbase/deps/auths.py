import httpx

class Auths:
    def __init__(self, username, password, host_url=None):
        self.username = username
        self.password = password
        self.host_url = host_url
        if self.host_url is None:
            raise Exception("Host URL is required")
        self.session = httpx.Client()

        response = self.session.post(
            f'{self.host_url}/api/admins/auth-with-password',
            json={
                "identity": self.username,
                "password": self.password
            }
        )
        if response.status_code != 200:
            raise Exception("Login failed")
        self.token = response.json()["token"]

    def get_token(self):
        return self.token

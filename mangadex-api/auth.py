from dataclasses import dataclass, field

import json, requests, os, dotenv

OPENID_CONFIGURATION_URL = "https://auth.mangadex.org/realms/mangadex/.well-known/openid-configuration"
TOKEN_REFRESH_URL = "https://auth.mangadex.org/realms/mangadex/protocol/openid-connect/token"
TOKEN_CHECK_URL = "https://api.mangadex.org/auth/check"


@dataclass
class AuthScopes:
    openid: bool = field(default = True)
    groups: bool = field(default = True)
    email: bool = field(default = True)
    profile: bool = field(default = True)

    @staticmethod
    def default() -> "AuthScopes":
        return AuthScopes()
    
    @staticmethod
    def object_from_string(string: str) -> "AuthScopes":
        return AuthScopes(**{key: True if key in string else False for key in AuthScopes.__dataclass_fields__.keys()})

    def prepare_for_request(self):
        return " ".join([key for key, value in self.__dict__.items() if value])
    
class AuthorizationObject(object):
    def __init__(self, refresh_token: str = "") -> None:
        self.refresh_token = refresh_token
        self.access_token: str = ""
        self.expires_in: int = 0
        self.refresh_expires_in: int = 0
        self.token_type: str = "" # Usually "Bearer"
        self.id_token: str = ""
        self.not_before_policy: int = 0
        self.session_state: str = ""
        self.scope: AuthScopes = ""

    def refresh(self):
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "scope": AuthScopes.default().prepare_for_request(),
            "client_id": "mangadex-frontend-stable"
        }

        response = requests.post(
            TOKEN_REFRESH_URL,
            json=data
        )
        res_data = response.json()
        self.access_token = res_data["access_token"]
        self.expires_in = res_data["expires_in"]
        self.refresh_expires_in = res_data["refresh_expires_in"]
        self.token_type = res_data["token_type"]
        self.id_token = res_data["id_token"]
        self.not_before_policy = res_data["not-before-policy"]
        self.session_state = res_data["session_state"]
        self.scope = AuthScopes.object_from_string(res_data["scope"])
        self.refresh_token = res_data["refresh_token"]

        with open("mdapi_auth.json", "w") as f:
            json.dump(res_data, f)

    def load_json(self):
        with open("mdapi_auth.json", "r") as f:
            self.refresh_token = json.load(f)["refresh_token"]

    def load_env(self):
        dotenv.load_dotenv()
        self.refresh_token = os.getenv("refresh_token")

    
    


from dataclasses import dataclass, field

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
    

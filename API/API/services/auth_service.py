class AuthToken:
    def __init__(self, token: str, creation_date: str, lifetime: int, name: str = None, description: str = None):
        self.token = token
        self.creation_date = creation_date
        self.lifetime = lifetime


class AuthService:
    def verify_token(token: str, name: str = None, description: str = None) -> bool:
        raise Exception
    
    def generate_token(lifetime: int, name: str = None, description: str = None) -> AuthToken:
        raise Exception
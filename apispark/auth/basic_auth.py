from fastapi import HTTPException
from fastapi.security import HTTPBasicCredentials

class BasicAuth:
    def __init__(self, valid_users):
        self.valid_users = valid_users

    def basic_auth_required(self, credentials: HTTPBasicCredentials):
        if credentials.username not in self.valid_users or self.valid_users[credentials.username] != credentials.password:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return credentials

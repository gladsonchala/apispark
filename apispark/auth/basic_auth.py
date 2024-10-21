from fastapi import HTTPException
from fastapi.security import HTTPBasicCredentials

class BasicAuth:
    def __init__(self, valid_users):
        """
        Initializes the BasicAuth class with the specified valid users.

        Args:
            valid_users (dict): A dictionary of valid users and their corresponding passwords.

        Returns:
            None
        """
        self.valid_users = valid_users

    def basic_auth_required(self, credentials: HTTPBasicCredentials):
        """
        Enforces basic authentication for an endpoint.

        This method takes an HTTPBasicCredentials object and verifies the credentials against the
        valid users dictionary. If the credentials are invalid, an HTTPException with a 401
        status code is raised.

        Args:
            credentials (HTTPBasicCredentials): The credentials provided by the client.

        Returns:
            HTTPBasicCredentials: The validated credentials if authentication is successful.

        Raises:
            HTTPException: If the credentials are invalid.
        """
        if credentials.username not in self.valid_users or self.valid_users[credentials.username] != credentials.password:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return credentials

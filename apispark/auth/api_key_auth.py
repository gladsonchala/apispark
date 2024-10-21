from functools import wraps
from fastapi import HTTPException, Header

class APIKeyAuth:
    def __init__(self, valid_keys=["default_key"]):
        """
        Initialize an APIKeyAuth instance.

        Args:
            valid_keys (list): List of valid API keys. Defaults to ["default_key"].
        """
        self.valid_keys = valid_keys

    def api_key_required(self, api_key: str = Header(None)):
        """
        Decorator to check if the API key is valid and in the valid list.
        
        Args:
            api_key (str): The API key passed in the request header.
        
        Returns:
            str: The API key if it is valid and in the valid list.
        
        Raises:
            HTTPException: If the API key is invalid or not in the valid list.
        """
        if api_key not in self.valid_keys:
            raise HTTPException(status_code=403, detail="Invalid API Key")
        return api_key

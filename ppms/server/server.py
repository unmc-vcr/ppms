from abc import ABC
from enum import Enum
from typing import List, Optional, Any, Union
from requests import Request, Session
from dotenv import dotenv_values
from ..excptions.exceptions import InstanceNotSpecified, APIKeyNotSpecified

from .endpoint import *

INSTANCE = None
ENV_API_KEY_NAME = 'PPMS_API_KEY'

class Server():
    def __init__(self, instance: str = INSTANCE, apikey: Union[str,None] = None):
            
            env = dotenv_values()

            apikey = apikey or env.get(ENV_API_KEY_NAME, None)

            if instance is None:
                raise InstanceNotSpecified
            
            if apikey is None:
                raise APIKeyNotSpecified
                 
            self.instance = instance
            self.apikey = apikey

            self.users = Users(self)
            self.publications = Publications(self)
            self.tags = Tag(self)
    
    @property
    def url(self):
        return f"https://ppms.us/{self.instance}/API2/"
    
    def __repr__(self):
        return f"<Server instance='{self.instance}'>"
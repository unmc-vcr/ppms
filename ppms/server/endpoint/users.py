from typing import List, TYPE_CHECKING
from pydantic import TypeAdapter
from ppms.models import User, UserDetail
from .endpoint import Endpoint

if TYPE_CHECKING:
    from ppms.server import Server

class Users(Endpoint):
    def __init__(self, server: "Server") -> None:
        super().__init__(server)

    USER_RESPONSE_VALIDATOR = TypeAdapter(List[User])
    USER_DETAIL_RESPONSE_VALIDATOR = TypeAdapter(List[UserDetail])
    
    def get(self):
        raw = self.get_request('GetUsersList')
        return self.USER_RESPONSE_VALIDATOR.validate_json(raw.text)

    def get_by_id(self, id: int = None, user: User = None):
        if id == None and user == None:
            raise Exception
        elif id != None and user != None:
            raise Exception
        id = id if id is not None else user.id
        raw = PPMSGetRequest.send('GetUserDetailsById', {"checkUserId": id, "coreid": 1})
        validated = self.USER_DETAIL_RESPONSE_VALIDATOR.validate_json(raw.text)
        if len(validated) != 1:
            raise Exception
        return validated[0]
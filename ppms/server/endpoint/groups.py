from typing import List, TYPE_CHECKING
from pydantic import TypeAdapter
from ppms.models import Group, GroupDetail
from .endpoint import Endpoint

if TYPE_CHECKING:
    from ppms.server import Server

class Groups(Endpoint):
    def __init__(self, server: "Server") -> None:
        super().__init__(server)

    GROUP_RESPONSE_VALIDATOR = TypeAdapter(List[Group])
    GROUP_DETAIL_RESPONSE_VALIDATOR = TypeAdapter(List[GroupDetail])
    
    def get(self):
        raw = self.get_request('GetGroupsList')
        return self.GROUP_RESPONSE_VALIDATOR.validate_json(raw.text)
    
    def get_by_id(self, id: int = None, group: Group = None):
        if id == None and group == None:
            raise Exception
        elif id != None and group != None:
            raise Exception
        id = id if id is not None else group.id
        raw = self.get_request('GetGroupDetail', {"unitId": id})
        validated = self.GROUP_DETAIL_RESPONSE_VALIDATOR.validate_json(raw.text)
        if len(validated) != 1:
            raise Exception
        return validated[0]
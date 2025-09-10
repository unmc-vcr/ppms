from .endpoint import Endpoint
from pydantic import TypeAdapter
from typing import List
from ppms.models import Tag

class Tag(Endpoint):

    TAG_RESPONSE_VALIDATOR = TypeAdapter(List[Tag])
    
    def get(self):
        raw = self.get_request('GetTags') 
        return self.TAG_RESPONSE_VALIDATOR.validate_json(raw.text)

    def create(self):
        # action = SetTag
        pass

    def get_links(self):
        # action = GetTagLinks
        pass

    def set_link(self, target):
        try:
            target_object_type = target._OBJECT_TYPE
        except AttributeError: 
            raise AttributeError(f"The target is not a valid taggable object.")
        
        raw = self.post_request(
            "SetTagLink",
            data = {
                'tagId': self.id,
                'inputTagLinkObjType': target_object_type,
                'inputTagLinkObjId': target.id
            }
        )
        pass

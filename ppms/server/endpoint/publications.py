from .endpoint import Endpoint
from typing import List, TYPE_CHECKING
from pydantic import TypeAdapter
from ppms.models import Publication, PublicationLink, PublicationLinkType

if TYPE_CHECKING:
    from ppms.server import Server

class Publications(Endpoint):
    def __init__(self, server: "Server") -> None:
        super().__init__(server)
    
    RESPONSE_VALIDATOR = TypeAdapter(List[Publication])
    LINK_RESPONSE_VALIDATOR = TypeAdapter(List[PublicationLink])

    def get(self, hydrate_links=False):
        raw = self.get_request('GetPublicationsList', {"filter": "validated", "coreid": 1})
        return self.RESPONSE_VALIDATOR.validate_json(raw.text, context={'skip_external': True})

    def get_links(self, id: int = 0, publication: Publication = None):
        id = publication.id if publication is not None else id

        raw = self.get_request('GetPublicationLinks', {"pubid": id})
        return self.LINK_RESPONSE_VALIDATOR.validate_json(raw.text)

    def get_by_id(self, id: int):
        raw = self.get_request('GetPublicationDetails', {"pubid": id})
        validated = self.RESPONSE_VALIDATOR.validate_json(raw.text, context={'skip_external': True})
        if len(validated) != 1:
            raise Exception
        return validated[0]

    def set(self, publication: Publication):
        raw = self.post_request('SetPublication', publication.model_dump(exclude=['links']))
        return raw.json()[0]['id']

    def set_link(self, publication_link: PublicationLink):
        raw = self.post_request('SetPublicationLinks', publication_link.model_dump(exclude_none=True))
        
    def create(self, publication: Publication):
        created_id = self.set(publication)
        if len(publication.links) > 0:
            for link in publication.links:
                link.pubid = created_id
                self.set_link(link)
        return created_id
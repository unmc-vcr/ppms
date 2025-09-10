from .endpoint import Endpoint

class Groups(Endpoint):
    raise NotImplementedError("Groups is not yet implemented in this module.")
    def get(self):
        raw = self.get_request('GetGroupsList')
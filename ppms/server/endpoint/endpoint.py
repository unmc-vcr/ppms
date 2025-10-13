from requests import Request, Session

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ppms.server import Server

class Endpoint():

    def __init__(self, server: "Server"):
        self.server = server

    def preflight_params(self, action: str, params: dict = {}):
        return {"apikey": self.server.apikey, "action": action, **params}
    
    def prepare(self, method, action: str, data: dict = {}):
        req = Request(method, self.server.url)
        params = self.preflight_params(action, data)
        if method == 'GET':
            req.params = params
        elif method == 'POST':
            req.data = params

        return req.prepare()
    
    def _make_request(self, request):
        s = Session()
        try:
            response = s.send(request)
            #logger.debug(f"[{datetime.timestamp()}] Call finished")
        except Exception as e:
            #logger.debug(f"Error making request to server: {e}")
            raise e
        return response
    
    def get_request(self, action, data = {}):
        prepped = self.prepare('GET', action, data)
        return self._make_request(prepped)
    
    def post_request(self, action, data):
        prepped = self.prepare('POST', action, data)
        return self._make_request(prepped)

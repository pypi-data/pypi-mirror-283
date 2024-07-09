import os
from dotenv import load_dotenv
import requests
from typing import Union, Optional
from .blueguard_uris import BlueguardURIs

load_dotenv()
class ClientRequests:
    def __init__(self, uris: BlueguardURIs):
        self._uris = uris
        self.api_key = None
    
    @property
    def uris(self):
        return self._uris
    
    def external_header(self, API_KEY):
        return dict(Accept="application/json", api_key=f"Bearer {API_KEY}") 
    

    def make_request_external(self, request_type: Union[requests.get, requests.post], uri: str, api_key: Optional[str] = None, payload: dict = None):
        if api_key:
            self.api_key = api_key
            response = request_type(uri, json=payload, headers=self.external_header(API_KEY=api_key))
        else:
            response = request_type(uri, json=payload)
        return response
    
    
    
class ClientGetRequests(ClientRequests):
    def __init__(self, uris: BlueguardURIs):
        self.request_type = requests.get
        super(ClientGetRequests, self).__init__(uris)
        
    def health(self):
        return self.make_request_external(self.request_type, self.uris.health)
    
    def metrics(self, api_key):
        return self.make_request_external(self.request_type, self.uris.metrics, api_key)
    
    def version(self, api_key):
        return self.make_request_external(self.request_type, self.uris.api_version, api_key)
    
    
class ClientPostRequests(ClientRequests):
    def __init__(self, uris: ClientRequests):
        self.request_type = requests.post
        super(ClientPostRequests, self).__init__(uris)
        
    def process_text(self, request_object, api_key):
        return self.make_request_external(self.request_type, self.uris.process_text, api_key, request_object)
    
    def reidentify_text(self, request_object, api_key):
        return self.make_request_external(self.request_type, self.uris.reidentify_text, api_key, request_object)

        

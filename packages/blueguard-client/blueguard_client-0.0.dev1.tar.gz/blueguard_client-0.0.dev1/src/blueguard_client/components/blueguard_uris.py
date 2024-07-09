
class BlueguardURIs:
    
    def __init__(self, url=None, scheme=None, host=None, port=None):
        if url:
            self._uri = url.rstrip('/') + '/'
        elif scheme and host:
            self.valid_schemes = ['http', 'https']
            scheme = scheme.split("://")[0]
            if scheme not in self.valid_schemes:
                raise ValueError(f"Scheme must be one of the following: {', '.join(self.valid_schemes)}")
            port = f":{port}" if port else ""
            self._uri = f"{scheme}://{host}{port}/".rstrip('/') + '/'
        else:
            ValueError("BlueGuardAPIClient needs either url or a scheme and host to initialize. You can find more information on which url to use in our documention at docs.blueguard.ai")
    
    def _create_uri(self, *args):
        return "/".join([i.strip("/") for i in args]).rstrip('/') + '/'
    
    @property
    def uri(self):
        return self._uri
    
    @property
    def api_version(self):
        return self._create_uri(self.uri, "version")
    
    @property
    def health(self):
        return self._create_uri(self.uri, "ping")
    
    @property
    def metrics(self, org_id: str = 1):
        return self._create_uri(self.uri, "api", "metrics", "application", str(org_id))
    
    @property
    def process_text(self):
        return self._create_uri(self.uri, "api", "process", "text", "deid")
    
    @property
    def reidentify_text(self):
        return self._create_uri(self.uri, "api", "process", "text", "reid")
    
    
    
                
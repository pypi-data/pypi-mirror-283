import logging
from .components.blueguard_uris import *
from .components.blueguard_requests import *
from .components.blueguard_response import *
from .components.request_objects import *

class BlueGuardAPIClient:
    
    def __init__(self, scheme: str = None, host: str = None, port: str = None, url: str = None, **kwargs):
        self._uris = BlueguardURIs(scheme=scheme, host=host, port=port, url=url)
        self.get = ClientGetRequests(self._uris)
        self.post = ClientPostRequests(self._uris)
        self.api_key = kwargs.get("api_key")
        self.org_uuid = kwargs.get("org_uuid")

    def get_version(self):
        version = VersionResponse(self.get.version(api_key=self.api_key))
        return version.get_version_details
         
    def health(self):
        response = self.get.health()
        if response.status_code != 200:
            logging.warning(f"The API server cannot be reached at this moment.")
            return False
        return True
    
    def form_extra_objects_from_kwargs(self, **kwargs):
        extra_objects = dict()
        if "policy_id" in kwargs:
            extra_objects["policy_id"] = kwargs["policy_id"]
        if "enable_details" in kwargs:
            extra_objects["enable_details"] = kwargs["enable_details"]
        if "enable_sensitive_scan" in kwargs:
            extra_objects["enable_sensitive_scan"] = kwargs["enable_sensitive_scan"]         
        if "identify_credentials" in kwargs:
            extra_objects["identify_credentials"] = kwargs["identify_credentials"]
        if "glossary_terms" in kwargs:
            extra_objects["glossary_terms"] = kwargs["glossary_terms"]
        if "lang" in kwargs:
            extra_objects["lang"] = kwargs["lang"]
        if "context_id" in kwargs:
            extra_objects["context_id"] = kwargs["context_id"]
        extra_objects["org_uuid"] = self.org_uuid
        return extra_objects
    
    def process_text(self, mode: Mode, text_inputs: list, **add_params):
        extra_objects = self.form_extra_objects_from_kwargs(**add_params)
        if mode == Mode.REDACT:
            objects = RedactRequestObjects(inputs=text_inputs, add_params=extra_objects)
        elif mode == Mode.MASK:
            objects = MaskRequestObjects(inputs=text_inputs, add_params=extra_objects)
        elif mode == Mode.REPLACE:
            objects = ReplaceRequestObjects(inputs=text_inputs, add_params=extra_objects)
        response = ProcessTextResponse(self.post.process_text(request_object=objects.to_dict(), api_key=self.api_key))
        if response._details:
            raise ValueError(f"Request failed: {response._details}")
        if response._output_response:
            return response

    def reidentify_text(self, text_inputs: str, **add_params):
        extra_objects = self.form_extra_objects_from_kwargs(**add_params)
        objects = ReidentifyRequestObjects(inputs=text_inputs, add_params=extra_objects)
        response = ReIdentifyTextResponse(self.post.reidentify_text(request_object=objects.to_dict(), api_key=self.api_key))
        if response._details:
            raise ValueError(f"{response._details}")
        if response._output_response:
            return response
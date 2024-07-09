from typing import *
from .modes import Mode


class ClientBaseRequest:
    
    def  __init__(self, mode: Optional[str], inputs: Optional[List[str]], extra_objects: Optional[dict]):
        self.mode = mode
        self.inputs = inputs
        self.input_list = []
        self.org_uuid = extra_objects.get("org_uuid", None)
        self.policy_id = extra_objects.get("policy_id", None)
        self.enable_details = extra_objects.get("enable_details", False)
        self.enable_sensitive_scan = extra_objects.get("enable_sensitive_scan", False)
        self.identify_credentials = extra_objects.get("identify_credentials", False)
        self.glossary_terms = extra_objects.get("glossary_terms", [])
        self.lang = extra_objects.get("lang", "en")
        
    def is_input_list_empty(self):
        return self.input_list == []
        
    def form_inputs(self):
        self.input_list = [{"text": input_text} for input_text in self.inputs]
            
    def to_dict(self) -> dict[str, Any]:
        request_objects = dict(
            mode=self.mode,
            inputs=self.input_list,
            org_uuid=self.org_uuid,
            policy_id=self.policy_id,
            enable_details=self.enable_details,
            enable_sensitive_scan=self.enable_sensitive_scan,
            identify_credentials=self.identify_credentials,
            glossary_terms=self.glossary_terms,
            lang=self.lang,
        )
        return request_objects
class RedactRequestObjects(ClientBaseRequest):
    def __init__(self, inputs: List[str], add_params: dict):
        super(RedactRequestObjects, self).__init__(mode=Mode.REDACT, inputs=inputs, extra_objects=add_params)
        self.form_inputs()
        if self.is_input_list_empty():
            raise ValueError("Input list can't be empty.")


class ReplaceRequestObjects(ClientBaseRequest):
    def __init__(self, inputs: List[str], add_params: dict):
        super(ReplaceRequestObjects, self).__init__(mode=Mode.REPLACE, inputs=inputs, extra_objects=add_params)
        self.form_inputs()
        if self.is_input_list_empty():
            raise ValueError("Input list can't be empty.")
    

class MaskRequestObjects(ClientBaseRequest):
    def __init__(self, inputs: List[str], add_params: dict):
        super(MaskRequestObjects, self).__init__(mode=Mode.MASK, inputs=inputs, extra_objects=add_params)
        self.form_inputs()
        if self.is_input_list_empty():
            raise ValueError("Input list can't be empty.")

class ReidentifyRequestObjects(ClientBaseRequest):
    def  __init__(self, inputs: Optional[List[str]], add_params: dict):
        super(ReidentifyRequestObjects, self).__init__(mode=None, inputs=inputs, extra_objects=add_params)

        self.context_id = add_params.get("context_id")
        self.enable_details = add_params.get("enable_details", False)
        self.org_uuid = add_params.get("org_uuid")
      
    def to_dict(self) -> dict:
        self.form_inputs()
        base_request_object = dict(
            inputs= self.input_list,
            context_id=self.context_id,
            org_uuid=self.org_uuid,
            enable_details=self.enable_details
        )
        return base_request_object


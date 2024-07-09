from requests import HTTPError, Response
import json

class BaseResponse:
    def __init__(self, response_object: Response, json_response: bool = True):
        self._response = response_object
        self._json_response = json_response
        if not self.ok:
            message = (f"This request has returned a {self.status_code} for {self.reason}.")
            if self.status_code == 402:
                message += f"request body -- {self.json_response}"
            raise HTTPError(message)
        
    def __call__(self):
        return self._response
    
    @property
    def ok(self):
        return self._response.ok
    
    @property
    def status_code(self):
        return self._response.status_code
    
    @property
    def reason(self):
        return self._response.reason
    
    @property
    def json_response(self):
        if self._json_response:
            return self._response.json()
        else:
            return self._response.text
        
    @json_response.setter
    def json_response(self, new_response):
        if type(new_response) is not Response:
            raise ValueError("response must be a Response object.")
        self._response = new_response

    def get_attribute_by_entries(self, name):
        if not self._json_response:
            raise ValueError("get_attribute_entries needs a response of type json")
        body = self.json_response
        if type(body) is list:
            return [row.get(name) for row in self().json()]
        elif type(body) is dict:
            return body.get(name)
        
class VersionResponse(BaseResponse):
    def __init__(self, response_object: Response = None):
        super(VersionResponse, self).__init__(response_object, json_response=True)
        
    @property
    def get_version_details(self):
        return self.get_attribute_by_entries("version")
    
class MetricsResponse(BaseResponse):
    def __init__(self, response_object: Response = None):
        super(MetricsResponse, self).__init__(response_object, json_response=True)
        
class ProcessTextResponse(BaseResponse):
    def __init__(self, response_object: Response = None):
        super(ProcessTextResponse, self).__init__(response_object, json_response=True)
        self._output_response = self.get_attribute_by_entries('output')
        self._details = self.get_attribute_by_entries('detail')
        
    def get_results_by_fields(self, field: str):
        if self._output_response is None:
            raise ValueError(self._details)
        else:
            return [response.get(field) for response in self._output_response]
        
    def extract_detailed_info(self):
        json_r = self.json_response
        if 'output' not in json_r:
            raise ValueError("The provided dictionary does not contain the 'output' key")

        result = {
            "success": json_r.get("success"),
            "status": json_r.get("status"),
            "output": [],
        }

        output_list = json_r['output']
        for item in output_list:
            processed_item = {
                "original_text": item.get("original_text"),
                "processed_text": item.get("processed_text"),
                "entities_exists": item.get("entities_exists"),
                "characters_processed": item.get("characters_processed"),
                "words_processed": item.get("words_processed"),
                "context_id": item.get("context_id"),
                "detailed_info": [],
                "replaced_words": item.get("replaced_words"),
                "sensitive_words": item.get("sensitive_words")
            }

            detailed_info_list = item.get("detailed_info", [])
            for sub_item in detailed_info_list:
                processed_sub_item = {
                    "start": sub_item.get("start"),
                    "end": sub_item.get("end"),
                    "score": sub_item.get("score"),
                    "entity_type": sub_item.get("entity_type"),
                    "entity_value": sub_item.get("entity_value"),
                    "start_processed": sub_item.get("start_processed"),
                    "end_processed": sub_item.get("end_processed")
                }
                processed_item["detailed_info"].append(processed_sub_item)

            result["output"].append(processed_item)

        return result

    def to_dict(self) -> dict[str, any]:
        result = self.extract_detailed_info()
        return result

    @property
    def output(self):
        return self.get_attribute_by_entries("output")
    
    @property
    def success(self):
        return self.get_attribute_by_entries("success")
    
    @property
    def status(self):
        return self.get_attribute_by_entries("status")

    @property
    def original_text(self):
        return self.get_results_by_fields("original_text")
    
    @property
    def processed_text(self):
        return self.get_results_by_fields('processed_text')

    @property
    def entities_exists(self):
        return self.get_results_by_fields('entities_exists')
    
    @property
    def characters_processed(self):
        return self.get_results_by_fields('characters_processed')
        
    @property
    def words_processed(self):
        return self.get_results_by_fields('words_processed')
    
    @property
    def context_id(self):
        return self.get_results_by_fields("context_id")
    
    @property
    def replaced_words(self):
        return self.get_results_by_fields("replaced_words")
    
    @property
    def sensitive_words(self):
        return self.get_results_by_fields("sensitive_words")
    
    @property
    def detailed_info(self):
        return self.get_results_by_fields("detailed_info")
    
    
class ReIdentifyTextResponse(ProcessTextResponse):
    def __init__(self, response_object: Response = None):
        super(ProcessTextResponse, self).__init__(response_object, json_response=True)
        self._output_response = self.get_attribute_by_entries('output')
        self._details = self.get_attribute_by_entries('details')

        
        
                
        
        
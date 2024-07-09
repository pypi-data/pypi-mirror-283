# Example illustration using the blueguard client to access the blueguard privacy APIs
# To be able run this client from command-line
# `cd src` and run `python -m blueguard_client.client_example`
import os, json
from blueguard_client import BlueGuardAPIClient, Mode

# Load the API_KEY variable
api_key = os.getenv('BLUEGUARD_API_KEY')
org_uuid = os.getenv('ORG_UUID')

# Initialize Blueguard API Client with URL
BLUEGUARD_SCHEME = "https"
BLUEGUARD_HOST = "localhost"
BLUEGUARD_URL = BLUEGUARD_SCHEME + "://" + BLUEGUARD_HOST

bgx_client = BlueGuardAPIClient(url = BLUEGUARD_URL, api_key=api_key, org_uuid=org_uuid)
#bgx_client = BlueGuardAPIClient(url="http://localhost:80", api_key=api_key, org_uuid=org_uuid)

# Check the health of the server /ping/
print(bgx_client.health())

# Get the current version of the server
print(bgx_client.get_version())

sample_text = ['Hi Sam, how are you. Whats your Margin', 'I live in Chennai']

# Mask text
response = bgx_client.process_text(Mode.MASK, text_inputs=sample_text)
print(response.processed_text, response.context_id)

# Redact: Enables replacement with appropriate entity types detected for the values eg. If the entity value is "Ram" then it's redacted as [PERSON], similary age 54 with [AGE] etc.
response = bgx_client.process_text(Mode.REDACT, text_inputs=sample_text)
print(response.processed_text, response.context_id)

# Replace: Replace mode replaces detected entity values in the input text with real fake data values that are relevant eg. entity value "Ram" with Lakshman, age 54 with 45 etc.
response = bgx_client.process_text(Mode.REPLACE, text_inputs=sample_text)
print(response.processed_text, response.context_id)


sample_text = ["Hi Ram, I lost my cc card in Chennai", "I love Sathya"]
response = bgx_client.process_text(Mode.REDACT, text_inputs=sample_text)
processed_text = response.processed_text
context_id = response.context_id

# Let us recall the original text by calling reidentify_text with the previously processed (redacted/masked/replaced) text
original_text_reidentified = bgx_client.reidentify_text(text_inputs= processed_text
                                                        , context_id = context_id[0]
                                                        , enable_details = True) # context_id that was originally passed to the original de-identification
print(f"Original Text RE-Identified: {original_text_reidentified.original_text[0]}") 

sample_text = ["Hi Ram"]
# Detailed Redacted response with index positions of redacted entities.
# This is helpful if your application needs visibility into exact words & the positions of these words in the processed_text.
# To fetch details part of the response, ensure to add addtional params such as `enable_details=True`
response = bgx_client.process_text(Mode.REDACT, text_inputs=sample_text
                                                     , enable_details = True # If True, each entity detected, it's position with start & end index etc is included. If False (default), then processed_text is output without details
                                                     , enable_sensitive_scan = False # If True, custom terms are scanned. None, otherwise.
                                                 , identify_credentials = False) # If True, Multiple Keys/Credentials such as AWS, SSH, RSA, Azure, Google's keys are detected.
print(f"Redacted Text With Details: {response.processed_text},  \n output: {json.dumps(response.output, indent=4)} ")

### There are 2 ways to retrieve details from the response from the call.
# 1. Using  response.extract_detailed_info() - as shown below which returns an object from which attributes can be extracted
# for eg. `detailed_json['output'][0]['processed_text'])` extracts the processed_text from the first item from the output of the response
# for more details refer to the response#extract_detailed_info() - method for the structure of the response object.
### 
detailed_json = response.extract_detailed_info()
processed_text = [detailed_json['output'][0]['processed_text']]
context_id = detailed_json['output'][0]['context_id']
print(f"Text DE-Identified: {processed_text}")

# Prints the json representation of the response from the redacted text / API
print("\n Complete JSON Response \n ############################ \n" + json.dumps(detailed_json, indent=4))

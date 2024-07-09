# Blueguard Python Client

A Python client library for communicating with the Blueguard API. This document provides information about how to best use the client. For more information, see Blueguard's [API Documentation.][1]

### Quick Links

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Running the tests](#testing)
4. [Working with the Client](#client)

## Installation

To install the BlueGuard SDK, you can use pip:

```bash
pip install blueguard_client
```

Or, if you're installing from the source (recommended as this is not published in pypi yet):

```bash
git clone https://github.com/bluegennx-ai/blueguard-thin-client.git
cd blueguard-thin-client

python3 -m venv venv
source venv/bin/activate

pip install -e .
```

## Configuration

To use the BlueGuard SDK, you need to have an API key. You can obtain this from the BlueGuard team.


### Installation <a name=installation></a>

```bash
pip install blueguard_client
```

### Quick Start <a name=quick-start></a>

```python

from blueguard_client import BlueGuardAPIClient, Mode
from blueguard_client import request_objects

sample_text = ['Hi Sam, how are you']
client = BlueGuardAPIClient(url="http://localhost:8080"
                                            , api_key=api_key # your Org's API Key to access Blueguard Privacy API
                                            , org_uuid=org_uuid) # unique id for your organization)

response = client.process_text(Mode.MASK, text_inputs=sample_text)

print(sample_text)
print(response.processed_text)


```

Output:

```
['Hi Sam, how are you']
['Hi [PERSON], how are you']
```

### Running the tests <a name=testing></a>

We use [pytest](https://docs.pytest.org/) to run our tests in the tests folder.

To run from command line, ensure you have pytest installed, and then run `pytest` from the main project folder.

```shell
pip install -U pytest -y
pytest
```

Alternatively, you can automatically run all tests from the Testing window in Visual Studio Code.

### Working With The Client <a name=client></a>

#### Initializing the Client

The Blueguard client requires a scheme, host, and optional port to initialize. 
Alternatively, a full url can be used. The APIs are authorized by adding an API key
and org_uuid while initializing the client.

Once created, the connection can be tested with the client's `health` function

```python
scheme = 'http'
host = 'localhost'
port= '8080'
api_key = '<API_KEY>'
org_uuid = '<ORG_UUID>'
client = BlueGuardAPIClient(scheme, host, port, api_key, org_uuid)

client.health()


url = "http://localhost:8080"
client = BlueGuardAPIClient(url=url)

client.health()
```

Output:

```
True
True
```

#### Making Requests

Once initialized the client can be used to make any request listed in the [Blueguard-Privacy-API documentation][1]

Available requests:

| Client Function                   | Endpoint                   |
| ------------------------          | -------------------------- |
| `version()`                       | `/version/`                |
| `health()`                        | `/ping/`                   |
| `get_metrics()`                   | `/api/metrics/application/`|
| `process_text()`                  | `/api/process/text/deid/`   |
| `reidentify_text()`               | `/api/process/text/reid/`   |

Requests can be made using asbtracted methods for each Mode [Redact/Replace/Mask] or Reidentify by passing
dictionary objects.

##### De-Identification using redaction

Redact: Enables replacement with appropriate entity types detected for the values eg. If the entity value is "Ram" then it's redacted as [PERSON], similary age 54 with [AGE] etc.

```python
sample_text = ['Hi Sam, how are you', 'I live in Chennai']
response = bgx_client.process_text(Mode.REDACT, text_inputs=sample_text)
print(response.processed_text, response.context_id)
```

Output:

```
['Hi [PERSON], how are you', 'I live in [CITY]'] ['00000000-0000-0000-a3425a-5679c9615a', '00000000-0000-0000-343d-af956uftyd9f0']
```

##### De-Identification using replacement

Replace: Replace mode replaces detected entity values in the input text with real fake data values that are relevant eg. entity value "Ram" with Lakshman, age 54 with 45 etc.

```python
sample_text = ['Hi Sam, how are you', 'I live in Chennai']
response = bgx_client.process_text(Mode.REPLACE, text_inputs=sample_text)
print(response.processed_text, response.context_id)
```

Output:

```
['Hi Ram, how are you', 'I live in Bijapur'] ['00000000-0000-0000-a335a-5679c9615a', '00000000-0000-0000-333d-af956uftyd9f0']
```

##### De-Identification using masking

Mask text: Enables replacing detected entities text ###### characters in their positions

```python
sample_text = ['Hi Sam, how are you', 'I live in Chennai']
response = bgx_client.process_text(Mode.MASK, text_inputs=sample_text)
print(response.processed_text, response.context_id)
```

Output:

```
['Hi ###, how are you', 'I live in #######'] ['00000000-0000-0000-a325a-5679c9615a', '00000000-0000-0000-323d-af956uftyd9f0']
```

##### Re-Identification - Retrieve original text from de-identified text

Re-identify: Enables retrieving a previously redacted/masked/replaced text to it's original text. This functionality needs to
have the context_id that was returned from the `/api/process/text/deid/` when the original text was de-identified.
See example below.

```python
sample_text = ["Hi Ram, I lost my cc card in Chennai", "I love Sathya"]
response = bgx_client.process_text(Mode.REDACT, text_inputs=sample_text)
processed_text = response.processed_text
context_id = response.context_id 

# Let us recall the original text by calling reidentify_text with the previously processed (redacted/masked/replaced) text
original_text_reidentified = bgx_client.reidentify_text(text_inputs= processed_text
                                                        , context_id = context_id[0]
                                                        , enable_details = True) # context_id that was originally passed to the original de-identification
print(f"Original Text RE-Identified: {original_text_reidentified.original_text[0]}")
```

Output:

```
Original Text RE-Identified: Hi Ram, I lost my cc card in Chennai
```

##### How to fetch details of words/text that are de-id/re-id ?

When text is deidentified, you may want to know what words, their classification of entities (PERSON, AGE, DATEOFBIRTH, CREDICARDNUMBER, CVV etc.), 
their positions in the original and the processed text. 
`/process/text/` APIs provide these details when `enable_details` is set to `True` as in the example below.

```python
sample_text = ["Hi Ram"]
response = client.process_text(Mode.REDACT, text_inputs=sample_text
                                                    , enable_details = True # If True, each entity detected, it's position with start & end index etc is included. If False (default), then processed_text is output without details
                                                    , enable_sensitive_scan = False # If True, custom terms are scanned. None, otherwise.
                                                    , identify_credentials = False) # If True, Multiple Keys/Credentials such as AWS, SSH, RSA, Azure, Google's keys are detected.
print(f"Redacted Text With Details: {response.processed_text},  \n output: {response.output} ")
```

Output:

```
Redacted Text With Details: ['Hi [PERSON]'],  
 output: [
    {
        "original_text": "Hi Ram",
        "processed_text": "Hi [PERSON]",
        "entities_exists": true,
        "characters_processed": 6,
        "words_processed": 2,
        "context_id": "00000000-0000-0000-f453-7vjhg74a898",
        "detailed_info": [
            {
                "start": 2,
                "end": 6,
                "score": 0.9996964931488037,
                "entity_type": "PERSON",
                "entity_value": "Ram",
                "start_processed": 3,
                "end_processed": 11
            }
        ],
        "replaced_words": 0
    }
] 
```

[Refer to the executable client Example](https://github.com/bluegennx-ai/blueguard-thin-client/blob/main/src/blueguard_client/client_example.py)

[1]: https://docs.bluegennx.ai/
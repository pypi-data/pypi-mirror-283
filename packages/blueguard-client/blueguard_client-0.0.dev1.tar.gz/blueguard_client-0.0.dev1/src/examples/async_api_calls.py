# Example script to illustrate how to make API calls to Blueguard API.
#
# To run this script you need to have Blueguard API_KEY and ORG_UUID 
# for your organization and the endpoint where this script interacts with.
# To get started, send us an email to subscribe@bluegennx.ai.
#
# In order to use the API, your keys issued by Blueguard should be available to the process
# < you can export them as environement variables. `export API_KEY=<your key here>; 
# export ORG_UUID=<your org_uuid here>` and run ` python async_call.py` 
# or you can define a `.env` file which has the lines `API_KEY=<your key here> 
# ORG_UUID=<your org_uuid here>`.
#
# To be able to run this example from command line, `cd src` and run `python examples/async_api_calls.py`

import os
import pprint
import asyncio
from typing import Dict

import aiohttp
import requests
import dotenv

dotenv.load_dotenv()

# Our other client_example files use the blueguard_client, but this demonstrates async calls with async built libraries

# Define an asynchronous function using the aiohttp library.
async def async_aiohttp_call() -> None:

# create an asynchronous aiohttp client session
    async with aiohttp.ClientSession() as session:
        
        ORG_UUID = os.environ["ORG_UUID"]
        # create an asynchronous aiohttp post call, done outside the blueguard client to use aiohttp
        async with session.post(
            url="https://localhost:80/api/process/text/deid/",
            headers={"api_key": "Bearer " + os.environ["API_KEY"]},
            json={
                "mode": "replace",
                "inputs": [                                                        
                    {"text": "Hi Ram, how are you?"}
                ],
                "org_uuid": ORG_UUID
            }
        ) as response:

            # print the deidentified text
            pprint.pprint(await response.json())


# Turn synchronous post call from the requests library to an asynchronous call.
async def async_post(
    url: str,
    headers: Dict[str, str],
    json: Dict[str, str]
) -> requests.Response:
    return requests.post(
        url=url,
        headers=headers,
        json=json
    )

async def async_requests_call() -> None:

    ORG_UUID = os.environ["ORG_UUID"]

    response = await async_post(
        url="https://localhost:80/api/process/text/deid/",
        headers = {"api_key": "Bearer " + os.environ["API_KEY"]},
        json = {
            "mode": "redact",
            "inputs": [                                                        
                {"text": "Hi Ram, how are you?"}
            ],
            "org_uuid": ORG_UUID
        }
    )

    # check if the request was successful
    response.raise_for_status()

    # print the result in a readable way
    pprint.pprint(response.json())


if __name__ == "__main__":
    
    # Use to load the API key for authentication
    dotenv.load_dotenv()
    
    # Check if the API_KEY environment variable is set
    if "API_KEY" not in os.environ:
        raise KeyError("API_KEY must be defined in order to run the examples.")

    if "ORG_UUID" not in os.environ:
        raise KeyError("ORG_UUID must be defined in order to run the examples.")
    
    # Run the examples
    asyncio.run(async_aiohttp_call())
    asyncio.run(async_requests_call())
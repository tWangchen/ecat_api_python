import argparse
import json
import logging
import os
from typing import Any, Tuple

import requests
from dotenv import load_dotenv

load_dotenv()


# Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s: %(levelname)s:%(name)s: %(message)s")
file_handler = logging.FileHandler("ecatid_uuid.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

ECAT_USERNAME = os.environ.get("ECAT_USERNAME") or ""
ECAT_PASSWORD = os.environ.get("ECAT_PASSWORD") or ""

# Use this to target specific eCat environment
ECAT_ENV = os.environ.get("ECAT_ENV") or ""
# Base url for the api endpoints
ECAT_BASE_URL = f"https://{ECAT_ENV}.ga.gov.au/geonetwork/srv/api"

# Option to specify arguments at runtime.
parser = argparse.ArgumentParser(description="find uuid for ecatid or vice versa")
parser.add_argument("--ecatid", type=str, help="ecatid to get uuid for")
parser.add_argument("--uuid", type=str, help="uuid to get ecatid for")

args = parser.parse_args()

# Note: If ecatid or uuid is not specified at runtime, you can fill them in the current empty string placeholder after or
# you do not have to supply both.
ECATID = args.ecatid or ""  # example: "149071"
UUID = args.uuid or ""  # example: "cbac5898-b284-4176-ae4e-0aa86db50619"


# You should not have to make any changes after this point
def get_auth_headers() -> Tuple[str, str]:
    """
    Obtains eCat API authentication headers.

    This function is designed to retrieve the necessary authentication headers for interacting with the eCat API.
    It returns a tuple containing the 'XSRF-TOKEN' and 'Set-Cookie' headers, which are typically required for maintaining
    session state and preventing cross-site request forgery (CSRF) attacks.

    Returns:
        Tuple[str, str]: A tuple containing the 'XSRF-TOKEN' and 'Set-Cookie' headers.
    """
    headers = {"Accept": "application/json"}
    logger.info(f"Getting your token and cookies from eCat API...")
    response = requests.get(
        f"{ECAT_BASE_URL}/me",
        headers=headers,
        auth=(ECAT_USERNAME, ECAT_PASSWORD),
    )
    if response.status_code != 200:
        logger.exception(f"Error auth with eCat API. Status: {response.status_code}")
        raise Exception(f"Error auth with eCat API. Status: {response.status_code}")

    xsrf_token = response.cookies["XSRF-TOKEN"]
    logger.info(f"Got your XSRF-TOKEN from eCat API.")

    set_cookie = response.headers["Set-Cookie"]
    logger.info(f"Got your Header Set  from eCat API.")

    return xsrf_token, set_cookie


def search(payload) -> Any:
    """
    Performs a search operation based on the provided payload

    Args:
        payload (Any): The payload based on which the search operation is to be performed.

    Returns:
        Any: The result of the search operation in json format.
    """
    xsrf_token, set_cookie = get_auth_headers()
    headers = {
        "Accept": "application/xml",
        "X-XSRF-TOKEN": xsrf_token,
        "Cookie": set_cookie,
        "Content-Type": "application/json",
    }
    payload = payload
    response = requests.get(
        f"{ECAT_BASE_URL}/search/records/_search",
        headers=headers,
        data=payload,
        auth=(ECAT_USERNAME, ECAT_PASSWORD),
    )
    if response.status_code != 200:
        print(response)
        logger.exception(f"Error response status: {response.status_code}")
        raise Exception(f"Error response status: {response.status_code}")

    response_json = json.loads(response.text)

    return response_json


def ecatid_to_uuid(ecatid) -> str:
    """
    This function takes an eCatId as input and returns a string representation of it's UUID.

    Args:
        ecatid (ECATID): The eCatId to be converted.

    Returns:
        str: The UUID string representation of the input eCatId.
    """
    payload_ecatid = json.dumps(
        {"query": {"query_string": {"query": f"(eCatId:{ecatid})"}}}
    )
    response_json = search(payload=payload_ecatid)
    uuid = response_json["hits"]["hits"][0]["_id"]

    return uuid


def uuid_to_ecatid(uuid) -> str:
    """
    This function takes UUID as input and returns a string representation of it's eCatId.

    Args:
        uuid (UUID): The UUID to be converted.

    Returns:
        str: The eCatId string representation of the input UUID.
    """
    payload_uuid = json.dumps({"query": {"query_string": {"query": f"(uuid:{uuid})"}}})
    response_json = search(payload=payload_uuid)
    ecatid = response_json["hits"]["hits"][0]["_source"]["eCatId"]

    return ecatid


def main() -> None:
    try:
        if ECATID and UUID:
            uuid = ecatid_to_uuid(ecatid=ECATID)
            logger.info(f"Obtained UUID: {uuid} for eCatId: {ECATID}")
            print(f"Obtained UUID: {uuid} for eCatId: {ECATID}")

            ecatid = uuid_to_ecatid(uuid=UUID)
            logger.info(f"Obtained eCatId: {ecatid} for UUID: {UUID}")
            print(f"Obtained eCatId: {ecatid} for UUID: {UUID}")
        elif ECATID:
            uuid = ecatid_to_uuid(ecatid=ECATID)
            logger.info(f"Obtained UUID: {uuid} for eCatId: {ECATID}")
            print(f"Obtained UUID: {uuid} for eCatId: {ECATID}")
        elif UUID:
            ecatid = uuid_to_ecatid(uuid=UUID)
            logger.info(f"Obtained eCatId: {ecatid} for UUID: {UUID}")
            print(f"Obtained eCatId: {ecatid} for UUID: {UUID}")
        else:
            logger.info(f"No eCatId or UUID provided.")
            print(f"No eCatId or UUID provided.")
    except Exception as e:
        logger.exception(f"Exception from main: {e}")
    return None


if __name__ == "__main__":
    main()

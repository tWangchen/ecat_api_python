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

# Provide option to specify arguments at runtime.
parser = argparse.ArgumentParser(description="find uuid for ecatid or vice versa")
parser.add_argument("--env", type=str, help="ecat environment")
parser.add_argument("--ecatid", type=str, help="ecatid to get uuid for")
parser.add_argument("--uuid", type=str, help="uuid to get ecatid for")
args = parser.parse_args()

ECATID = os.environ.get("ecatid") or args.ecatid
UUID = os.environ.get("uuid") or args.uuid
ENV = os.environ.get("env") or args.env
# Base url for the api endpoints. Defaults to production.
if ENV.lower() in ("dev", "test"):
    ECAT_BASE_URL = f"https://{ENV}.ecat.ga.gov.au/geonetwork/srv/api"
else:
    ECAT_BASE_URL = "https://ecat.ga.gov.au/geonetwork/srv/api"


def search(payload) -> Any:
    headers = {"Content-Type": "application/json"}
    payload = payload
    response = requests.post(
        f"{ECAT_BASE_URL}/search/records/_search", headers=headers, data=payload
    )
    if response.status_code != 200:
        print(response)
        logger.exception(f"Error response status: {response.status_code}")
        raise Exception(f"Error response status: {response.status_code}")

    response_json = json.loads(response.text)

    return response_json


def ecatid_to_uuid(ecatid) -> str:
    payload_ecatid = json.dumps(
        {"query": {"query_string": {"query": f"(eCatId:{ecatid})"}}}
    )
    response_json = search(payload=payload_ecatid)
    uuid = response_json["hits"]["hits"][0]["_id"]

    return uuid


def uuid_to_ecatid(uuid) -> str:
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

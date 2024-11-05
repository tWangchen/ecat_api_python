import json
import logging
import os
from typing import Tuple

import requests
from dotenv import load_dotenv

load_dotenv()

# Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s: %(levelname)s:%(name)s: %(message)s")
file_handler = logging.FileHandler("ecat_record_with_token.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

ECAT_USERNAME = os.environ.get("ECAT_USERNAME")
ECAT_PASSWORD = os.environ.get("ECAT_PASSWORD")
ENV = os.environ.get("ENV")
# Base url for the api endpoints.
if ENV.lower() in ("prod"):
    ECAT_BASE_URL = "https://ecat.ga.gov.au/geonetwork/srv/api"
else:
    ECAT_BASE_URL = f"https://{ENV}.ecat.ga.gov.au/geonetwork/srv/api"


def get_token() -> str:
    """
    Obtains eCat XRSF token.

    Returns:
        str: A string containing 'XSRF-TOKEN'.
    """
    logger.info(f"Getting eCat {ENV} token...")
    response = requests.post(f"{ECAT_BASE_URL}/me")

    xsrf_token = response.cookies["XSRF-TOKEN"]
    if not xsrf_token:
        logger.exception("Error: XSRF-TOKEN not found in response cookies.")
        raise Exception("Error: XSRF-TOKEN not found in response cookies.")

    logger.info(f"Got XSRF-TOKEN from eCat {ENV} API.")

    return xsrf_token


def create_record() -> Tuple[str, str]:
    """
    Create record in ecat.

    This function sends a PUT request to ecat with XML data read from a local file.

    Returns:
        Tuple[str, str]: A tuple containing the metadata_id id and UUID of the created ecat record.

    """
    xsrf_token = get_token()
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/xml",
        "X-XSRF-TOKEN": xsrf_token,
        "Cookie": f"XSRF-TOKEN={xsrf_token}",
    }
    params = {
        "metadataType": "METADATA",
        "transformWith": "_none_",  # "schema:iso19115-3.2018:convert/fromISO19115-3.2014",
    }
    with open("ga-19115-3-dataset.xml", "rb") as ecat_xml:
        payload = ecat_xml.read()
    logger.info(f"Creating ecat {ENV} record...")
    response = requests.put(
        f"{ECAT_BASE_URL}/records",
        headers=headers,
        params=params,
        data=payload,
        auth=(ECAT_USERNAME, ECAT_PASSWORD),
    )
    if response.status_code != 201:
        logger.exception(
            f"Error Status: {response.status_code} \n Error details: {response.content}"
        )
        raise Exception(
            f"Error Status: {response.status_code} \n Error details: {response.content}"
        )

    response_json = json.loads(response.content)
    metadata_id = next(iter(response_json["metadataInfos"]))
    uuid = response_json["metadataInfos"][metadata_id][0]["uuid"]
    logger.info(
        f"Created ecat {ENV} record with metadata_id: {metadata_id} and UUID: {uuid}"
    )

    return metadata_id, uuid


def main() -> None:
    try:
        create_record()
    except Exception as e:
        logger.exception(f"Exception from main: {e}")

    return None


if __name__ == "__main__":
    main()

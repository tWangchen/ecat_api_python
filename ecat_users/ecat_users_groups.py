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
file_handler = logging.FileHandler("ecat_users_groups.log")
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
    logger.info(f"Getting eCat token...")
    response = requests.post(f"{ECAT_BASE_URL}/me")

    xsrf_token = response.cookies["XSRF-TOKEN"]
    if not xsrf_token:
        logger.exception("Error: XSRF-TOKEN not found in response cookies.")
        raise Exception("Error: XSRF-TOKEN not found in response cookies.")

    logger.info(f"Got XSRF-TOKEN from eCat API: {xsrf_token}.")

    return xsrf_token


def get_user_groups() -> str:
    """
    Retrieve all user groups.

    Returns:
        str: A JSON object representing user groups.
    """
    xsrf_token = get_token()
    headers = {
        "Accept": "application/json",
        "X-XSRF-TOKEN": xsrf_token,
    }

    logger.info(f"Getting eCat users groups...")
    response = requests.get(
        f"{ECAT_BASE_URL}/users/groups",
        headers=headers,
        auth=(ECAT_USERNAME, ECAT_PASSWORD),
    )
    if response.status_code != 200:
        logger.exception(
            f"Error Status: {response.status_code} \n Error details: {response.content}"
        )
        raise Exception(
            f"Error Status: {response.status_code} \n Error details: {response.content}"
        )

    response_json = json.loads(response.content)
    logger.info(f"users_groups: {response_json}")

    return response_json


def main() -> None:
    try:
        get_user_groups()
    except Exception as e:
        logger.exception(f"Exception from main: {e}")

    return None


if __name__ == "__main__":
    main()

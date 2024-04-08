import json
import logging
import os
from typing import Tuple

import requests

# Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s: %(levelname)s:%(name)s: %(message)s")
file_handler = logging.FileHandler("ecat_reindex.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# If you want to substitute from Terraform, Packer, CodeDeploy using sed, then
# use placeholder values specified after each "or" operators
ECAT_ADMIN_USERNAME = os.environ.get("ECAT_ADMIN_USERNAME") or "ecat_admin_username_val"
ECAT_ADMIN_PASSWORD = os.environ.get("ECAT_ADMIN_PASSWORD") or "ecat_admin_password_val"

# Optional, use this to target specific eCat environment
# Example test2.ecat
ECAT_ENV = os.environ.get("ECAT_ENV")
# Defaults to localhost if ECAT_ENV not specified
ECAT_BASE_URL = "http://localhost:8080/geonetwork/srv/api"
if ECAT_ENV:
    ECAT_BASE_URL = f"https://{ECAT_ENV}.ga.gov.au/geonetwork/srv/api"


def get_auth_headers() -> Tuple[str, str]:
    """
    Obtains eCat api authentication headers.
    Returns tuple: XSRF-TOKEN and Set-Cookie
    """
    headers = {"Accept": "application/json"}
    logger.info(f"Getting your token and cookies from eCat API...")
    response = requests.get(
        f"{ECAT_BASE_URL}/me",
        headers=headers,
        auth=(ECAT_ADMIN_USERNAME, ECAT_ADMIN_PASSWORD),
    )
    if response.status_code != 200:
        logger.exception(f"Error auth with eCat API. Status: {response.status_code}")
        raise Exception(f"Error auth with eCat API. Status: {response.status_code}")

    xsrf_token = response.cookies["XSRF-TOKEN"]
    logger.info(f"Got your XSRF-TOKEN from eCat API.")

    set_cookie = response.headers["Set-Cookie"]
    logger.info(f"Got your Header Set  from eCat API.")

    return xsrf_token, set_cookie


def reindex() -> None:
    xsrf_token, set_cookie = get_auth_headers()
    headers = {
        "Accept": "application/json",
        "X-XSRF-TOKEN": xsrf_token,
        "Cookie": set_cookie,
    }
    # Ensure payload reflects requirements
    payload = json.dumps({"reset": False, "indices": "records", "asynchronous": True})
    logger.info(f"Reindexing eCat...")
    response = requests.put(
        f"{ECAT_BASE_URL}/site/index",
        headers=headers,
        data=payload,
        auth=(ECAT_ADMIN_USERNAME, ECAT_ADMIN_PASSWORD),
    )
    if response.status_code != 200:
        logger.exception(f"Error re-indexing eCat. Status: {response.status_code}")
        raise Exception(f"Error re-indexing eCat. Status: {response.status_code}")

    logger.info(f"Reindexed eCat. Status: {response.status_code}")
    return None


def main() -> None:
    try:
        reindex()
    except Exception as e:
        logger.exception(f"Error calling reindex: {e}")
    return None


if __name__ == "__main__":
    main()

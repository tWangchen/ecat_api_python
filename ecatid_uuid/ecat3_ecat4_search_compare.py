import json

import requests

ECATID = 141436


def search_ecat3(ECATID) -> None:

    ecat3_qsearch_ep = f"https://ecat.ga.gov.au/geonetwork/srv/eng/q?resultType=details&fast=index&_content_type=json&uuid={ECATID}"
    ecat3_response = requests.get(ecat3_qsearch_ep)
    if ecat3_response.status_code != 200:
        raise Exception(f"Error status: {ecat3_response.status_code}")

    ecat3_response_json = ecat3_response.json()

    # eCat3 response path mdSatatus
    eCat3_mdStatus = ecat3_response_json["metadata"]["mdStatus"]
    print(f"eCat3_mdStatus: {eCat3_mdStatus}")

    # eCat3 response path owner
    eCat3_owner = ecat3_response_json["metadata"]["owner"]
    print(f"eCat3_owner: {eCat3_owner}")

    # eCat3 response path recordOwner
    eCat3_recordOwner = ecat3_response_json["metadata"]["recordOwner"]
    print(f"eCat3_recordOwner: {eCat3_recordOwner}")


def search_ecat4(ECATID) -> None:
    headers = {"Content-Type": "application/json"}
    search_payload = json.dumps(
        {"query": {"query_string": {"query": f"(eCatId:{ECATID})"}}}
    )

    ecat4_underscore_search_ep = (
        "https://dev.ecat.ga.gov.au/geonetwork/srv/api/search/records/_search"
    )
    ecat4_response = requests.post(
        ecat4_underscore_search_ep, headers=headers, data=search_payload
    )
    if ecat4_response.status_code != 200:
        raise Exception(f"Error status: {ecat4_response.status_code}")

    ecat4_response_json = ecat4_response.json()

    # eCat3 response path mdStatus
    eCat4_mdstatus = ecat4_response_json["hits"]["hits"][0]["_source"]["mdStatus"]
    print(f"\neCat4_mdstatus: {eCat4_mdstatus}")

    # eCat3 response path owner
    eCat4_owner = ecat4_response_json["hits"]["hits"][0]["_source"]["owner"]
    print(f"eCat4_owner: {eCat4_owner}")

    # eCat3 response path recordOwner
    eCat4_recordOwner = ecat4_response_json["hits"]["hits"][0]["_source"]["recordOwner"]
    print(f"eCat4_recordOwner: {eCat4_recordOwner}")


def main() -> None:
    print(f"Compare ecat3 vs ecat4 response for eCatId: {ECATID}\n")
    search_ecat3(ECATID=ECATID)
    search_ecat4(ECATID=ECATID)


if __name__ == "__main__":
    main()

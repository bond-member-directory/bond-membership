import csv

import requests
from settings import (
    SALESFORCE_AUTH_URL,
    SALESFORCE_CLIENT_ID,
    SALESFORCE_CLIENT_SECRET,
    SALESFORCE_OUTPUT,
    SALESFORCE_PASSWORD,
    SALESFORCE_USERNAME,
)
from simple_salesforce import Salesforce, format_soql

FIELDS_TO_FETCH = [
    "Id",
    "Name",
    "Charity_Commission_number__c",
    "Website",
    "Registration_number__c",
    "Year_joined__c",
    "Membership_type__c",
    "Organisation_Size__c",
    "Membership_Band__c",
]
MEMBERSHIP_STATUS = ["Member", "Renewal", "Lapsed", "Provisional"]
IDS_TO_EXCLUDE = ["0014000000suyW6AAI"]
SALESFORCE_QUERY = f"""
SELECT {", ".join(FIELDS_TO_FETCH)}
FROM Account
WHERE Membership_status__c IN {{membership_status}}
    AND Id NOT IN {{ids_to_exclude}}
"""


def get_salesforce_instance():
    response = requests.post(
        SALESFORCE_AUTH_URL,
        data={
            "client_secret": SALESFORCE_CLIENT_SECRET,
            "client_id": SALESFORCE_CLIENT_ID,
            "grant_type": "password",
            "username": SALESFORCE_USERNAME,
            "password": SALESFORCE_PASSWORD,
        },
    ).json()
    return Salesforce(
        instance_url=response["instance_url"],
        session_id=response["access_token"],
    )


def fetch_data(sf):
    data = sf.query_all(
        format_soql(
            SALESFORCE_QUERY,
            membership_status=MEMBERSHIP_STATUS,
            ids_to_exclude=IDS_TO_EXCLUDE,
        )
    )
    print(f"{data['totalSize']:,.0f} members found")
    return {row["Id"]: row for row in data["records"]}


if __name__ == "__main__":

    sf = get_salesforce_instance()
    records = fetch_data(sf)

    with open(SALESFORCE_OUTPUT, "w", encoding="utf8") as a:
        writer = csv.DictWriter(a, fieldnames=FIELDS_TO_FETCH, lineterminator="\n")
        writer.writeheader()
        for row in records.values():
            writer.writerow({f: row.get(f) for f in FIELDS_TO_FETCH})

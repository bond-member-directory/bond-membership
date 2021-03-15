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
from utils import to_dotted

FIELDS_TO_FETCH = [
    "Id",
    "Name",
    "Charity_Commission_number__c",
    "Website",
    "Registration_number__c",
    "Year_joined__c",
    "Membership_type__c",
    "Membership_Band__c",
    "Logo_url__c",
    "Current_Membership__r.No_poverty__c",
    "Current_Membership__r.Zero_hunger__c",
    "Current_Membership__r.Good_health_and_wellbeing__c",
    "Current_Membership__r.Quality_education__c",
    "Current_Membership__r.Gender_equality__c",
    "Current_Membership__r.Clean_water_and_sanitation__c",
    "Current_Membership__r.Affordable_and_clean_energy__c",
    "Current_Membership__r.Decent_work_and_economic_growth__c",
    "Current_Membership__r.Industry_innovation_and_infrastructure__c",
    "Current_Membership__r.Reduced_inequalities__c",
    "Current_Membership__r.Sustainable_cities_and_communities__c",
    "Current_Membership__r.Responsible_consumption_and_production__c",
    "Current_Membership__r.Climate_action__c",
    "Current_Membership__r.Life_below_water__c",
    "Current_Membership__r.Life_on_land__c",
    "Current_Membership__r.Peace_justice_and_strong_institutions__c",
    "Current_Membership__r.Partnerships_for_the_goals__c",
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
        fieldnames = [f.split(".")[-1] for f in FIELDS_TO_FETCH]
        writer = csv.DictWriter(a, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in records.values():
            row = dict(to_dotted(row))
            writer.writerow({f.split(".")[-1]: row.get(f) for f in FIELDS_TO_FETCH})

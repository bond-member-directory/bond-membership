import base64
import html

import requests
from settings import (
    SALESFORCE_AUTH_URL,
    SALESFORCE_AUTHENTICATION_METHOD,
    SALESFORCE_CLIENT_ID,
    SALESFORCE_CLIENT_SECRET,
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
    "Primary_contact_email__c",
    "Members_directory_contact_email__c",
    "Hide_email_on_members_directory__c",
    "Remove_from_member_directory__c",
    "Description",
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
    payload = {
        "grant_type": "client_credentials",
        "client_id": SALESFORCE_CLIENT_ID,
        "client_secret": SALESFORCE_CLIENT_SECRET,
    }
    if SALESFORCE_AUTHENTICATION_METHOD == "password":
        payload = {
            "grant_type": "password",
            "client_id": SALESFORCE_CLIENT_ID,
            "client_secret": SALESFORCE_CLIENT_SECRET,
            "username": SALESFORCE_USERNAME,
            "password": SALESFORCE_PASSWORD,
        }

    r = requests.post(
        SALESFORCE_AUTH_URL,
        data=payload,
    )
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Error: {r.text}")
        raise e
    response = r.json()
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

    for row in data["records"]:
        if row.get("Members_directory_contact_email__c") and not row.get(
            "Hide_email_on_members_directory__c"
        ):
            row["Primary_contact_email__c"] = base64.b64encode(
                html.escape(row["Members_directory_contact_email__c"]).encode("utf8")
            ).decode("utf8")
        elif row.get("Primary_contact_email__c") and not row.get(
            "Hide_email_on_members_directory__c"
        ):
            row["Primary_contact_email__c"] = base64.b64encode(
                html.escape(row["Primary_contact_email__c"]).encode("utf8")
            ).decode("utf8")
        else:
            row["Primary_contact_email__c"] = None
        yield row["Id"], row

import csv
import io
import json

import requests
from settings import (
    CHARITYBASE_API_KEY,
    CHARITYBASE_URL,
    FINAL_OUTPUT,
    GSS_LOOKUP_CSV,
    SALESFORCE_OUTPUT,
    SDGS_INPUT,
)
from tqdm import tqdm
from utils import clean_object

CHARITYBASE_HEADERS = {
    "Authorization": f"Apikey {CHARITYBASE_API_KEY}",
    "Content-Type": "application/json",
}
GRAPH_QL_QUERY = r"""
query($ids: [ID]){
  CHC {
    getCharities(filters: {id:$ids}){
      list {
        id,
        image {
          logo {
            medium
          }
        },
        areas {
          id
          name
        }
      }
    }
  }
}
"""
SDG_NAMES = {
    "No poverty": "01",
    "Zero hunger": "02",
    "Good health and wellbeing": "03",
    "Quality education": "04",
    "Gender equality": "05",
    "Clean water and sanitation": "06",
    "Affordable and clean energy": "07",
    "Decent work and economic growth": "08",
    "Industry, innovation and infrastructure": "09",
    "Reduced inequalities": "10",
    "Sustainable cities and communities": "11",
    "Responsible consumption and production": "12",
    "Climate action": "13",
    "Life below water": "14",
    "Life on land": "15",
    "Peace, justice and strong institutions": "16",
    "Partnerships for the goals": "17",
}


def split_list(input_list, n=10):
    return [input_list[i : i + n] for i in range(0, len(input_list), n)]


def get_member_data():
    with open(SALESFORCE_OUTPUT, encoding="utf8") as a:
        reader = csv.DictReader(a)
        return {row["Id"]: row for row in reader}


def get_charity_numbers(members):
    return [
        row["Charity_Commission_number__c"]
        for k, row in members.items()
        if row["Charity_Commission_number__c"]
    ]


def get_iso_lookup():
    response = requests.get(GSS_LOOKUP_CSV)
    lines = (line.decode("utf-8") for line in response.iter_lines())
    reader = csv.DictReader(lines)
    return {row["key"]: row["ISO3166-1"] for row in reader if row["ISO3166-1"]}


def get_charitybase_data(charity_numbers, iso_lookup):
    results = {}
    with tqdm(total=len(charity_numbers)) as pbar:
        for chunk in split_list(charity_numbers):
            res = requests.post(
                CHARITYBASE_URL,
                headers=CHARITYBASE_HEADERS,
                json={"query": GRAPH_QL_QUERY, "variables": {"ids": chunk}},
            )
            res.raise_for_status()
            result = res.json()
            for charity in result["data"]["CHC"]["getCharities"]["list"]:
                results[charity["id"]] = {
                    "logoUrl": charity.get("image", {}).get("logo", {}).get("medium")
                    if charity.get("image")
                    else None,
                    "countries": list(
                        set(
                            iso_lookup[a["id"]]
                            for a in charity.get("areas", [])
                            if a["id"] in iso_lookup
                        )
                    ),
                }
            pbar.update(len(chunk))
    return results


def fetch_sdgs():
    sdgs = {}
    with open(SDGS_INPUT, encoding="latin1") as a:
        reader = csv.DictReader(a)
        for row in reader:
            sdgs[row["Organisation Name"]] = [
                code for name, code in SDG_NAMES.items() if int(row[name]) == 1
            ]
    return sdgs


if __name__ == "__main__":
    sdgs = fetch_sdgs()
    iso_lookup = get_iso_lookup()
    members = get_member_data()
    charity_numbers = get_charity_numbers(members)
    charity_data = get_charitybase_data(charity_numbers, iso_lookup)

    for k, m in members.items():
        charity = charity_data.get(
            m["Charity_Commission_number__c"],
            {
                "logoUrl": None,
                "countries": [],
            },
        )
        members[k] = {**clean_object(m), **charity, "sdgs": sdgs.get(m["Name"], [])}

    with open(FINAL_OUTPUT, "w", encoding="utf8") as a:
        json.dump(
            {
                "members": members,
                "sdgs": dict(zip(SDG_NAMES.values(), SDG_NAMES.keys())),
            },
            a,
            indent=4,
        )

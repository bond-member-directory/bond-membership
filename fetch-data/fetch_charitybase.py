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
        },
        activities,
        finances {
          income
          financialYear {
            end
          }
        }
      }
    }
  }
}
"""


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
                    "logourl": charity.get("image", {}).get("logo", {}).get("medium")
                    if charity.get("image")
                    else None,
                    "countries": sorted(
                        set(
                            iso_lookup[a["id"]]
                            for a in charity.get("areas", [])
                            if a["id"] in iso_lookup
                        )
                    ),
                    "activities": charity.get("activities", ""),
                    "latest_income": None,
                    "latest_fye": None,
                }
                if charity.get("finances", []):
                    results[charity["id"]]["latest_income"] = charity.get("finances", [{}])[0].get("income")
                    results[charity["id"]]["latest_fye"] = charity.get("finances", [{}])[0].get("financialYear", {}).get("end")
            pbar.update(len(chunk))
    return results


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
                "logourl": None,
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

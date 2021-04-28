import json

import click
from fetch_charitybase import (
    clean_object,
    get_charity_numbers,
    get_charitybase_data,
    get_iso_lookup,
)
from fetch_salesforce import fetch_data, get_salesforce_instance
from settings import FINAL_OUTPUT
from sdgs import clean_sdgs, SDG_NAMES


@click.command()
@click.option('--output', default=FINAL_OUTPUT, show_default=True)
def main(output):
    click.echo("Fetching data from salesforce")
    sf = get_salesforce_instance()
    members = dict(fetch_data(sf))
    click.echo(f"Fetched {len(members):,.0f} records from salesforce")

    click.echo("Clean SDG data")
    members = dict(clean_sdgs(members))
    click.echo("Get Charity Commission key -> ISO country code lookups")
    iso_lookup = get_iso_lookup()
    click.echo("Extract charity numbers to fetch")
    charity_numbers = get_charity_numbers(members)
    click.echo(f"Fetching data on {len(charity_numbers):,.0f} charities from CharityBase")
    charity_data = get_charitybase_data(charity_numbers, iso_lookup)
    click.echo(f"Fetched data on {len(charity_data):,.0f} charities from CharityBase")

    click.echo("Add charity data to member data")
    members_for_site = {}
    for k, m in members.items():
        charity = charity_data.get(
            m["Charity_Commission_number__c"],
            {
                "logourl": None,
                "activities": None,
                "countries": [],
            },
        )
        members_for_site[k] = {**charity, **clean_object(m)}

    click.echo("Write data to output file")
    with open(output, "w", encoding="utf8") as a:
        json.dump(
            {
                "members": members_for_site,
                "sdgs": dict(zip(SDG_NAMES.values(), SDG_NAMES.keys())),
            },
            a,
            indent=4,
        )
        click.echo(f"Data written to `{output}`")

if __name__ == '__main__':
    main()

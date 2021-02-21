import json

import click
from fetch_charitybase import (
    SDG_NAMES,
    clean_object,
    fetch_sdgs,
    get_charity_numbers,
    get_charitybase_data,
    get_iso_lookup,
)
from fetch_salesforce import fetch_data, get_salesforce_instance
from settings import FINAL_OUTPUT


@click.command()
@click.option('--output', default=FINAL_OUTPUT, show_default=True)
def main(output):
    click.echo("Fetching data from salesforce")
    sf = get_salesforce_instance()
    members = fetch_data(sf)
    click.echo(f"Fetched {len(members):,.0f} records from salesforce")

    click.echo("Import data on SDGs")
    sdgs = fetch_sdgs()
    click.echo("Get Charity Commission key -> ISO country code lookups")
    iso_lookup = get_iso_lookup()
    click.echo("Extract charity numbers to fetch")
    charity_numbers = get_charity_numbers(members)
    click.echo(f"Fetching data on {len(charity_numbers):,.0f} charities from CharityBase")
    charity_data = get_charitybase_data(charity_numbers, iso_lookup)
    click.echo(f"Fetched data on {len(charity_data):,.0f} charities from CharityBase")

    click.echo("Add charity data to member data")
    for k, m in members.items():
        charity = charity_data.get(
            m["Charity_Commission_number__c"],
            {
                "logoUrl": None,
                "countries": [],
            },
        )
        members[k] = {**clean_object(m), **charity, "sdgs": sdgs.get(m["Name"], [])}

    click.echo("Write data to output file")
    with open(output, "w", encoding="utf8") as a:
        json.dump(
            {
                "members": members,
                "sdgs": dict(zip(SDG_NAMES.values(), SDG_NAMES.keys())),
            },
            a,
            indent=4,
        )
        click.echo(f"Data written to `{output}`")

if __name__ == '__main__':
    main()

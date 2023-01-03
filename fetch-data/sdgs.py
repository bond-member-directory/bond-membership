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


def clean_sdgs(members):

    sdg_fields = {
        k.replace(" ", "_").replace(",", "") + "__c": v for k, v in SDG_NAMES.items()
    }

    for member_id, row in members.items():
        row["sdgs"] = []
        if row["Current_Membership__r"]:
            for field_name, value in row["Current_Membership__r"].items():
                if field_name != "attributes" and value:
                    row["sdgs"].append(sdg_fields[field_name])
        del row["Current_Membership__r"]
        yield (member_id, row)

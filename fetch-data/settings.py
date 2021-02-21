import os

from dotenv import load_dotenv

load_dotenv()

# Salesforce settings
SALESFORCE_AUTH_URL = os.environ.get(
    "SALESFORCE_AUTH_URL", "https://login.salesforce.com/services/oauth2/token"
)
SALESFORCE_CLIENT_SECRET = os.environ["SALESFORCE_CONSUMER_SECRET"]
SALESFORCE_CLIENT_ID = os.environ["SALESFORCE_CONSUMER_KEY"]
SALESFORCE_USERNAME = os.environ["SALESFORCE_USERNAME"]
SALESFORCE_PASSWORD = os.environ["SALESFORCE_PASSWORD"]

# Charitybase settings
CHARITYBASE_URL = os.environ.get(
    "CHARITYBASE_URL", "https://charitybase.uk/api/graphql"
)
CHARITYBASE_API_KEY = os.environ["CHARITYBASE_API_KEY"]

# Charity Commission GSS Lookup URL
GSS_LOOKUP_CSV = os.environ.get(
    "GSS_LOOKUP_CSV",
    "https://raw.githubusercontent.com/drkane/charity-lookups/master/cc-aoo-gss-iso.csv",
)

# Input files
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
SDGS_INPUT = os.path.join(SCRIPT_DIR, "..", "source-data", "SDGs.csv")

# output files
SALESFORCE_OUTPUT = os.path.join(SCRIPT_DIR, "..", "source-data", "members.csv")
FINAL_OUTPUT = os.path.join(SCRIPT_DIR, "..", "src", "assets", "bond_members.json")

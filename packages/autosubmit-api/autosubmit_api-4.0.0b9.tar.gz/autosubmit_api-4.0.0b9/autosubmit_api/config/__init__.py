import os
from dotenv import load_dotenv

load_dotenv()

# Auth
PROTECTION_LEVEL = os.environ.get("PROTECTION_LEVEL")
# WARNING: Always provide a SECRET_KEY for production
JWT_SECRET = os.environ.get(
    "SECRET_KEY", "M87;Z$,o5?MSC(/@#-LbzgE3PH-5ki.ZvS}N.s09v>I#v8I'00THrA-:ykh3HX?"
)
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 84000 * 5  # 5 days

# CAS Stuff
CAS_SERVER_URL = os.environ.get("CAS_SERVER_URL")
# e.g: 'https://cas.bsc.es/cas/login'
CAS_LOGIN_URL = os.environ.get(
    "CAS_LOGIN_URL", (CAS_SERVER_URL + "login") if CAS_SERVER_URL else ""
)
# e.g: 'https://cas.bsc.es/cas/serviceValidate'
CAS_VERIFY_URL = os.environ.get(
    "CAS_VERIFY_URL", (CAS_SERVER_URL + "serviceValidate") if CAS_SERVER_URL else ""
)

# GitHub Oauth App

GITHUB_OAUTH_CLIENT_ID = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
GITHUB_OAUTH_CLIENT_SECRET = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")
GITHUB_OAUTH_WHITELIST_ORGANIZATION = os.environ.get("GITHUB_OAUTH_WHITELIST_ORGANIZATION")
GITHUB_OAUTH_WHITELIST_TEAM = os.environ.get("GITHUB_OAUTH_WHITELIST_TEAM")

# Startup options
RUN_BACKGROUND_TASKS_ON_START = os.environ.get("RUN_BACKGROUND_TASKS_ON_START") in [
    "True",
    "T",
    "true",
]  # Default false

DISABLE_BACKGROUND_TASKS = os.environ.get("DISABLE_BACKGROUND_TASKS") in [
    "True",
    "T",
    "true",
]  # Default false

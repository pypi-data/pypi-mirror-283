import requests
import os
import urllib3
from pprint import pprint
import json
import requests
import os
import sys
import datetime
import tempfile
import pynetbox
import urllib3
import datetime
from awx.awx_common import awx_get_id
from awx.awx_common import getawxdata
from awx.awx_credential import awx_create_credential
from common import prettyllog
from awx.awx_organisation import awx_create_organization
from awx.awx_project import awx_create_project
from awx.awx_project import awx_get_project

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
VERIFY_SSL = False
ansibletoken = os.getenv("ANSIBLE_TOKEN")

def default_secrets():
    return {
        "client_id": os.getenv("AAP_CLIENT_ID"),
        "client_secret": os.getenv("AAP_CLIENT_SECRET"),
        "username": os.getenv("AAP_USERNAME"),
        "password": os.getenv("AAP_PASSWORD"),
        "aaphost": os.getenv("AAP_HOST"),
        "aaptoken": os.getenv("AAP_TOKEN"),
    }

secrets = default_secrets()


def awx_get_organization(orgid, mytoken=None, r=None):
  headers = {"User-agent": "python-awx-client", "Content-Type": "application/json","Authorization": "Bearer {}".format(ansibletoken)}
  url = os.getenv("IGN8_AAP_HOST") + "/api/v2/organizations/%s" % orgid
  resp = requests.get(url,headers=headers, verify=VERIFY_SSL)
  return   json.loads(resp.content)

def aap_organisations():
    url = secrets["aaphost"] + "
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    data = {
        "client_id": secrets["client_id"],
        "client_secret": secrets["client_secret"],
        "username": secrets["username"],
        "password": secrets["password"],
    }
    response = requests.post(url, headers=headers, json=data, verify=False)
    return response.json()



def status():
    #We need to create an ascii menu that shows the status of the AAP
    #We need to show the status of the AAP

    print("AAP Status")
    print("==========")
    print("Checking AAP Status")
    print("Please wait...")
    print(default_secrets())
    print("....")



    
import requests
from requests.auth import HTTPBasicAuth
import json
import os
import sys
from dotenv import load_dotenv

def getallProject():
    global headers, baseurl, auth
    url = f'{baseurl}/rest/api/3/project'
    response = requests.request(
        "GET",
        url,
        headers=headers,
        auth=auth
    )
    projects = response.json() if response.status_code==200 else []
    for project in projects:
        getProjectIssues(project)
    
    #print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
def getProjectIssues(project):
    '''Get all the issues in the project and return json object'''
    global baseurl, auth, headers
    key = project['key']
    query = {
        "jql": f'project = "{key}" ORDER BY created ASC',
        "maxResults": 1000,
        "startAt": 0
    }
    url = f"{baseurl}/rest/api/3/search/jql"
    response = requests.request("GET", url, headers=headers, auth=auth, params=query)
    response = response.json()
    all_issues = []
    print(response)
    #print(f"Total issues: {len(all_issues)}")
    # Optional: pretty print
    # print(json.dumps(all_issues, indent=4))
    for id in response['issues']:
        url = f"{baseurl}/rest/api/3/issue/{id['id']}"
        resp = requests.request(
            "GET",
            headers=headers,
            auth=auth,
            url=url
        )
        all_issues.append(resp.json())
    return all_issues
    return response.json()  # json.loads(response.text)
def createJiraTickets(command):
    pass

def issuePicker(issue):
    global headers, baseurl, auth
    url = f'{baseurl}/rest/api/3/issue/{issue}'
    response = requests.request(
        "GET",
        url,
        headers=headers,
        auth=auth
    )
    print(response.status_code)

if __name__ == "__main__":
    if ".env" not in os.listdir():
        print(".env doesn't exist. Please check if you're running from same location as .env or create a env with following config:\n APITOKEN=<TOKEN>\nbaseURL=<baseurl>\nemail=<your email>") 
        sys.exit(1)
    load_dotenv()
    api_token = os.getenv("APITOKEN")
    baseurl= os.getenv("baseURL")
    email = os.getenv("email")

    auth = HTTPBasicAuth(email, api_token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    with open('command.json', 'r') as file:
        command = json.load(file)
    print(command)
    #createJiraTickets(command)


    

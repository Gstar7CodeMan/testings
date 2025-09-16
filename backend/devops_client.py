import requests
from requests.auth import HTTPBasicAuth

class AzureDevOpsClient:
    def __init__(self, org_url, project, repo, pat):
        self.base_url = f"{org_url}/{project}/_apis/git/repositories/{repo}"
        self.auth = HTTPBasicAuth("", pat)
        self.headers = {"Content-Type": "application/json"}

    def get_all_branches(self):
        branches, token = [], None
        while True:
            url = f"{self.base_url}/refs?filter=heads/&api-version=7.0&$top=100"
            headers = self.headers.copy()
            if token:
                headers["x-ms-continuationtoken"] = token
            r = requests.get(url, auth=self.auth, headers=headers)
            if not r.ok: break
            branches += r.json().get("value", [])
            token = r.headers.get("x-ms-continuationtoken")
            if not token: break
        return branches

    def get_branch_commit_date(self, branch_name):
        url = f"{self.base_url}/commits?searchCriteria.itemVersion.version={branch_name}&$top=1&api-version=7.0"
        r = requests.get(url, auth=self.auth, headers=self.headers)
        if r.ok and r.json()["value"]:
            return r.json()["value"][0]["committer"]["date"]
        return None

    def delete_branch(self, branch_name):
        ref = f"refs/heads/{branch_name}"
        url = f"{self.base_url}/refs?api-version=7.0"
        data = [{
            "name": ref,
            "oldObjectId": "0000000000000000000000000000000000000000",
            "newObjectId": "0000000000000000000000000000000000000000"
        }]
        r = requests.post(url, json=data, auth=self.auth, headers=self.headers)
        return r.ok

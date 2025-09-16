import pandas as pd
from datetime import datetime
from devops_client import AzureDevOpsClient

def generate_reports(config):
    client = AzureDevOpsClient(**config)
    branches = client.get_all_branches()
    cutoff = datetime.strptime(config["cutoff_date"], "%Y-%m-%d")

    all_data, stale_data = [], []
    for b in branches:
        name = b["name"].replace("refs/heads/", "")
        commit_date_str = client.get_branch_commit_date(name)
        if commit_date_str:
            commit_date = datetime.strptime(commit_date_str, "%Y-%m-%dT%H:%M:%SZ")
            all_data.append({"Branch": name, "Last Commit": commit_date})
            if commit_date < cutoff:
                stale_data.append({"Branch": name, "Last Commit": commit_date})

    df_all = pd.DataFrame(all_data)
    df_stale = pd.DataFrame(stale_data)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    all_file = f"all_branches_{timestamp}.xlsx"
    stale_file = f"stale_branches_{timestamp}.xlsx"

    df_all.to_excel(all_file, index=False)
    df_stale.to_excel(stale_file, index=False)

    return {
        "total": len(df_all),
        "stale": len(df_stale),
        "files": [all_file, stale_file]
    }

def delete_stale(config):
    client = AzureDevOpsClient(**config)
    branches = client.get_all_branches()
    cutoff = datetime.strptime(config["cutoff_date"], "%Y-%m-%d")

    deleted = []
    for b in branches:
        name = b["name"].replace("refs/heads/", "")
        commit_date_str = client.get_branch_commit_date(name)
        if commit_date_str:
            commit_date = datetime.strptime(commit_date_str, "%Y-%m-%dT%H:%M:%SZ")
            if commit_date < cutoff and client.delete_branch(name):
                deleted.append(name)
    return deleted

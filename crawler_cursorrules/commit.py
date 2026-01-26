import requests
import os
import sqlite3
import time
import itertools

with open("/mnt/d/1stp_cursor/crawlerV2.0/tokens.txt", "r") as f:
    tokens = [line.strip() for line in f.readlines() if line.strip()]

token_cycle = itertools.cycle(tokens)
token_usage_count = {token: 0 for token in tokens}
MAX_USAGE_PER_TOKEN = 9


GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

def get_headers():
    global token_cycle

    for _ in range(len(tokens)):
        token = next(token_cycle)
        if token_usage_count[token] < MAX_USAGE_PER_TOKEN:  
            token_usage_count[token] += 1
            return {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    
    print("All tokens have been used, get into sleep and wait for reset...")
    time.sleep(3600)
    token_usage_count.clear()
    return get_headers()

def create_tables(conn):
    cursor = conn.cursor()

    # Create table 'repos'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS repos (
            repo_full_name TEXT PRIMARY KEY,
            repo_name TEXT NOT NULL,
            repo_owner TEXT NOT NULL,
            repo_owner_id INTEGER NOT NULL,
            repo_created_at TEXT,
            repo_last_updated TEXT,
            repo_size INTEGER,
            repo_starts INTEGER,
            repo_watchers INTEGER,
            repo_forks INTEGER,
            repo_open_issues INTEGER,
            repo_contributors INTEGER,
            repo_releases INTEGER,
            repo_prs INTEGER,
            repo_commits INTEGER,
            repo_functions TEXT,
            repo_functions_count INTEGER,
            repo_languages TEXT,
            repo_description TEXT,
            repo_topics TEXT
        )
    ''')
    conn.commit()

# Save path
save_path = "/mnt/d/1stp_cursor/crawlerV2.0/save_files"
if not os.path.exists(save_path):
    os.makedirs(save_path)
 
# -github.com/search?q=awesome-cursorrules&type=repositories
def get_repo(conn, per_page, page):
    query = "awesome-cursorrules in:name"
    params = {"q": query, "per_page": per_page, "page": page}
    url = "https://api.github.com/search/repositories"
    repo_response = requests.get(url, headers=headers, params=params)
    
    if repo_response.status_code != 200:
        print("Error:", repo_response.status_code, repo_response.text)
        return []
    
    repo_data = repo_response.json()
    if "items" not in repo_data:
        print("Error: No 'items' found in repository response")
        return []
    
    # print(f"\n\n{repo_data}\n\n")
    
    for repo in repo_data["items"]:
        repo_functions = []
        repo_name = repo["name"]
        repo_fullname = repo["full_name"]
        repo_created_at = repo["created_at"]
        repo_updated_at = repo["updated_at"]
        repo_size = repo["size"]
        repo_stars = repo["stargazers_count"]
        repo_watchers = repo["watchers_count"]
        repo_forks = repo["forks_count"]
        repo_open_issues = repo["open_issues_count"]
        repo_owner = repo["owner"]["login"]
        repo_wiki = "wiki" if repo["has_wiki"] else None
        repo_discussion = "discussion" if repo["has_discussions"] else None
        repo_license = "license" if repo["license"] else None
        repo_language = get_repo_languages(repo_owner, repo_name)
        repo_contributors_url = repo["contributors_url"]
        repo_releases_url = repo["releases_url"]
        repo_pr_url = repo["pulls_url"]
        repo_commits_url = repo["commits_url"]
        repo_default_branch = repo["default_branch"]
        repo_description = repo["description"]
        repo_topics = repo["topics"]
        
        
        # Round 2
        if repo_wiki:
            repo_functions.append("wiki")
        if repo_discussion:
            repo_functions.append("discussion")
        if repo_license:
            repo_functions.append("license")
        if has_readme(repo_fullname):
            repo_functions.append("readme")
        
        repo_functions_count = len(repo_functions)
        
        metrics = get_metric_count_graphql(repo_owner, repo_name)
        repo_releases = metrics["releases"]
        repo_contributors = metrics["contributors"]
        repo_pr = metrics["pull_requests"]
        repo_commits = metrics["commits"]
        
        download_repo_zip(repo_fullname, repo_default_branch)
        ### save to SQLite**
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO commits (file_hash, commit_num, first_commit_time, last_commit_time, commit_times, commit_changes, contributors, contributor_num, creator_id, creator_commit_num, creator_last_activity, creator_star, creator_fork, creator_follower, creator_created_at, creator_repo_num)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (file_hash, commit_num, first_commit_time, last_commit_time, ",".join(commit_times), ",".join(commit_changes), ",".join(contributors), contributor_num, creator_id, creator_commit_num, creator_last_activity, creator_star, creator_fork, creator_follower, creator_created_at, creator_repo_num)
        )
        conn.commit()
        
        '''
        print(f"Get metadata from {repo_fullname}:\n")
        print(f"#01. repo_fullname: {repo_fullname}\n")
        print(f"#02. repo_created_at: {repo_created_at}\n")
        print(f"#03. repo_updated_at: {repo_updated_at}\n")
        print(f"#04. repo_size: {repo_size}\n")
        print(f"#05. repo_stars: {repo_stars}\n")
        print(f"#06. repo_watchers: {repo_watchers}\n")
        print(f"#07. repo_language: {repo_language}\n")
        print(f"#08. repo_forks: {repo_forks}\n")
        print(f"#09. repo_open_issues: {repo_open_issues}\n")
        print(f"#10. repo_owner: {repo_owner}\n")
        print(f"#18. repo_description: {repo_description}\n")
        print(f"#19. repo_topics: {repo_topics}\n")
        print(f"#20. repo_functions: {repo_functions}\n")
        print(f"#21. repo_functions_count: {repo_functions_count}\n")
        print(f"#27. repo_releases: {repo_releases}\n")
        print(f"#28. repo_contributors: {repo_contributors}\n")
        print(f"#29. repo_pr: {repo_pr}\n")
        print(f"#30. repo_commits: {repo_commits}\n")
        print("=======================================\n\n")
        '''
  
        '''
        query = f"filename:.cursorrules repo:{repo_fullname}"
        params = {"q": query, "per_page": per_page, "page": page}
        url = "https://api.github.com/search/code"
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            print("Error:", response.status_code, response.text)
            continue
        
        file_data = response.json()
        if "items" not in file_data:
            print(f"Warning: No 'items' found in search response for repo {repo_fullname}")
            continue
        print(f"\n\n{file_data}\n\n")
        
        for item in file_data["items"]:
            file_path = item["path"]
            file_hash = item["sha"]
            file_name = item["name"]
            repo_name = item["repository"]["name"]
            repo_owner = item["repository"]["owner"]["login"]
            repo_id = item["repository"]["id"]
            owner_id = item["repository"]["owner"]["id"]
            owner_type = item["repository"]["owner"]["type"]
            file_url = item["html_url"]
            raw_url = item["html_url"].replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
            
            file_size = get_file_size(repo_owner, repo_name, file_path)
            languages_percentage = get_repo_languages(repo_owner, repo_name)

            print(f"Get {file_name} from {repo_id}:\n")
            print(f"02. file_hash: {file_hash}\n")
            print(f"03. file_name: {file_name}\n")
            print(f"04. file_size: {file_size}\n")
            print(f"05. repo_owner: {repo_owner}\n")
            print(f"06. repo_name: {repo_name}\n")
            print(f"07. file_path: {file_path}\n")
            print(f"10. repo_id: {repo_id}\n")
            print(f"11. owner_id: {owner_id}\n")
            print(f"12. languages: {languages_percentage}\n")
            print(f"13. owner_type: {owner_type}\n")
            print(f"14. file_url: {file_url}\n")
            print(f"15. raw_url: {raw_url}\n")
            print("=======================================\n\n")
            '''

def get_file_size(repo_owner, repo_name, file_path):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("size", 0)
    return -1


def get_repo_languages(repo_owner, repo_name):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/languages"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Get languages failed. url: {url}, status_code: {response.status_code}")
    
    res = response.json()
    total_size = sum(res.values())
    languages_percentage = {lang: round(size / total_size * 100, 2) for lang, size in res.items()} if total_size > 0 else {}
    return languages_percentage


# download repo.zip
def download_repo_zip(repo_fullname, default_branch):
    zip_url = f"https://github.com/{repo_fullname}/archive/{default_branch}.zip"
    zip_filename = f"{repo_fullname.replace('/', '-')}.zip"
    zip_path = os.path.join(save_path, zip_filename)
    response = requests.get(zip_url, headers=headers)
    
    if response.status_code == 200:
        with open(zip_path, "wb") as f:
            f.write(response.content)
        print(f"Succeed to download repo {zip_path}\n")
    else:
        print(f"Failed to download repo {zip_url}\n")


# check readme
def has_readme(repo_fullname):
    url = f"https://api.github.com/repos/{repo_fullname}/readme"
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # print("Succeed to get readme\n")
        return "readme"
    elif response.status_code == 404:
        print("Failed to get readme\n")
        return None


# get commits, pr, contributors, releases_url by GraphQL
def get_metric_count_graphql(repo_owner, repo_name):
    query = f"""
    query {{
      repository(owner: "{repo_owner}", name: "{repo_name}") {{
        releases {{ totalCount }}
        pullRequests(states: [OPEN, CLOSED, MERGED]) {{ totalCount }}
        defaultBranchRef {{
          target {{
            ... on Commit {{
              history(first: 0) {{ totalCount }}
            }}
          }}
        }}
        mentionableUsers {{ totalCount }}
      }}
    }}
    """

    response = requests.post(GITHUB_GRAPHQL_URL, json={"query": query}, headers=headers)
    if response.status_code != 200:
        raise Exception(f"GraphQL request failed: {response.status_code}, {response.text}")

    res = response.json()
    
    repo_data = res["data"]["repository"]
    metrics = {
        "releases": repo_data["releases"]["totalCount"],
        "pull_requests": repo_data["pullRequests"]["totalCount"],
        "commits": repo_data["defaultBranchRef"]["target"]["history"]["totalCount"],
        "contributors": repo_data["mentionableUsers"]["totalCount"]
    }
    
    return metrics


# 
def fetch_commit(conn, repo_owner, repo_name, file_path, file_hash):
    commit_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
    commit_params = {"path": file_path, "per_page": 10}
    commit_response = requests.get(commit_url, headers=headers, params=commit_params)
    
    print("1 Get_commit_info() get:\n")
    print(f"repo_owner: {repo_owner}\n")
    print(f"repo_name: {repo_name}\n")
    print(f"file_path: {file_path}\n")
    print(f"file_hash: {file_hash}\n")
    print(f"commit_url: {commit_url}\n")
    print(f"commit_params: {commit_params}\n")
    print(f"json: {commit_response.json()}\n")
    print("###########################################\n\n")
    

    if commit_response.status_code != 200:
        print("Error fetching commits:", commit_response.status_code, commit_response.text)
        return 1, "Unknown", "Unknown", "Unknown", {"Unknown"}
    
    try:
        commits_json = commit_response.json()
        print("\n### commit_response.status_code == 200 ###\n")
        if not commits_json:
            return 1, "Unknown", "Unknown", "Unknown", {"Unknown"}
        
        commit_num = len(commits_json)
        first_commit = commits_json[-1]
        last_commit = commits_json[0]

        creator_id = first_commit["author"]["id"] if first_commit.get("author") else "Unknown"
        first_commit_time = first_commit["commit"]["author"]["date"] if first_commit.get("commit") else "Unknown"
        last_commit_time = last_commit["commit"]["author"]["date"] if last_commit.get("commit") else "Unknown"
        
        contributors = set()
        commit_times = []
        commit_changes = []
        
        
        for i, commit in enumerate(commits_json):
            commit_times.append(commit["commit"]["author"]["date"])
            if commit.get("author") and commit["author"].get("login"):
                contributors.add(commit["author"]["login"])
            else:
                contributors.add("Unknown")
            
            ### Get commit changes
            curr_commit_sha = commit["sha"]
            if i == 0:
                commit_changes.append(f"First commit: {curr_commit_sha}")
            else:
                prev_commit_sha = commits_json[i - 1]["sha"]
                compare_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/compare/{prev_commit_sha}...{curr_commit_sha}"
                compare_response = requests.get(compare_url, headers=headers)  # 这个有没有可能多页?
                
                if compare_response.status_code == 200:
                    compare_data = compare_response.json()
                    file_changes = [
                        file["patch"] for file in compare_data.get("files", []) if file["filename"] == file_path
                    ]
                    commit_changes.append(f"SSSSStart\n{curr_commit_sha}: \n" + "\n".join(file_changes) + "\nEEEEEnd\n")
                else:
                    commit_changes.append("Unknown")
        
        contributor_num = len(contributors)
        

        
        print(f"Commit related metada in: {repo_name}:\n")
        print(f"C01. file_hash: {file_hash}\n")
        print(f"C02. commit_num: {commit_num}\n")
        print(f"C03. first_commit_time: {first_commit_time}\n")
        print(f"C04. last_commit_time: {last_commit_time}\n")
        print(f"C05. commit_times: {commit_times}\n")
        print(f"C06. commit_changes: {commit_changes}\n")
        print(f"C07. contributors: {contributors}\n")
        print(f"C08. contributor_num: {contributor_num}\n")
        print(f"C09. creator_id: {creator_id}\n")
        print("=======================================\n\n")
        return commit_num, first_commit_time, last_commit_time, creator_id, contributors, contributor_num
        
    except Exception as e:
        print(f"Error when parsing {repo_owner}/{repo_name}/{file_path}: {e}")
        return 1, "Unknown", "Unknown", "Unknown", {"Unknown"}


# commit_num, file_created_at, creator_id, file_last_updated, file_contributor_num
#commit_num, first_commit_time, creator_id, last_commit_time, contributors = get_commit_info(conn, repo_owner, repo_name, item["path"], file_hash)
#sssss = get_commit_info(conn, repo_owner, repo_name, item["path"], file_hash)



def main():
    global headers
    headers = get_headers()
    conn = sqlite3.connect("cursor0321.db")
    create_tables(conn)
    
    # https://github.com/grapeot/devin.cursorrules/commits/master/.cursorrules
    # https://github.com/PatrickJS/awesome-cursorrules/commits/main/rules/go-backend-scalability-cursorrules-prompt-file/.cursorrules
    
    
    get_repo(conn, 10, 1)
    conn.close()
    
    '''result = fetch_commit(conn, repo_owner, repo_name, file_path, file_hash, per_page, page)
    commit_num = result['commit_num']
    first_commit_time = result['first_commit_time']
    last_commit_time = result['last_commit_time']
    creator_id = result['creator_id']
    contributors = result['contributors']
    contributor_num = result['contributor_num']
    
    print(f"In Main:\n")
    print(f"C01. result: {result}\n")
    print(f"C02. commit_num: {commit_num}\n")
    print(f"C03. first_commit_time: {first_commit_time}\n")
    print(f"C04. last_commit_time: {last_commit_time}\n")
    print(f"C07. contributors: {contributors}\n")
    print(f"C08. contributor_num: {contributor_num}\n")
    print(f"C09. creator_id: {creator_id}\n")
    print("=======================================\n\n")'''


if __name__=="__main__":
    main()
    







'''
# get commits, pr, contributors, releases_url
def get_metric_count(repo_fullname, api_name):
    url = f"https://api.github.com/repos/{repo_fullname}/{api_name}"
    params = {'per_page': 100, 'page': 1}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Request API {api_name} failed: {url}, status_code: {response.status_code}")
    
    res = response.json()
    count = len(res)
    
    link = response.headers.get('Link', '')
    if 'rel="next"' in link:
        return 101
    else:
        return count

# Invoke get_metric_count():
repo_releases1 = get_metric_count(repo_fullname, "releases")
repo_contributors1 = get_metric_count(repo_fullname, "contributors")
repo_pr1 = get_metric_count(repo_fullname, "pulls?state=all")
repo_commits1 = get_metric_count(repo_fullname, "commits")
'''
import requests
import os
import sqlite3
import time
import itertools
import json
import logging

GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"


def get_repo_from_db(conn, repo_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM repos WHERE repo_id = ?", (repo_id,))
    fetchone_repodb = cursor.fetchone()
    if fetchone_repodb:
        print(f"raw_md5[0]: {fetchone_repodb[0]}\n")
        print(f"user_id[1]: {fetchone_repodb[1]}\n")
        print(f"login[2]: {fetchone_repodb[2]}\n")
        print(f"user_repos[3]: {fetchone_repodb[3]}\n")
        print(f"user_gists[4]: {fetchone_repodb[4]}\n")
        print(f"user_followers[5]: {fetchone_repodb[5]}\n")
        print(f"user_stars[6]: {fetchone_repodb[6]}\n")
        print(f"user_forks[7]: {fetchone_repodb[7]}\n")
        print(f"user_open_issues[8]: {fetchone_repodb[8]}\n")
        print(f"user_created_at[9]: {fetchone_repodb[9]}\n")
        print(f"user_last_active[10]: {fetchone_repodb[10]}\n")
        print(f"user_tags_count[11]: {fetchone_repodb[11]}\n")
        print(f"user_tags[12]: {fetchone_repodb[12]}\n")
        print(f"user_bio[13]: {fetchone_repodb[13]}\n")
        print(f"user_organizations_count[14]: {fetchone_repodb[14]}\n")
        print(f"user_type[15]: {fetchone_repodb[15]}\n")
        print(f"user_company[16]: {fetchone_repodb[16]}\n")
        print(f"user_blog[17]: {fetchone_repodb[17]}\n")
    
    return fetchone_repodb


def create_table_repos(conn):
    cursor = conn.cursor()

    # Create table 'repos'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS repos (
            raw_md5 TEXT PRIMARY KEY,
            repo_id INTEGER NOT NULL,
            repo_owner_id INTEGER NOT NULL,
            repo_name TEXT NOT NULL,
            repo_owner TEXT NOT NULL,
            repo_created_at TEXT,
            repo_last_updated TEXT,
            repo_size INTEGER,
            repo_stars INTEGER,
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
            repo_topics TEXT,
            repo_license TEXT,
            repo_wiki TEXT,
            repo_discussion TEXT
        )
    ''')
    conn.commit()

 
# -github.com/search?q=awesome-cursorrules&type=repositories
def get_repo(conn, headers, repo_full_name, repo_id, raw_md5, save_path):
    '''query = "awesome-cursorrules in:name"
    params = {"q": query, "per_page": per_page, "page": page}
    url = "https://api.github.com/search/repositories"
    repo_response = requests.get(url, headers=headers, params=params)'''
    
    try:
        url = f"https://api.github.com/repos/{repo_full_name}"
        repo_response = requests.get(url, headers=headers)
        
        if repo_response.status_code != 200:
            print("Error:", repo_response.status_code, repo_response.text)
            logging.error(f"[Repo Error] {repo_full_name}: {repo_response.status_code} {repo_response.text}\n")
            return {}
        
        repo_data = repo_response.json()
        time.sleep(1)
        
        repo_name = repo_data.get("name")
        repo_created_at = repo_data.get("created_at")
        repo_updated_at = repo_data.get("updated_at")
        repo_size = repo_data.get("size")
        repo_stars = repo_data.get("stargazers_count")
        repo_watchers = repo_data.get("watchers_count")
        repo_forks = repo_data.get("forks_count")
        repo_open_issues = repo_data.get("open_issues_count")
        owner = repo_data.get("owner", {})
        repo_owner = owner.get("login", None)
        repo_owner_id = owner.get("id", -1)
        # https://github.com/{owner}/{repo}/wiki
        repo_wiki = f"https://github.com/{repo_owner}/{repo_name}/wiki" if repo_data.get("has_wiki") else None
        repo_discussion = f"https://github.com/{repo_owner}/{repo_name}/discussions" if repo_data.get("has_discussions") else None
        repo_license = str(repo_data.get("license")) if repo_data.get("license") else ""
        repo_languages = get_repo_languages(headers, repo_full_name)
        repo_topics = repo_data.get("topics", [])
        repo_topics_str = ",".join(repo_topics) if repo_topics else ""
        repo_default_branch = repo_data.get("default_branch")
        repo_description = repo_data.get("description")

        repo_functions = []
        if repo_wiki: repo_functions.append("wiki")
        if repo_discussion: repo_functions.append("discussion")
        if repo_license: repo_functions.append("license")
        if has_readme(headers, repo_full_name, raw_md5, save_path):
            repo_functions.append("readme")
        repo_functions_count = len(repo_functions)
        repo_functions_str = ",".join(repo_functions)

        try:
            metrics = get_metric_count_graphql(headers, repo_owner, repo_name)
            repo_releases = metrics.get("releases", 0)
            repo_contributors = metrics.get("contributors", 0)
            repo_prs = metrics.get("pull_requests", 0)
            repo_commits = metrics.get("commits", 0)
        except Exception as metric_error:
            print(f"[Metrics Error]: repo {repo_full_name}: {metric_error}\n")
            logging.error(f"[Metrics Error]: repo {repo_full_name}: {metric_error}\n")
            repo_releases = repo_contributors = repo_prs = repo_commits = 0
                
        ### save to SQLite**
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO repos (raw_md5, repo_id, repo_owner_id, repo_name, repo_owner, repo_created_at, repo_last_updated, repo_size, repo_stars, repo_watchers, repo_forks, repo_open_issues, repo_contributors, repo_releases, repo_prs, repo_commits, repo_functions, repo_functions_count, repo_languages, repo_description, repo_topics, repo_license, repo_wiki, repo_discussion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (raw_md5, repo_id, repo_owner_id, repo_name, repo_owner, repo_created_at, repo_updated_at, repo_size, repo_stars, repo_watchers, repo_forks, repo_open_issues, repo_contributors, repo_releases, repo_prs, repo_commits, repo_functions_str, repo_functions_count, repo_languages, repo_description, repo_topics_str, repo_license, repo_wiki, repo_discussion)
            )
            conn.commit()
        except Exception as saveDB_error:
            print(f"[Save to SQLite Error]: repo {repo_full_name}: {saveDB_error}\n")
            logging.error(f"[Save to SQLite Error]: repo {repo_full_name}: {saveDB_error}\n")
        
        try:
            download_repo_zip(headers, repo_full_name, repo_default_branch, raw_md5, save_path)
        except Exception as zip_error:
            print(f"[Download Error]: repo {repo_full_name}: {zip_error}\n")
            logging.error(f"[Download Error]: repo {repo_full_name}: {zip_error}\n")
        
        repo_return = {
            "repo_created_at": repo_created_at,
            "repo_updated_at": repo_updated_at,
            "repo_stars": repo_stars,
            "repo_forks": repo_forks,
            "repo_contributors": repo_contributors,
            "repo_prs": repo_prs,
            "repo_commits": repo_commits,
            "repo_languages": repo_languages
        }
        return repo_return
    except Exception as e:
        print(f"[FATAL get_repo ERROR]: repo {repo_full_name}: {e}\n")
        logging.error(f"[FATAL get_repo ERROR]: repo {repo_full_name}: {e}\n")
        return {}


# get repo languages_percentage
def get_repo_languages(headers, repo_full_name):
    try:
        url = f"https://api.github.com/repos/{repo_full_name}/languages"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Get languages failed. url: {url}, status_code: {response.status_code}")
        
        res = response.json()
        total_size = sum(res.values())
        languages_percentage = {
            lang: round(size / total_size * 100, 2)
            for lang, size in res.items()
        } if total_size > 0 else {}
        # print(f"\n\nlanguages persentage: {languages_percentage}\n\n")
        return str(languages_percentage)
    except Exception as e:
        logging.error(f"[Language Error] {repo_full_name}: {e}\n")
        return ""

# download repo.zip
def download_repo_zip(headers, repo_full_name, default_branch, raw_md5, save_path):
    MAX_SIZE_BYTES = 800 * 1024 * 1024
    zip_url = f"https://github.com/{repo_full_name}/archive/{default_branch}.zip"
    zip_filename = f"{raw_md5}.zip"
    zip_path = os.path.join(save_path, zip_filename)
    try:
        response = requests.get(zip_url, headers=headers, stream=True, timeout=60)
        if response.status_code != 200:
            print(f"Failed to download repo {zip_url}\n")
            return

        file_size = int(response.headers.get('Content-Length', 0))
        if file_size > MAX_SIZE_BYTES:
            print(f"Skipping download for {zip_url}. File size ({file_size / 1024 / 1024:.2f} MB) exceeds 800MB.")
            return
        else:
            print(f"File size is {file_size / 1024 / 1024:.2f} MB, proceeding with download.")

        with open(zip_path, "wb") as f:
            f.write(response.content)
        print(f"Succeeded to download repo {zip_path}\n")
    except Exception as e:
        print(f"Error downloading repo {zip_url}: {e}")

# check readme
def has_readme(headers, repo_full_name, raw_md5, save_path):
    readme_url = f"https://api.github.com/repos/{repo_full_name}/readme"
    response = requests.get(readme_url, headers=headers)
    if response.status_code == 200:
        # print("Succeed to get readme\n")
        readme = response.json()
        download_url = readme.get("download_url")
        readme_filename = f"{raw_md5}.readme.md"
        readme_path = os.path.join(save_path, readme_filename)
        response2 = requests.get(download_url, headers=headers)
        if response2.status_code == 200:
            with open(readme_path, "wb") as f:
                f.write(response2.content)
            print(f"Succeed to download repo {readme_path}\n")
        else:
            print(f"Failed to download repo {download_url}\n")
        return "readme"
    elif response.status_code == 404:
        print("README not found.\n")
        return None
    else:
        print(f"Failed to get README, HTTP Status: {response.status_code}\n")
        return None

# get commits, pr, contributors, releases_url by GraphQL
def get_metric_count_graphql(headers, repo_owner, repo_name):
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

    try:
        response = requests.post(GITHUB_GRAPHQL_URL, json={"query": query}, headers=headers)
        if response.status_code != 200:
            raise Exception(f"GraphQL request failed: {response.status_code}, {response.text}")

        res = response.json()
        repo_data = res.get("data", {}).get("repository", {})
        metrics = {
            "releases": repo_data.get("releases", {}).get("totalCount", 0),
            "pull_requests": repo_data.get("pullRequests", {}).get("totalCount", 0),
            "commits": repo_data.get("defaultBranchRef", {}).get("target", {}).get("history", {}).get("totalCount", 0),
            "contributors": repo_data.get("mentionableUsers", {}).get("totalCount", 0)
        }
        
        return metrics
    except Exception as e:
        logging.error(f"[GraphQL Error]: repo {repo_owner}/{repo_name}: {e}\n")
        metrics = {
            "releases": 0,
            "pull_requests": 0,
            "commits": 0,
            "contributors": 0
        }
        return metrics
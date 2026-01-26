import requests
import os
import sqlite3
import time
import itertools
import json
from file import get_commit
from file import get_file


GITHUB_TOKEN = ""

# Function to check the API rate limit
def check_rate_limit():
    url = "https://api.github.com/rate_limit"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data["resources"]["code_search"]["remaining"], data["resources"]["code_search"]["reset"]
    else:
        print(f"Error checking rate limit: {response.text}\n")
        return 0, time.time() + 60  # Assume 60s wait if API call fails

# Function to get headers (ensuring we don't exceed the rate limit)
def get_headers():
    remaining, reset_time = check_rate_limit()

    if remaining == 0:  # If limit is reached, wait until reset
        wait_time = reset_time - time.time()
        if wait_time > 0:
            print(f"API limit reached! Sleeping for {int(wait_time)} seconds until reset...\n")
            time.sleep(wait_time)

    return {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}


def create_tables(conn):
    cursor = conn.cursor()
    # Create table 'files'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            raw_md5 TEXT PRIMARY KEY,
            repo_id INTEGER NOT NULL,
            owner_id INTEGER NOT NULL,
            creator_login TEXT NOT NULL,
            file_size INTEGER,
            file_created_at TEXT,
            file_last_updated TEXT,
            repo_languages TEXT,
            commit_count INTEGER,
            commit_authors_count INTEGER,
            commit_timeflow TEXT,
            commit_messages TEXT,
            creator_repos INTEGER,
            creator_gists INTEGER,
            creator_followers INTEGER,
            creator_stars INTEGER,
            creator_forks INTEGER,
            creator_created_at TEXT,
            creator_last_active TEXT,
            creator_tags TEXT,          
            owner_repos INTEGER,
            owner_gists INTEGER,
            owner_followers INTEGER,
            owner_stars INTEGER,
            owner_forks INTEGER,
            owner_created_at TEXT,
            owner_last_active TEXT,
            owner_tags TEXT,
            repo_stars INTEGER,
            repo_forks INTEGER,
            repo_contributors INTEGER,
            repo_prs INTEGER,
            repo_commits INTEGER,
            repo_created_at TEXT,
            repo_updated_at TEXT,
            file_url TEXT NOT NULL
        )
    ''')
    
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

    # Create table 'users'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            raw_md5 TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,            
            user_login TEXT NOT NULL,
            user_repos INTEGER,
            user_gists INTEGER,
            user_followers INTEGER,
            user_stars INTEGER,
            user_forks INTEGER,
            user_open_issues INTEGER,
            user_created_at TEXT,
            user_last_active TEXT,
            user_tags_count INTEGER,
            user_tags TEXT,
            user_bio TEXT,
            user_organizations_count INTEGER,
            user_type TEXT,
            user_company TEXT,
            user_blog TEXT
        )
    ''')

    # Create table 'creators'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS creators (
            raw_md5 TEXT PRIMARY KEY,
            creator_id INTEGER NOT NULL,            
            creator_login TEXT NOT NULL,
            creator_repos INTEGER,
            creator_gists INTEGER,
            creator_followers INTEGER,
            creator_stars INTEGER,
            creator_forks INTEGER,
            creator_open_issues INTEGER,
            creator_created_at TEXT,
            creator_last_active TEXT,
            creator_tags_count INTEGER,
            creator_tags TEXT,
            creator_bio TEXT,
            creator_organizations_count INTEGER,
            creator_type TEXT,
            creator_company TEXT,
            creator_blog TEXT
        )
    ''')
    
    # Create table 'commits'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS commits (
            raw_md5 TEXT NOT NULL,
            commit_sha TEXT NOT NULL,
            commit_time TEXT,
            commit_author TEXT,
            commit_author_id INTEGER,
            commit_message TEXT,
            commit_comment_count INTEGER,
            v_verified INTEGER,
            v_reason TEXT,
            v_time TEXT,
            commit_status TEXT,
            commit_additions INTEGER,
            commit_deletions INTEGER,
            commit_changes INTEGER,
            commit_patch TEXT,
            commit_url TEXT,
            file_commits_url TEXT NOT NULL,
            PRIMARY KEY (raw_md5, commit_sha)
        )
    ''')
    conn.commit()


def main():
    global headers
    headers = get_headers()
    conn = sqlite3.connect("/mnt/d/1stp_cursor/4.0crawler/cursor0409_general.db")
    create_tables(conn)
    
    try:
        with open("/mnt/d/1stp_cursor/4.0crawler/last_page.txt", "r") as f:
            start_page = int(f.read().strip())
    except FileNotFoundError:
        start_page = 1

    per_page = 100
    max_page = 10
    for page in range(start_page, max_page + 1):  
        print(f"\nFetching page {page}...\n")

        # query = "filename:.cursorrules -repo:alpgul/Cursorrules-Database -repo:PatrickJS/awesome-cursorrules -repo:afontana1/Data-Engineering"
        query = "filename:.cursorrules repo:PatrickJS/awesome-cursorrules"
        params = {"q": query, "per_page": per_page, "page": page}
        url = f"https://api.github.com/search/code"
        file_response = requests.get(url, headers=headers, params=params)
        get_file(file_response, conn, headers, per_page, page)  # Fetch one page at a time

        try:
            with open("/mnt/d/1stp_cursor/4.0crawler/last_page.txt", "w") as f:
                f.write(str(page + 1))
        except Exception as e:
            print(f"Error writing last_page.txt: {e}")
        
    
    print("\n######################################\n")
    print("####  ALL DONE! Congratulations!  ####\n")
    print("######################################\n")
    conn.close()


   

if __name__=="__main__":
    main()

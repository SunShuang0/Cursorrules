import hashlib
import requests
import os
import sqlite3
import time
import itertools
import json
import logging
from repo import get_repo
from user import get_user

logging.basicConfig(filename='errors_general.log', level=logging.ERROR)
save_path = "/mnt/d/1stp_cursor/4.0crawler/download_general"
if not os.path.exists(save_path):
    os.makedirs(save_path)

def get_user_from_db(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    fetchone = cursor.fetchone()
    return fetchone

def get_repo_from_db(conn, repo_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM repos WHERE repo_id = ?", (repo_id,))
    fetchone_repodb = cursor.fetchone()
    return fetchone_repodb

def get_creator_from_db(conn, creator_login):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM creators WHERE creator_login = ?", (creator_login,))
    fetchone_db = cursor.fetchone()
    return fetchone_db

def genmd5(url):
    md5_str = hashlib.md5(url.encode()).hexdigest()
    return md5_str

def get_file(file_response, conn, headers, per_page, page):
    # query = "filename:.cursorrulesANDyouANDareANDjava -repo:alpgul/Cursorrules-Database"
    # file_response = requests.get(url, headers=headers, params=params)
    # query = "filename:.cursorrules safely -repo:alpgul/Cursorrules-Database -repo:PatrickJS/awesome-cursorrules"
    # params = {"q": query, "per_page": per_page, "page": page}
    # url = f"https://api.github.com/search/code"   
    # file_response = requests.get(url, headers=headers, params=params)
    print(f"Making GET request to URL: {file_response.url}")
    if file_response.status_code == 403 and "X-RateLimit-Reset" in file_response.headers:
        reset_time = int(file_response.headers["X-RateLimit-Reset"])
        sleep_time = reset_time - int(time.time())
        print(f"Rate limit exceeded. Sleeping for {sleep_time} seconds.")
        time.sleep(max(sleep_time, 1))
        return get_file(conn, headers, per_page, page)  # Retry after sleeping
        
    if file_response.status_code != 200:
        print("Error:", file_response.status_code, file_response.text)
        return []
    
    file_data = file_response.json()
    if "items" not in file_data:
        print("Error: No 'items' found in repository response")
        return []
    
    # print(f"\n\n{file_data}\n\n")
    


    for file in file_data["items"]:
        commit_count = 0
        commit_authors_count = 0
        commit_timeflow = ""
        commit_messages = ""
        creator_login = None
        creator_created_at = None
        creator_last_active = None
        creator_repos = 0
        creator_followers = 0
        creator_gists = 0
        creator_stars = 0
        creator_forks = 0
        creator_tags = ""
        owner_created_at = None
        owner_last_active = None
        owner_repos = 0
        owner_followers = 0
        owner_gists = 0
        owner_stars = 0
        owner_forks = 0
        owner_tags = ""
        repo_created_at = None
        repo_updated_at = None
        repo_stars = 0
        repo_forks = 0
        repo_contributors = 0
        repo_prs = 0
        repo_commits = 0
        repo_languages = ""
        file_url = file.get("html_url", "")
        if not file_url:
            print("Warning: file html_url is missing.\n")
        raw_url = file_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/").strip()
        raw_md5 = genmd5(raw_url)
        file_path = file.get("path", "")
        repo_full_name = file.get("repository", {}).get("full_name", "")
        repo_id =  file.get("repository", {}).get("id", "")
        owner_id = file.get("repository", {}).get("owner", {}).get("id", "")
        owner_login = file.get("repository", {}).get("owner", {}).get("login", "")
        repo_commits_url = file.get("repository", {}).get("commits_url", "")
        if repo_commits_url:
            repo_commits_url = repo_commits_url.replace("{/sha}", "")
        else:
            print("Warning: repository commits_url is missing for file:", file.get("html_url", "Unknown URL"))
        file_commits_url = f"{repo_commits_url}?path={file_path}"
        file_commits_url = file_commits_url.strip()

        if not raw_url:
            print(f"Error: Missing raw_url for {raw_md5}. Skipping download.\n")
        else:
            try:
                download_file(raw_url, raw_md5, headers)
            except Exception as e:
                print(f"Failed to download {raw_url}: {e}\n")
                logging.error(f"Failed to download {raw_url}: {e}\n")
        
        file_size = get_file_size(repo_full_name, file_path, headers)
        
        ##################################################
        # 1. Get commits metadata
        print(f"\n--------------- 1. Get commits ---------------\n")
        try:
            commit_return = get_commit(conn, headers, file_commits_url, raw_md5, file_path)
        except Exception as e:
            print(f"Error in get_commit() for {file_commits_url}, {raw_md5}, {file_path}: {e}\n")
            logging.error(f"Error in get_commit() for {file_commits_url}, {raw_md5}, {file_path}: {e}\n")
            commit_return = {}
        if not isinstance(commit_return, dict):
            print(f"Warning: get_commit() returned an invalid response for {file_commits_url}, {raw_md5}, {file_path}")
            commit_return = {}
        file_created_at = commit_return.get("file_created_at", None)
        file_last_updated = commit_return.get("file_last_updated", None)
        creator_str = commit_return.get("file_creator")
        if isinstance(creator_str, str) and creator_str.strip() and creator_str != "Not Github User":
            creator_login = creator_str.strip()
        commit_count = commit_return.get("commit_count", 0)
        commit_authors_count = commit_return.get("commit_authors_count", 0)
        commit_timeflow = commit_return.get("commit_timeflow", [])
        commit_messages = commit_return.get("commit_messages", [])
        commit_timeflow_json = json.dumps(commit_timeflow)
        commit_messages_json = json.dumps(commit_messages, ensure_ascii=False)
        # If you need to read commit_timeflow_json and commit_messages_json from DB:
        # commit_timeflow = json.loads(row["commit_timeflow"])
        # commit_messages = json.loads(row["commit_messages"])
        print("\n ********** 1. Get commit data DONE! **********\n")
        
        ##################################################
        # 2. Get creator metadata
        if creator_login:
            print(f"\n--------------- 2. Get creator ---------------\n")
            try:
                fetchone_creatordb = get_creator_from_db(conn, creator_login)
                ## 2.1 If the creator_login is existed in the table 'creators'
                if fetchone_creatordb:
                    print(f"Creator {creator_login} is found in database. Reinserting with new raw_md5 {raw_md5}.")
                    ### 2.1.1 Insert a new item with new raw_md5 to table 'creators'
                    try:
                        cursor = conn.cursor()
                        cursor.execute('''
                            INSERT INTO creators (raw_md5, creator_id, creator_login, creator_repos, creator_gists, creator_followers, creator_stars, creator_forks, creator_open_issues, creator_created_at, creator_last_active, creator_tags_count, creator_tags, creator_bio, creator_organizations_count, creator_type, creator_company, creator_blog)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (raw_md5, fetchone_creatordb[1], creator_login, fetchone_creatordb[3], fetchone_creatordb[4], fetchone_creatordb[5], fetchone_creatordb[6], fetchone_creatordb[7], fetchone_creatordb[8], fetchone_creatordb[9], fetchone_creatordb[10], fetchone_creatordb[11], fetchone_creatordb[12], fetchone_creatordb[13], fetchone_creatordb[14], fetchone_creatordb[15], fetchone_creatordb[16], fetchone_creatordb[17])
                        )
                        conn.commit()
                        print(f"\nCreator {creator_login} has been inserted into creators_table with new raw_md5 {raw_md5}.\n")
                    except Exception as e:
                        print(f"Error inserting creator {creator_login} into DB with new raw_md5 {raw_md5}: {e}\n")
                        logging.error(f"Error inserting creator {creator_login} into DB with new raw_md5 {raw_md5}: {e}\n")
                    ### 2.1.2 Value the following variables so that they can be inserted into the table 'files' later
                    try:
                        creator_created_at = fetchone_creatordb[9]
                        creator_last_active = fetchone_creatordb[10]
                        creator_repos = fetchone_creatordb[3]
                        creator_followers = fetchone_creatordb[5]
                        creator_gists = fetchone_creatordb[4]
                        creator_stars = fetchone_creatordb[6]
                        creator_forks = fetchone_creatordb[7]
                        creator_tags = fetchone_creatordb[12]
                    except Exception as e:
                        print(f"Error extracting creator data for {creator_login}: {e}\n")
                        logging.error(f"Error extracting creator data for {creator_login}: {e}\n")
                ## 2.2 If the creator_login is new
                else:
                    print(f"\nUser with creator_login {creator_login} is not found in database.\n")
                    ### 2.2.1 Invoke new API request to fetch user data
                    try:
                        creator_return = get_user(conn, headers, raw_md5, creator_login, 2)
                    except Exception as e:
                        print(f"Error fetching creator data from API for {creator_login}: {e}\n")
                        logging.error(f"Error fetching creator data from API for {creator_login}: {e}\n")
                        creator_return = {}
                    ### 2.2.2 Value the variables with new data
                    creator_created_at = creator_return.get("user_created_at")
                    creator_last_active = creator_return.get("user_last_active")
                    creator_repos = creator_return.get("user_repos")
                    creator_followers = creator_return.get("user_followers")
                    creator_gists = creator_return.get("user_gists")
                    creator_stars = creator_return.get("user_stars")
                    creator_forks = creator_return.get("user_forks")
                    creator_tags = creator_return.get("user_tags")
                print("\n ********** 2. Get creator data DONE! **********\n")
            except Exception as e:
                print(f"Unexpected error processing creator metadata for {creator_login}: {e}\n")
                logging.error(f"Unexpected error processing creator metadata for {creator_login}: {e}\n")
        
        ##################################################
        # 3. Get repos metadata
        if repo_id:       
            print(f"\n--------------- 3. Get repos ---------------\n")
            try:
                fetchone_repodb = get_repo_from_db(conn, repo_id)
                ## 3.1 If the repo_id is existed in the table 'repos'
                if fetchone_repodb:
                    print(f"Repository {repo_id} is found in database. Reinserting with new raw_md5 {raw_md5}.")
                    ### 3.1.1 Insert a new item with new raw_md5
                    try:
                        cursor = conn.cursor()
                        cursor.execute('''
                            INSERT INTO repos (raw_md5, repo_id, repo_owner_id, repo_name, repo_owner, repo_created_at, repo_last_updated, repo_size, repo_stars, repo_watchers, repo_forks, repo_open_issues, repo_contributors, repo_releases, repo_prs, repo_commits, repo_functions, repo_functions_count, repo_languages, repo_description, repo_topics, repo_license, repo_wiki, repo_discussion)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (raw_md5, repo_id, fetchone_repodb[2], fetchone_repodb[3], fetchone_repodb[4], fetchone_repodb[5], fetchone_repodb[6], fetchone_repodb[7], fetchone_repodb[8], fetchone_repodb[9], fetchone_repodb[10], fetchone_repodb[11], fetchone_repodb[12], fetchone_repodb[13], fetchone_repodb[14], fetchone_repodb[15], fetchone_repodb[16], fetchone_repodb[17], fetchone_repodb[18], fetchone_repodb[19], fetchone_repodb[20], fetchone_repodb[21], fetchone_repodb[22], fetchone_repodb[23])
                        )
                        conn.commit()
                        print(f"\nRepository {repo_id} has been inserted into repos_table with new raw_md5 {raw_md5}.\n")
                    except Exception as e:
                        print(f"\nError inserting repository {repo_id} into repos_table with new raw_md5 {raw_md5}: {e}.\n")
                        logging.error(f"\nError inserting repository {repo_id} into repos_table with new raw_md5 {raw_md5}: {e}.\n")
                    ### 3.1.2 Value the repo-relative variables with existed repo-data
                    try:
                        repo_created_at = fetchone_repodb[5]
                        repo_updated_at = fetchone_repodb[6]
                        repo_stars = fetchone_repodb[8]
                        repo_forks = fetchone_repodb[10]
                        repo_contributors = fetchone_repodb[12]
                        repo_prs = fetchone_repodb[14]
                        repo_commits = fetchone_repodb[15]
                        repo_languages = fetchone_repodb[18]
                    except Exception as e:
                        print(f"Error extracting repo data for repo {repo_id}.\n")
                        logging.error(f"Error extracting repo data for repo {repo_id}.\n")
                ## 3.2 If the repo_id is new (not existed in the table 'repos')
                else:
                    print(f"\nRepository {repo_id} is not found in database.\n")
                    ### 3.2.1 Invoke new API request to fetch repo data
                    try:
                        repo_return = get_repo(conn, headers, repo_full_name, repo_id, raw_md5, save_path)
                    except Exception as e:
                        print(f"Error fetching repo data from API for {repo_id}: {e}\n")
                        logging.error(f"Error fetching repo data from API for {repo_id}: {e}\n")
                        repo_return = {}
                    ### 3.2.2 Value the variables with new data
                    repo_created_at = repo_return.get("repo_created_at")
                    repo_updated_at = repo_return.get("repo_updated_at")
                    repo_stars = repo_return.get("repo_stars")
                    repo_forks = repo_return.get("repo_forks")
                    repo_contributors = repo_return.get("repo_contributors")
                    repo_prs = repo_return.get("repo_prs")
                    repo_commits = repo_return.get("repo_commits")
                    repo_languages = repo_return.get("repo_languages")
                print("\n ********** 3. Get repo data DONE! **********\n")
            except Exception as e:
                print(f"Error processing repo {repo_id}: {e}\n")
                logging.error(f"Error processing repo {repo_id}: {e}\n")
        else:
            print(f"repo_id: {repo_id} is None. Skipping processing.")
            logging.warning(f"repo_id: {repo_id} is None. Skipping processing.")
        
        ##################################################
        # 4. Get owner metadata
        if owner_id:
            print(f"\n--------------- 4. Get owner ---------------\n")
            try:
                fetchone_userdb = get_user_from_db(conn, owner_id)
                ## 4.1 If the owner_id is existed in the table 'users'
                if fetchone_userdb:
                    print(f"Owner {owner_login} with owner_id {owner_id} is found in database. Reinserting with new raw_md5 {raw_md5}.\n")
                    ### 4.1.1 Insert a new item with new sha to table 'users'
                    try:
                        cursor = conn.cursor()
                        cursor.execute('''
                            INSERT INTO users (raw_md5, user_id, user_login, user_repos, user_gists, user_followers, user_stars, user_forks, user_open_issues, user_created_at, user_last_active, user_tags_count, user_tags, user_bio, user_organizations_count, user_type, user_company, user_blog)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (raw_md5, owner_id, owner_login, fetchone_userdb[3], fetchone_userdb[4], fetchone_userdb[5], fetchone_userdb[6], fetchone_userdb[7], fetchone_userdb[8], fetchone_userdb[9], fetchone_userdb[10], fetchone_userdb[11], fetchone_userdb[12], fetchone_userdb[13], fetchone_userdb[14], fetchone_userdb[15], fetchone_userdb[16], fetchone_userdb[17])
                        )
                        conn.commit()
                        print(f"\nOwner {owner_id} with new raw_md5 {raw_md5} has been inserted into users_table.\n")
                    except Exception as e:
                        print(f"\nError inserting owner {owner_id} into users_table with new raw_md5 {raw_md5}: {e}.\n")
                        logging.error(f"\nError inserting owner {owner_id} into users_table with new raw_md5 {raw_md5}: {e}.\n")
                    ### 4.1.2 Value the following variables so that they can be inserted into the table 'files' later
                    try:
                        owner_created_at = fetchone_userdb[9]
                        owner_last_active = fetchone_userdb[10]
                        owner_repos = fetchone_userdb[3]
                        owner_followers = fetchone_userdb[5]
                        owner_gists = fetchone_userdb[4]
                        owner_stars = fetchone_userdb[6]
                        owner_forks = fetchone_userdb[7]
                        owner_tags = fetchone_userdb[12]
                    except Exception as e:
                        print(f"Error extracting owner data for {owner_id}: {e}\n")
                        logging.error(f"Error extracting owner data for {owner_id}: {e}\n")
                ## 4.2 If the owner_id is new
                else:
                    print(f"\nOwner {owner_id} with owner_login {owner_login} is not found in database.\n")
                    ### 4.2.1 Invoke new API request to fetch user data
                    try:
                        owner_return = get_user(conn, headers, raw_md5, owner_login, 1)
                    except Exception as e:
                        print(f"Error fetching owner {owner_id} data from API with owner_login {owner_login}: {e}\n")
                        logging.error(f"Error fetching owner {owner_id} data from API with owner_login {owner_login}: {e}\n")
                        owner_return = {}
                    ### 4.2.2 Value the variables with new data
                    owner_created_at = owner_return.get("user_created_at")
                    owner_last_active = owner_return.get("user_last_active")
                    owner_repos = owner_return.get("user_repos")
                    owner_followers = owner_return.get("user_followers")
                    owner_gists = owner_return.get("user_gists")
                    owner_stars = owner_return.get("user_stars")
                    owner_forks = owner_return.get("user_forks")
                    owner_tags = owner_return.get("user_tags")
                print("\n ********** 4. Get Owner Data DONE! **********\n")
            except Exception as e:
                print(f"Unexpected error processing owner metadata for {owner_id}: {e}\n")
                logging.error(f"Unexpected error processing owner metadata for {owner_id}: {e}\n")
        else:
            print(f"owner_id: {owner_id} is None. Skipping processing.")
            logging.warning(f"owner_id: {owner_id} is None. Skipping processing.")
        
        ##################################################
        ### 5. Save to SQLite**
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO files (raw_md5, repo_id, owner_id, creator_login, file_size, file_created_at, file_last_updated, repo_languages, commit_count, commit_authors_count, commit_timeflow, commit_messages, creator_repos, creator_gists, creator_followers, creator_stars, creator_forks, creator_created_at, creator_last_active, creator_tags, owner_repos, owner_gists, owner_followers, owner_stars, owner_forks, owner_created_at, owner_last_active, owner_tags, repo_stars, repo_forks, repo_contributors, repo_prs, repo_commits, repo_created_at, repo_updated_at, file_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (raw_md5, repo_id, owner_id, creator_login, file_size, file_created_at, file_last_updated, repo_languages, commit_count, commit_authors_count, commit_timeflow_json, commit_messages_json, creator_repos, creator_gists, creator_followers, creator_stars, creator_forks, creator_created_at, creator_last_active, creator_tags, owner_repos, owner_gists, owner_followers, owner_stars, owner_forks, owner_created_at, owner_last_active, owner_tags, repo_stars, repo_forks, repo_contributors, repo_prs, repo_commits, repo_created_at, repo_updated_at, file_url)
            )
            conn.commit()
            print("\n ********** 5. Save data to table 'files' DONE! **********\n")
        except Exception as e:
            print(f"Error inseting the file of raw_md5 {raw_md5} into files_table: {e}\n")
            logging.error(f"Error inseting the file of raw_md5 {raw_md5} into files_table: {e}\n")
            continue
    print(f"Finished processing page {page}. Waiting 3 seconds before next request...")
    time.sleep(1)

# get file size
def get_file_size(repo_full_name, file_path, headers):
    if not repo_full_name or not file_path:
        print(f"Error: Missing repo_full_name ({repo_full_name}) or file_path ({file_path}).")
        return None
    url = f"https://api.github.com/repos/{repo_full_name}/contents/{file_path}"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching file size for {repo_full_name}/{file_path}: {response.status_code}")
            return None
        data = response.json()
        if data.get("message") == "This API returns blobs up to 1MB in size.":
            print(f"File too large, fetching size using Blob API...")
            return get_large_file_size(repo_full_name, file_path, headers)
        file_size = data.get("size", None)
        return file_size
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def get_large_file_size(repo_full_name, file_path, headers):
    url = f"https://api.github.com/repos/{repo_full_name}/git/blobs/{file_path}"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            file_size = data.get("size", None)
            return int(file_size)
        else:
            print(f"Error fetching large file size for {repo_full_name}/{file_path}")
            return None
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

# download cursorrules files
def download_file(raw_url, raw_md5, headers):
    response = requests.get(raw_url, headers=headers)

    if response.status_code == 200:
        file_path = os.path.join(save_path, f"{raw_md5}.cursorrules")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Succeed to download {raw_md5}.cursorrules\n")
        return response.text
    else:
        print(f"Failed to download {raw_url}\n")
        return None

def get_commit(conn, headers, file_commits_url, raw_md5, file_path):
    # print(f"\n!!! file_commits_url: {file_commits_url}\n")
    try:
        file_commits_response = requests.get(file_commits_url, headers=headers)
        commits_list = file_commits_response.json()
    except Exception as e:
        print(f"Error fetching commits from URL {file_commits_url}: {e}\n")
        logging.error(f"Error fetching commits from URL {file_commits_url}: {e}\n")
        return {}
    
    commit_timeflow = []
    commit_authors = []
    commit_authors_ids = set()
    commit_messages = []
    commit_commits_count = len(commits_list)
		
    for commit in commits_list:
        commit_sha = ""
        commit_time = None
        commit_author = None
        commit_author_id = None
        commit_message = ""
        commit_comment_count = 0
        v_verified = None
        v_reason = ""
        v_time = None
        commit_url = None
        commit_status = None
        commit_additions = 0
        commit_deletions = 0
        commit_changes = 0
        commit_patch = ""        
        try:
            commit_info = commit.get("commit")
            commit_time = commit_info.get("author").get("date")
            commit_timeflow.append(commit_time)
            commit_comment_count = commit_info.get("comment_count")
            v_verified = commit_info.get("verification", {}).get("verified")
            v_reason = commit_info.get("verification", {}).get("reason")
            v_time = commit_info.get("verification", {}).get("verified_at")
            commit_message = commit_info.get("message") or "(No message provided)"
            commit_messages.append(commit_message)
            commit_sha = commit.get("sha")
            commit_url = commit.get("url")
        
            if commit.get("author") is not None:
                commit_author = commit.get("author").get("login")
                commit_author_id = commit.get("author").get("id")
            else:
                commit_author = "Not Github User"
            commit_authors.append(commit_author)
            commit_authors_ids.add(commit_author_id)
            
            # Generate commit_md5 - the unique id for each commit of each file
            # urls_con = raw_md5 + "|" + commit_sha
            # commit_md5 = genmd5(urls_con)

            # file-level commit details
            print(f"commit_url: {commit_url}.\n")
            try:
                commit_files_response = requests.get(commit_url, headers=headers)
                if commit_files_response.status_code != 200:
                    print(f"Error fetching commit details for {commit_url}")
                    continue    # Skip this commit if details cannot be fetched
                commit_files_list = commit_files_response.json()
            except Exception as e:
                print(f"Error processing commit details for {commit_url}: {e}\n")
                logging.error(f"Error processing commit details for {commit_url}: {e}\n")
                continue
            
            # Loop through files in the commit to find our file
            for file_item in commit_files_list.get("files"):
                if file_item.get("filename") == file_path:
                    commit_status = file_item.get("status")
                    commit_additions = file_item.get("additions")
                    commit_deletions = file_item.get("deletions")
                    commit_changes = file_item.get("changes")
                    commit_patch = file_item.get("patch")
                    # download
                    if commit_patch:
                        patch_path = os.path.join(save_path, f"{raw_md5}_commit_{commit_sha}.txt")
                        try:
                            with open(patch_path, "w", encoding="utf-8") as f:
                                f.write(commit_patch)
                        except Exception as file_error:
                            print (f"Error saving patch for raw_md5 {raw_md5} and commit {commit_sha}: {file_error}\n")
                            logging.error(f"Error saving patch for raw_md5 {raw_md5} and commit {commit_sha}: {file_error}\n")
                    else:
                        print(f"No patch available for raw_md5 {raw_md5} and commit {commit_sha}: {commit_url}\n")
                    break

            # Insert commit data into database
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR IGNORE INTO commits (raw_md5, commit_sha, commit_time, commit_author, commit_author_id, commit_message, commit_comment_count, v_verified, v_reason, v_time, commit_status, commit_additions, commit_deletions, commit_changes, commit_patch, commit_url, file_commits_url)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (raw_md5, commit_sha, commit_time, commit_author, commit_author_id, commit_message, commit_comment_count, v_verified, v_reason, v_time, commit_status, commit_additions, commit_deletions, commit_changes, commit_patch, commit_url, file_commits_url)
                )
                conn.commit()
            except Exception as db_error:
                print(f"Error inserting commit {commit_sha} for raw_md5 {raw_md5} into commits_table: {db_error}\n")
                logging.error(f"Error inserting commit {commit_sha} for raw_md5 {raw_md5} into commits_table: {db_error}\n")
                # Continue processing other commits even if commits_table insertion fails
        except Exception as commit_error:
            print(f"Error processing a commit: {commit_error}\n")
            logging.error(f"Error processing a commit: {commit_error}\n")
            continue    # Skip this commit and continue with the next one
    
    # Determine first and last commit times based on the commit_timeflow list
    if commit_timeflow:
        commit_first_time = min(commit_timeflow)
        commit_last_time = max(commit_timeflow)
        # commit_first_time = commit_timeflow[-1]
        # commit_last_time = commit_timeflow[0]
    else:
        commit_first_time = commit_last_time = None
    
	
    commit_authors_count = len(commit_authors_ids)
    commit_creator = commit_authors[-1] if commit_authors else None

    '''
    if commit_creator.strip() == "Not Github User" or not commit_creator:
        print(f"Skipping metadata fetch for non-GitHub user: {commit_creator}\n")
    if commit_authors and commit_creator != "Not Github User":
        try:
            get_user(conn, headers, raw_md5, commit_creator, 2)
            time.sleep(3)
        except Exception as e:
            print(f"Error fetching user data for {commit_creator}: {e}\n")
            logging.error(f"Error fetching user data for {commit_creator}: {e}\n")
    '''

    commit_return = {
        "file_created_at": commit_first_time,
        "file_last_updated": commit_last_time,
        "file_creator": commit_creator,
        "commit_count": commit_commits_count,
        "commit_authors_count": commit_authors_count,
        "commit_timeflow": commit_timeflow,
        "commit_messages": commit_messages
    }
    return commit_return






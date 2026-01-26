import requests
import sqlite3
import time
import logging




def get_user_from_db(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    fetchone_db = cursor.fetchone()
    '''
    print(f"sha[0]: {fetchone_db[0]}\n")
    print(f"user_id[1]: {fetchone_db[1]}\n")
    print(f"login[2]: {fetchone_db[2]}\n")
    print(f"user_repos[3]: {fetchone_db[3]}\n")
    print(f"user_gists[4]: {fetchone_db[4]}\n")
    print(f"user_followers[5]: {fetchone_db[5]}\n")
    print(f"user_stars[6]: {fetchone_db[6]}\n")
    print(f"user_forks[7]: {fetchone_db[7]}\n")
    print(f"user_open_issues[8]: {fetchone_db[8]}\n")
    print(f"user_created_at[9]: {fetchone_db[9]}\n")
    print(f"user_last_active[10]: {fetchone_db[10]}\n")
    print(f"user_tags_count[11]: {fetchone_db[11]}\n")
    print(f"user_tags[12]: {fetchone_db[12]}\n")
    print(f"user_bio[13]: {fetchone_db[13]}\n")
    print(f"user_organizations_count[14]: {fetchone_db[14]}\n")
    print(f"user_type[15]: {fetchone_db[15]}\n")
    print(f"user_company[16]: {fetchone_db[16]}\n")
    print(f"user_blog[17]: {fetchone_db[17]}\n")
    '''
    return fetchone_db

# -github.com/search?q=awesome-cursorrules&type=repositories
def get_user(conn, headers, raw_md5, login, tag):
    url = f"https://api.github.com/users/{login}"
    try:
        user_response = requests.get(url, headers=headers)
        user_response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"[Error] Failed to fetch user data for {login}: {e}")
        return {}
        
    user_data = user_response.json()
    # print(f"\n\nuser_data: {user_data}\n\n")
    try:
    
        user_id = user_data.get("id")
        user_repos = user_data.get("public_repos")
        user_gists = user_data.get("public_gists")
        user_followers = user_data.get("followers")
        user_created_at = user_data.get("created_at")
        user_last_active = last_active_time(login, headers)
        user_bio = user_data.get("bio")
        user_type = user_data.get("type")
        user_company = user_data.get("company")
        user_blog = user_data.get("blog")
    except KeyError as e:
        logging.error(f"[Error] Missing expected field in user data for {login}: {e}")
        return {}
    
    user_organizations_url = f"https://api.github.com/users/{login}/orgs"
    try:
        res_org = requests.get(f"{user_organizations_url}?per_page=100&page=1", headers=headers).json()
        user_organizations_count = len(res_org) if res_org else 0
    except requests.RequestException as e:
        logging.error(f"[Error] Failed to fetch organizations for {login}: {e}")
        user_organizations_count = 0
      
    user_tags = []
    if user_type == "Organization": user_tags.append("typeOrganization")
    if user_company: user_tags.append("company")
    if user_blog: user_tags.append("blog")
    if user_organizations_url: user_tags.append("inOrganization")
    user_tags_count = len(user_tags)
    user_tags_str = ",".join(user_tags)
    
    # Get repositories' stargazers_count and forks_count
    user_repos_url = user_data.get("repos_url", "")
    try:
        user_repos_data = get_user_repos(headers, user_repos_url)
        user_stars = user_repos_data.get("user_stars")
        user_forks = user_repos_data.get("user_forks")
        user_open_issues = user_repos_data.get("user_open_issues")
    except Exception as e:
        logging.error(f"[Error] Failed to fetch repositories for {login}: {e}\n")
        user_stars = user_forks = user_open_issues = 0

    ### save to SQLite**
    if tag == 1:
        try:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT OR IGNORE INTO users (raw_md5, user_id, user_login, user_repos, user_gists, user_followers, user_stars, user_forks, user_open_issues, user_created_at, user_last_active, user_tags_count, user_tags, user_bio, user_organizations_count, user_type, user_company, user_blog)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (raw_md5, user_id, login, user_repos, user_gists, user_followers, user_stars, user_forks, user_open_issues, user_created_at, user_last_active, user_tags_count, user_tags_str, user_bio, user_organizations_count, user_type, user_company, user_blog)
            )
            conn.commit()
            print("\n ********** user.py: Save new data to table 'users' DONE! **********\n")
        except Exception as e:
            print(f"[Error in user.py]: Failed to save data to table 'users' for {login}: {e}\n")
            logging.error(f"[Error in user.py]: Failed to save data to table 'users' for {login}: {e}\n")
    elif tag == 2:
        try:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT OR IGNORE INTO creators (raw_md5, creator_id, creator_login, creator_repos, creator_gists, creator_followers, creator_stars, creator_forks, creator_open_issues, creator_created_at, creator_last_active, creator_tags_count, creator_tags, creator_bio, creator_organizations_count, creator_type, creator_company, creator_blog)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (raw_md5, user_id, login, user_repos, user_gists, user_followers, user_stars, user_forks, user_open_issues, user_created_at, user_last_active, user_tags_count, user_tags_str, user_bio, user_organizations_count, user_type, user_company, user_blog)
            )
            conn.commit()
            print("\n ********** user.py: Save new data to table 'creators' DONE! **********\n")
        except Exception as e:
            print(f"[Error in user.py]: Failed to save data to table 'creators' for {login}: {e}\n")
            logging.error(f"[Error in user.py]: Failed to save data to table 'creators' for {login}: {e}\n")        
    
    user_return = {
        "user_id": user_id,
        "user_created_at": user_created_at,
        "user_last_active": user_last_active,
        "user_repos": user_repos,
        "user_followers": user_followers,
        "user_gists": user_gists,
        "user_stars": user_stars,
        "user_forks": user_forks,
        "user_tags": user_tags_str
    }
    return user_return


def last_active_time(login, headers):
    url = f"https://api.github.com/users/{login}/events/public"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Get last_active_time for user {login} failed! url: {url}, status_code: {response.status_code}\n")
        res = response.json()
        if res:
            last_active_time = res[0].get('created_at')
            if last_active_time:
                print(f"Use {login} last_active_time: {last_active_time}. URL: {url}\n")
                return last_active_time
        else:
            logging.warning(f"No events found for user {login}.\n")
    except requests.RequestException as e:
        print(f"[Error]: Failed to fetch events for user {login}: {e}\n")
        logging.error(f"[Error]: Failed to fetch events for user {login}: {e}\n")

    return None


def get_user_repos(headers, user_repos_url):
    user_stars = 0
    user_forks = 0
    user_open_issues = 0
    page = 1
    per_page = 100
    while True:
        try:
            response = requests.get(f"{user_repos_url}?per_page={per_page}&page={page}", headers=headers)
            if response.status_code == 403:
                print("\nAPI limitation run out! Please try it later!\n")
                return {"user_stars": user_stars, "user_forks": user_forks, "user_open_issues": user_open_issues}
            
            repos_data = response.json()
            if not repos_data:
                if page == 1:
                    print("\nNo repositories found for this user.\n")
                else:
                    print(f"\nAll repositories fetched in {page-1} pages.\n")
                break
            
            for repo in repos_data:
                user_stars += repo.get("stargazers_count", 0)
                user_forks += repo.get("forks_count", 0)
                user_open_issues += repo.get("open_issues_count", 0)
            
            if "next" not in response.headers.get("Link", ""):
                break
            page += 1
            time.sleep(1)
        except requests.RequestException as e:
            print(f"[Error] Failed to fetch repos for {user_repos_url}: {e}\n")
            logging.error(f"[Error] Failed to fetch repos for {user_repos_url}: {e}\n")
            break
    # print(f"In the function: user_stars: {user_stars}\n")
    # print(f"In the function: user_forks: {user_forks}\n")
    # print(f"In the function: user_open_issues: {user_open_issues}\n")
    return {"user_stars": user_stars, "user_forks": user_forks, "user_open_issues": user_open_issues}


def mainIgnore():
    global headers
    global processed_users
    headers = headers
    # Pre-load processed users
    # load_processed_users()

    conn = sqlite3.connect("/mnt/d/1stp_cursor/crawlerV2.0/user_test/cursor0326_user.db")
    # create_table_users(conn)
    
    '''
    if user_id in processed_users:
        print(f"Skipping duplicate user_id: {user_id}")
        return None
    check_get_user = get_user(conn, headers, "c756764046b1090e9784421c12cd4c14b59798fd", "SilasReinagel", user_id)
    if check_get_user:
        processed_users.add(user_id)
        save_processed_users()
    return check_get_user
    '''
    
    user_id = 16170448
    sha = "1003182ec207e2ffcabffbc9ca085517db8b640c"
    login = "nicholasjprimianomd"
    
    fetchone_db = get_user_from_db(conn, user_id)
    if fetchone_db:
        print(f"User {login} with user_id {user_id} is found in database. Reinserting with new SHA {sha}.")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (sha, user_id, user_login, user_repos, user_gists, user_followers, user_stars, user_forks, user_open_issues, user_created_at, user_last_active, user_tags_count, user_tags, user_bio, user_organizations_count, user_type, user_company, user_blog)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (sha, user_id, login, fetchone_db[3], fetchone_db[4], fetchone_db[5], fetchone_db[6], fetchone_db[7], fetchone_db[8], fetchone_db[9], fetchone_db[10], fetchone_db[11], fetchone_db[12], fetchone_db[13], fetchone_db[14], fetchone_db[15], fetchone_db[16], fetchone_db[17])
        )
        conn.commit()
        print(f"\nNew user data inserted for {login} with user_id {user_id}.\n")
    else:
        print(f"\nUser {login} with user_id {user_id} is not found in database.\n")
        user_return = get_user(conn, headers, sha, login, user_id)
    conn.close()
    
    # last_active_time("SilasReinagel")
    

def main222222222222():
    global headers
    global processed_users
    headers = headers

    # conn = sqlite3.connect("/mnt/d/1stp_cursor/crawlerV2.0/user_test/cursor0326_user.db")
    # create_table_users(conn)
    
    user_id = 16170448
    sha = "1003182ec207e2ffcabffbc9ca085517db8b640c"
    login = "PatrickJS"
    # url = f"https://api.github.com/users/{login}"
    # user_response = requests.get(url, headers=headers)
    # if user_response.status_code != 200:
    #    print("Error:", user_response.status_code, user_response.text)
    #    return []
    # user_data = user_response.json()
    user_organizations_url = f"https://api.github.com/users/{login}/orgs"
    res_org = requests.get(f"{user_organizations_url}?per_page=100&page=1").json()
    if res_org:
        user_organizations_count = len(res_org)
    else:
        user_organizations_count = 0    
    print(f"user_organizations_count: {user_organizations_count}\n")

#if __name__=="__main__":
#    main()

'''
print("\n-------In Main() -------\n")
print(f"user_id[0]: {user_id}\n")
print(f"sha[1]: {sha}\n")
print(f"login[2]: {login}\n")
print(f"user_repos[3]: {fetchone_db[3]}\n")
print(f"user_gists[4]: {fetchone_db[4]}\n")
print(f"user_followers[5]: {fetchone_db[5]}\n")
print(f"user_stars[6]: {fetchone_db[6]}\n")
print(f"user_forks[7]: {fetchone_db[7]}\n")
print(f"user_open_issues[8]: {fetchone_db[8]}\n")
print(f"user_created_at[9]: {fetchone_db[9]}\n")
print(f"user_last_active[10]: {fetchone_db[10]}\n")
print(f"user_tags_count[11]: {fetchone_db[11]}\n")
print(f"user_tags[12]: {fetchone_db[12]}\n")
print(f"user_bio[13]: {fetchone_db[13]}\n")
print(f"user_organizations_count[14]: {fetchone_db[14]}\n")
print(f"user_type[15]: {fetchone_db[15]}\n")
print(f"user_company[16]: {fetchone_db[16]}\n")
print(f"user_blog[17]: {fetchone_db[17]}\n")
'''
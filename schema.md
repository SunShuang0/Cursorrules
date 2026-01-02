# Database Structure

## Table: files
```sql
CREATE TABLE files (
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
        );
```

## Table: repos
```sql
CREATE TABLE repos (
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
        );
```

## Table: users
```sql
CREATE TABLE users (
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
        );
```

## Table: creators
```sql
CREATE TABLE creators (
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
        );
```

## Table: commits
```sql
CREATE TABLE commits (
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
        );
```

## Table: repo_size
```sql
CREATE TABLE repo_size (
            repo_id INTEGER PRIMARY KEY,
            repo_files_count INTEGER
        );
```


import os
import sqlite3
import requests
import time
import zipfile
import io
import logging

# ========== 配置 ==========
DB_PATH = "/mnt/d/1stp_cursor/5.0crawler/final_repo_size3.db"
GITHUB_TOKEN = "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"
GITHUB_API = "https://api.github.com"

HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"token {GITHUB_TOKEN}",
    "User-Agent": "RepoFileCounter"
}

ZIP_TMP_DIR = "./tmp_zips"
SAVE_BATCH = 5
REQUEST_INTERVAL = 2
# Thresholds
MEMORY_ZIP_LIMIT_MB = 500
DISK_ZIP_LIMIT_MB = 2048
SKIP_ZIP_LIMIT_MB = 2048

# ========== Logging ==========
logging.basicConfig(
    filename="repo_size3_1025.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ============================================================
# 模块 A：数据库接口层
# ============================================================

def get_unprocessed_repos(conn):
    cursor = conn.cursor()
    query = """
        SELECT r.repo_id, r.repo_owner, r.repo_name, r.repo_size,
               r.repo_owner_id, r.repo_topics, r.repo_license
        FROM repos r
        LEFT JOIN repo_size rs ON r.repo_id = rs.repo_id
        WHERE rs.repo_id IS NULL
        ORDER BY r.repo_id
    """
    return cursor.execute(query).fetchall()

def save_repo_sizes(conn, results):
    cursor = conn.cursor()
    cursor.executemany(
        "INSERT OR REPLACE INTO repo_size (repo_id, repo_files_count) VALUES (?, ?)",
        results
    )
    conn.commit()

# ============================================================
# 模块 B：仓库有效性检测
# ============================================================

def check_repo_status(owner, name):
    """Check repo exists or not"""
    url = f"{GITHUB_API}/repos/{owner}/{name}"
    resp = requests.get(url, headers=HEADERS)
    time.sleep(REQUEST_INTERVAL)

    if resp.status_code == 404:
        return {"status": "not_found"}
    if resp.status_code != 200:
        logging.warning(f"{owner}/{name} API Error: {resp.status_code}")
        return {"status": "error"}

    data = resp.json()
    if data.get("private"):
        return {"status": "private"}
    if data.get("archived"):
        return {"status": "archived"}

    size_kb = data.get("size", 0)
    return {"status": "valid", "size_mb": size_kb / 1024.0}

# ============================================================
# 模块 C：ZIP 下载 + 文件计数
# ============================================================

def count_files_via_zip_memory(owner, name):
    url = f"{GITHUB_API}/repos/{owner}/{name}/zipball"
    resp = requests.get(url, headers=HEADERS, stream=True)
    time.sleep(REQUEST_INTERVAL)
    if resp.status_code != 200:
        logging.warning(f"{owner}/{name} zipball download failed: {resp.status_code}")
        return None
    with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
        files = [f for f in z.namelist() if not f.endswith("/")]
        return len(files)

def count_files_via_zip_disk(owner, name):
    os.makedirs(ZIP_TMP_DIR, exist_ok=True)
    url = f"{GITHUB_API}/repos/{owner}/{name}/zipball"
    zip_path = os.path.join(ZIP_TMP_DIR, f"{owner}-{name}.zip")

    with requests.get(url, headers=HEADERS, stream=True) as r:
        if r.status_code != 200:
            logging.warning(f"{owner}/{name} zipball download failed: {r.status_code}")
            return None
        with open(zip_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    time.sleep(REQUEST_INTERVAL)

    try:
        with zipfile.ZipFile(zip_path) as z:
            files = [f for f in z.namelist() if not f.endswith("/")]
            return len(files)
    finally:
        os.remove(zip_path)  # remove after downloaded

# ============================================================
# 模块 E：跳过日志
# ============================================================

def log_skip(repo_id, owner, name, reason):
    with open("skipped_repos_1025.txt", "a", encoding="utf-8") as f:
        f.write(f"{repo_id},{owner}/{name},{reason}\n")

# ============================================================
# 模块 F：主流程控制
# ============================================================

def main():
    print("="*60)
    print("启动仓库文件统计脚本（低成本模式）")
    print("="*60)

    conn = sqlite3.connect(DB_PATH)
    repos = get_unprocessed_repos(conn)
    print(f"总待处理仓库数: {len(repos)}")

    results = []
    processed = 0

    for index, (repo_id, owner, name, size_kb, *_ ) in enumerate(repos, start=1):
        print(f"\n[{index}/{len(repos)}] 检查 {owner}/{name} ...")

        status = check_repo_status(owner, name)
        if status["status"] != "valid":
            log_skip(repo_id, owner, name, status["status"])
            continue

        repo_size_mb = status["size_mb"]
        print(f"仓库大小约 {repo_size_mb:.2f} MB")

        count = None  # ← Initialize

        # Step 1：≤500 → Memory ZIP
        if repo_size_mb <= MEMORY_ZIP_LIMIT_MB:
            count = count_files_via_zip_memory(owner, name)

        # Step 2：500 - 2048 → Disk ZIP
        elif repo_size_mb <= DISK_ZIP_LIMIT_MB:
            count = count_files_via_zip_disk(owner, name)

        # Step 3：> 2048MB → Skip and record
        else:
            log_skip(repo_id, owner, name, f"too_large_{repo_size_mb:.2f}MB")
            print(f"⚠️ Skip huge repo: {repo_size_mb:.2f} MB")
            continue

        # Step 4：Store into database if successed
        if count is not None:
            results.append((repo_id, count))
            print(f"✅ Success: {count} files")

        # Step 5: Store to database every five records
        if len(results) >= SAVE_BATCH:
            save_repo_sizes(conn, results)
            processed += len(results)
            print(f"💾 Stored {processed} items to database.")
            results = []

    if results:
        save_repo_sizes(conn, results)
        print(f"💾 The last batch of {len(results)} items are saved.")

    conn.close()
    print("✅ All done.")

# ============================================================
if __name__ == "__main__":
    main()
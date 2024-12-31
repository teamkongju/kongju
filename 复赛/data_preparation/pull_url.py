import csv
import requests


def get_active_repositories(token, page_size=100, num_repos=1000):
    base_url = "https://api.github.com/search/repositories"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    params = {
        "q": "stars:>1",  # 搜索有至少一个 star 的仓库，可根据需要调整
        "sort": "updated",  # 按更新时间排序，代表活跃度
        "order": "desc",  # 降序排列
        "per_page": page_size  # 每页的结果数量
    }
    repo_urls = []
    page = 1
    while len(repo_urls) < num_repos:
        params["page"] = page
        try:
            response = requests.get(base_url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            items = data.get('items', [])
            if not items:  # 如果没有更多结果，退出循环
                break
            for item in items:
                repo_urls.append(item['html_url'])
            page += 1
        except requests.RequestException as e:
            print(f"请求出错（第{page}页）: {e}")
            break
    return repo_urls[:num_repos]


# 使用你提供的个人访问令牌
token = "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"
active_repos = get_active_repositories(token)


# 写入 CSV 文件
with open('active_repos_urls.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Repository URL'])  # 写入表头
    for url in active_repos:
        writer.writerow([url])

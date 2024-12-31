import csv
import requests
from tqdm import tqdm


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
    # 使用 tqdm 显示获取页面的进度
    with tqdm(total=num_repos, desc="获取仓库页面", unit="页") as pbar_page:
        while len(repo_urls) < num_repos:
            params["page"] = page
            try:
                response = requests.get(base_url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()
                items = data.get('items', [])
                if not items:  # 如果没有更多结果，退出循环
                    break
                # 使用 tqdm 显示添加仓库 URL 的进度
                with tqdm(total=len(items), desc=f"添加仓库 URL (第{page}页)", leave=False, unit="URL") as pbar_url:
                    for item in items:
                        repo_urls.append(item['html_url'])
                        pbar_url.update(1)
                page += 1
                pbar_page.update(len(items))
            except requests.RequestException as e:
                print(f"请求出错（第{page}页）: {e}")
                break
    return repo_urls[:num_repos]


def fetch_issues_by_label(token, repo_urls, target_labels):
    all_issue_info_list = []
    label_mapping = {
        'bug': 'bug',
        'enhancement': 'enhancement',
        'question': 'question',
        'Bug': 'bug',
        'Enhancement': 'enhancement',
        'Question': 'question',
        'BUG': 'bug',
        'ENHANCEMENT': 'enhancement',
        'QUESTION': 'question'
    }
    for repo_url in tqdm(repo_urls, desc="处理仓库", unit="仓库"):
        try:
            owner, repo = repo_url.split('/')[-2:]
            issues_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
            headers = {
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json"
            }
            page = 1
            while True:
                params = {
                    "page": page,
                    "per_page": 100
                }
                response = requests.get(issues_url, headers=headers, params=params)
                response.raise_for_status()
                issues = response.json()
                if not issues:
                    break
                for issue in issues:
                    labels = [label_mapping[label['name']] if label['name'] in label_mapping else label['name'] for label in issue.get('labels', [])]
                    if any(label in target_labels for label in labels):
                        issue_info = {
                            "issue_url": issue['html_url'],
                            "issue_created_at": issue['created_at'],
                            "issue_author_association": issue['author_association'],
                            "repository_url": repo_url,
                            "issue_title": issue['title'],
                            "issue_body": issue['body'] if issue['body'] else "",
                            "issue_label": labels
                        }
                        all_issue_info_list.append(issue_info)
                page += 1
        except requests.RequestException as e:
            print(f"请求仓库 {repo_url} 的 issue 列表出错: {e}")
        except Exception as e:
            print(f"处理仓库 {repo_url} 时出错: {e}")
    return all_issue_info_list


def write_issues_to_csv(issue_infos, output_file):
    fieldnames = ['issue_url', 'issue_created_at', 'issue_author_association', 'repository_url', 'issue_title', 'issue_body', 'issue_label']
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for info in tqdm(issue_infos, desc="写入文件", unit="行"):
            writer.writerow(info)


if __name__ == "__main__":
    token = "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"
    target_labels = ['bug', 'enhancement', 'question']  # 目标 label 统一为小写
    active_repos = get_active_repositories(token)
    issue_infos = fetch_issues_by_label(token, active_repos, target_labels)
    write_issues_to_csv(issue_infos, 'filtered_issues.csv')

import pandas as pd
import csv
from tqdm import tqdm  # 用于显示进度条

# 定义输入和输出文件路径
input_file_path = r'top300_20_23_1681699961594.csv'
output_file_path = r'new_log_2020_01.csv'

# 定义每个数据块的行数
chunksize = 10000

# 打开输出文件以写入，模式为'w'表示写入模式，如果文件已存在则覆盖
with open(output_file_path, 'w', newline='', encoding='utf-8') as output_file:
    # 创建一个csv.writer对象用于写入输出文件
    output_writer = csv.writer(output_file)
    
    # 写入输出文件的表头（可选，但推荐执行，以确保输出文件的列顺序正确）
    header = ['id', 'type', 'action', 'actor_id', 'actor_login', 'repo_id', 'repo_name', 'org_id', 'org_login', 'created_at', 'issue_id', 'issue_number', 'issue_title', 'body', 'issue_labels_name', 'issue_labels_color', 'issue_labels_default', 'issue_labels_description', 'issue_author_id', 'issue_author_login', 'issue_author_type', 'issue_author_association', 'issue_assignee_id', 'issue_assignee_login', 'issue_assignees_login', 'issue_assignees_id', 'issue_created_at', 'issue_updated_at', 'issue_comments', 'issue_closed_at', 'issue_comment_id', 'issue_comment_created_at', 'issue_comment_updated_at', 'issue_comment_author_association', 'issue_comment_author_id', 'issue_comment_author_login', 'issue_comment_author_type', 'pull_commits', 'pull_additions', 'pull_deletions', 'pull_changed_files', 'pull_merged', 'pull_merge_commit_sha', 'pull_merged_at', 'pull_merged_by_id', 'pull_merged_by_login', 'pull_merged_by_type', 'pull_requested_reviewer_id', 'pull_requested_reviewer_login', 'pull_requested_reviewer_type', 'pull_review_comments', 'repo_description', 'repo_size', 'repo_stargazers_count', 'repo_forks_count', 'repo_language', 'repo_has_issues', 'repo_has_projects', 'repo_has_downloads', 'repo_has_wiki', 'repo_has_pages', 'repo_license', 'repo_default_branch', 'repo_created_at', 'repo_updated_at', 'repo_pushed_at', 'pull_review_state', 'pull_review_author_association', 'pull_review_id', 'pull_review_comment_id', 'pull_review_comment_path', 'pull_review_comment_position', 'pull_review_comment_author_id', 'pull_review_comment_author_login', 'pull_review_comment_author_type', 'pull_review_comment_author_association', 'pull_review_comment_created_at', 'pull_review_comment_updated_at', 'push_id', 'push_size', 'push_distinct_size', 'push_ref', 'push_head', 'push_commits_name', 'push_commits_email', 'push_commits_message', 'fork_forkee_id', 'fork_forkee_full_name', 'fork_forkee_owner_id', 'fork_forkee_owner_login', 'fork_forkee_owner_type', 'delete_ref', 'delete_ref_type', 'delete_pusher_type', 'create_ref', 'create_ref_type', 'create_master_branch', 'create_description', 'create_pusher_type', 'gollum_pages_page_name', 'gollum_pages_title', 'gollum_pages_action', 'member_id', 'member_login', 'member_type', 'release_id', 'release_tag_name', 'release_target_commitish', 'release_name', 'release_draft', 'release_author_id', 'release_author_login', 'release_author_type', 'release_prerelease', 'release_created_at', 'release_published_at', 'release_body', 'release_assets_name', 'release_assets_uploader_login', 'release_assets_uploader_id', 'release_assets_content_type', 'release_assets_state', 'release_assets_size', 'release_assets_download_count', 'commit_comment_id', 'commit_comment_author_id', 'commit_comment_author_login', 'commit_comment_author_type', 'commit_comment_author_association', 'commit_comment_path', 'commit_comment_position', 'commit_comment_line', 'commit_comment_created_at', 'commit_comment_updated_at', 'pt']
    output_writer.writerow(header)
    
    # 使用chunksize参数逐块读取输入文件
    for chunk in pd.read_csv(input_file_path, chunksize=chunksize):
        # 过滤出type列内容为IssueCommentEvent的行
        filtered_chunk = chunk[chunk['type'] == 'IssueCommentEvent']
        
        # 将过滤后的DataFrame逐行转换为csv格式并写入输出文件
        for _, row in filtered_chunk.iterrows():
            output_writer.writerow(row.tolist())

print("过滤完成，新文件已保存为new_log_2020_01.csv")

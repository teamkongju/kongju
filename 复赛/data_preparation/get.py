import pandas as pd
from tqdm import tqdm


def main(csv_file_path, output_file_path, chunksize=1000):
    fieldnames = ['issue_url', 'issue_label', 'issue_created_at', 'issue_author_association', 
                 'repository_url', 'issue_title', 'issue_body']
    # 先将表头写入文件
    with open(output_file_path, mode='w', newline='', encoding='utf-8') as output_file:
        writer = pd.DataFrame(columns=fieldnames).to_csv(output_file, index=False)
    
    # 计算文件的行数
    total_rows = sum(1 for _ in open(csv_file_path, encoding='utf-8')) - 1  # 减去表头行
    total_chunks = (total_rows // chunksize) + (1 if total_rows % chunksize > 0 else 0)
    
    # 逐块读取输入文件，并使用 tqdm 显示进度
    with tqdm(total=total_chunks, desc="Processing rows") as pbar:
        for chunk in pd.read_csv(csv_file_path, chunksize=chunksize, encoding='utf-8'):
            extracted_data = []
            for index, row in chunk.iterrows():
                # 构建 issue_url
                issue_url = f"https://github.com/{row['org_login']}/{row['repo_name']}/issues/{row['issue_number']}"
                # 提取 issue_label，将列表转换为逗号分隔的字符串
                issue_label = ",".join(row['issue_labels_name'].strip('[]').replace('"', '').split(','))
                issue_created_at = row['issue_created_at']
                issue_author_association = row['issue_author_association']
                # 构建 repository_url
                repository_url = f"https://github.com/{row['org_login']}/{row['repo_name']}"
                issue_title = row['issue_title']
                issue_body = row['body']
                
                # 过滤 issue_label 为 ["bug"]、["question"] 或 ["enhancement"] 的行
                if issue_label in ["bug", "question", "enhancement"]:
                    extracted_data.append({
                        'issue_url': issue_url,
                        'issue_label': issue_label,
                        'issue_created_at': issue_created_at,
                        'issue_author_association': issue_author_association,
                        'repository_url': repository_url,
                        'issue_title': issue_title,
                        'issue_body': issue_body
                    })
            # 将提取的数据写入输出文件
            if extracted_data:
                with open(output_file_path, mode='a', newline='', encoding='utf-8') as output_file:
                    pd.DataFrame(extracted_data).to_csv(output_file, header=False, index=False)
            pbar.update(1)


if __name__ == "__main__":
    csv_file_path = 'new_log_2020_01.csv'  # 输入 CSV 文件的实际路径
    output_file_path = 'output.csv'  # 输出 CSV 文件的路径
    main(csv_file_path, output_file_path, chunksize=1000)

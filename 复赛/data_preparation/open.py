import csv
from tqdm import tqdm  # 用于显示进度条

# 定义输入和输出CSV文件的路径
input_file_path = r'output.csv'  # 输入文件路径
output_file_path = r'open.csv'  # 输出文件路径

# 打开输入CSV文件
with open(input_file_path, newline='', encoding='utf-8') as input_csvfile:
    csvreader = csv.reader(input_csvfile)
    
    # 打开输出CSV文件以写入
    with open(output_file_path, 'w', newline='', encoding='utf-8') as output_csvfile:
        csvwriter = csv.writer(output_csvfile)
        
        # 读取并写入前几行
        for row_num, row in enumerate(csvreader, start=1):
            if row_num > 100:  # 只写入前100行
                break
            csvwriter.writerow(row)  # 将每行的数据写入输出文件

# 注意：这里没有打印到控制台的代码，所有数据都被写入到了输出CSV文件中

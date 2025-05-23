import re
from datasets import load_dataset, load_from_disk
import pandas as pd

# 设置自定义缓存目录
# os.environ['HF_DATASETS_CACHE'] = r'E:\project\Work\education\BERTopic\data'
csv_path = 'coursera_courses_cleaned.csv'
# ds = load_dataset("azrai99/coursera-course-dataset")
ds = load_from_disk(r"E:\project\Work\education\BERTopic\data\coursera\azrai99___coursera-course-dataset\default\0.0.0\repaired") # 本地读取
train_data = ds['train']
# 查看特征信息
print(train_data.info)
# print(train_data[378])  # 查看某个问题样本，如4091

# 转换为 Pandas DataFrame
df = pd.DataFrame(train_data)

# 清洗 'title' 字段，去除换行符
df['title'] = df['title'].str.replace('\r\n', ' ').str.replace('\n', ' ').str.replace('\r', ' ').str.replace('\t', ' ')

# 清洗 'enrolled' 字段
df['enrolled'] = df['enrolled'].replace('Enrollment number not found', pd.NA)
 
# 清洗 'rating' 字段
df['rating'] = df['rating'].replace('Rating not found', pd.NA)

# 清洗 'Organization' 字段
df['Organization'] = df['Organization'].replace('Organization not found', pd.NA)

# 清洗 'Instructor' 字段
df['Instructor'] = df['Instructor'].replace('Instructor not found', pd.NA)

# 清洗 'Description' 字段，去除换行符
df['Description'] = df['Description'].str.replace('\r\n', ' ').str.replace('\n', ' ').str.replace('\r', ' ').str.replace('\t', ' ').str.strip()

# 保存清洗后的数据
df.to_csv(csv_path, index=False)

import csv
 
def check_csv_for_issues(csv_path):
    # 读取 CSV 文件
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # 读取标题行
        expected_columns = len(header)
        
        # 找到 'Modules/Courses' 列的索引
        try:
            modules_index = header.index('Modules/Courses')
            url_index = header.index('URL')
        except ValueError:
            print("Column 'Modules/Courses' not found in the CSV file.")
            return
 
        for i, row in enumerate(reader):
            if len(row) != expected_columns:
                print(f"Line {i + 2} has an incorrect number of columns: {len(row)}")
            
            # 检查 'Modules/Courses' 列是否为空
            if len(row) > modules_index and row[modules_index].strip() == '':
                print(f"Line {i + 2} has an empty 'Modules/Courses' value.")
                print(f"Unnamed: {row[0]}, Name: {row[1]}, Url: {row[-2]}") 

            # 检查 'URL' 列是否为空
            if len(row) > url_index and row[url_index].strip() == '':
                print(f"Line {i + 2} has an empty 'URL' value.")
                print(f"Unnamed: {row[0]}, Name: {row[1]}, Url: {row[-2]}")
 
    print("CSV file check completed.")
 
# 调用检查函数
check_csv_for_issues('coursera_courses_cleaned.csv')

# 以下是修复缺少 Modules/Courses 列的课程，404的课程和没有目录的课程设为 0 module，然后保存到新的数据集。
# 我们没有修复缺少description的片段，因为原数据集将目录描述和每个module描述以及该module的资源统计都加上了，导致噪声太多，所以用新的爬虫数据
# from datasets import load_dataset, Dataset, DatasetDict
# import pandas as pd# # 1. 加载原始数据集
# ds = load_dataset(r"E:\project\Work\education\BERTopic\data\coursera\azrai99___coursera-course-dataset\default\0.0.0\ccd36c1660fee9610d5262e7517d8397c343168b")
# df = pd.DataFrame(ds['train'])
# repaired = {
#     378: '6 modules',
#     790: '4 modules',
#     1073: '4 modules',
#     1540: '4 modules',
#     2544: '4 module',
#     2868: '0 modules',
#     3044: '3 modules',
#     4669: '0 modules',
#     5438: '4 module',
#     5534: '0 module',
# }

# # 3. 更新 DataFrame
# df['Unnamed: 0'] = df['Unnamed: 0']
# for index, modules in repaired.items():
#     df.loc[df['Unnamed: 0'] == index, 'Modules/Courses'] = modules

# # 4. 转换回 Dataset 对象
# updated_dataset = Dataset.from_pandas(df)

# # 创建一个包含更新后数据的新 DatasetDict 对象
# updated_dataset_dict = DatasetDict({
#     'train': updated_dataset
# })

# # 5. 保存到修复路径
# updated_dataset_dict.save_to_disk(r"E:\project\Work\education\BERTopic\data\coursera\azrai99___coursera-course-dataset\default\0.0.0\repaired")


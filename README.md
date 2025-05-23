# Raw
**Project name** : 
Coursera-Course-Dataset

**Publication:** https://medium.com/analytics-vidhya/web-scraping-and-coursera-8db6af45d83f

**Description** : 
The project aims to scrap through data from website of Coursera and generate a csv file for its analysis.

**Table of Contents** :
 
 1. scrapping_coursera.py : Used for scrapping
  
 2. UCoursera_Courses.csv : The final scrapped CSV file.
 
 **Libraries used** :
 
 https://pypi.org/project/beautifulsoup4/
 


**Usage** : 
Csv can be used for data analysis and to bring out insights about courses.

**Contributing** : 
Feel free to fork and add more code to scrap more data for better csv.


# New
**Project name** : 
Coursera-Course-Dataset-TableofContents

**Dataset**: [Coursera Courses on Hugging Face](https://huggingface.co/datasets/azrai99/coursera-course-dataset)
 
## 📌 项目核心
通过爬取Coursera课程页面，为现有课程数据集补充**课程目录结构**信息，生成含章节/模块的增强版CSV文件，支持课程内容分析。
 
## 🚀 快速使用
1. **准备数据**  
   运行`fetch_huggingface_dataset.py`自动：
   - 加载原始数据集
   - 清洗文本字段（Title/Description）
   - 修复缺失值（Modules/Courses）
   - 验证关键字段完整性
 
2. **爬取目录**  
   执行`crawling_coursera_by_url.py`：
   ```bash
   python crawling_coursera_by_url.py

## 🔧 技术栈
```bash
    pip install beautifulsoup4 requests pandas tqdm datasets
```
## 🆕 近期改进
   - 数据清洗增强：修复缺失模块数、处理特殊字符、标准化空值
   - 健壮性提升：增加URL有效性检查、目录结构容错处理
   - 验证机制：添加CSV格式校验和关键字段存在性检查

## 📊 输出示例
```csv
    "CUID": "understanding-fitness-programming",
    "Class": "Health",
    "Subject": "Basic Science",
    "CourseContents": [
        {
            "chapter": "Introduction",
            "sections": [
                {
                    "section": "What is Algorithms?",
                    "subsection": []
                }
            ]
        }
    ]
```

## 🤝 参与贡献
   - Fork仓库
   - 添加新特性（如讲师信息爬取）
   - 提交PR时附带测试数据
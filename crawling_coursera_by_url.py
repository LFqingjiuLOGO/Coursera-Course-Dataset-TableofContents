from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import json

from tqdm import tqdm

def parse_course_content(url):
    """解析单个课程页面的目录结构"""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 定位目录容器
        modules_div = soup.find('div', id='modules')
        if not modules_div:
            return None
        contents_div = modules_div.find('div', class_='css-fndret')
        if not contents_div:
            return None
        course_contents = []
        description_div = modules_div.find('div', class_='content-inner')
        # 提取所有 p 标签的文字内容，并过滤掉空字符串
        paragraphs = [p.get_text(strip=True) for p in description_div.find_all('p') if p.get_text(strip=True)]
        # 合并成一段，每段之间用单个空格分隔，确保没有换行符或多余空白
        description = ' '.join(paragraphs).replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
        # print(description)


        # 遍历每个章节模块
        for chapter_div in contents_div.contents:
            # 提取章节标题
            chapter_title = chapter_div.find('h3').get_text(strip=True)
            # chapter_desc = chapter_div.find('p', class_='css-4s48ix').get_text(strip=True)
            # print(chapter_title)
            # print(chapter_desc)
            unique_sections = set()
            
            # 收集所有唯一的章节名称
            for li in chapter_div.find_all('li'):
                # 获取所有文本节点
                texts = li.find_all(string=True, recursive=False)
                # 提取第一个非空文本节点
                first_sentence = next((text.strip() for text in texts if text.strip()), None)
                if first_sentence:
                    unique_sections.add(first_sentence)
            
            # 生成sections列表
            sections = []
            for section_name in unique_sections:
                sections.append({
                    'section': section_name,
                    'subsections': []
                })

            course_contents.append({
                'chapter': chapter_title,
                'sections': sections
            })
        
        return course_contents, description
    
    except Exception as e:
        print(f"Error parsing {url}: {str(e)}")
        return None

def generate_cuid(url):
    parsed_url = urlparse(url)
    path = parsed_url.path.strip('/')
    parts = path.split('/')
    return parts[-1]

# 主程序
if __name__ == "__main__":
    # 读取课程信息 CSV
    course_info_df = pd.read_csv('coursera_courses_cleaned.csv')
    
    # 存储课程信息的列表
    courses_data = []
 
    # 使用 tqdm 显示进度条
    for idx, row in tqdm(course_info_df.iterrows(), total=len(course_info_df), desc="Processing Courses"):
        type = row['Modules/Courses']
        if not 'modules' in type.lower():
            continue
        if type.lower().strip() == '0 module':
            continue
        # if idx > 1: # 测试用
        #     break
 
        link = row['URL']
        # print(f"\nProcessing course {idx+1}/{len(course_info_df)}: {link}")
        
        # 获取课程基础信息
        try:
            response = requests.get(link)
            response.raise_for_status()  # 检查请求是否成功
            soup = BeautifulSoup(response.content, 'html.parser')
 
            navigation = soup.find('nav', class_='css-m5ieuv')
            
            # 提取导航步骤
            steps = []
            if navigation:
                # 找到导航列表中的所有列表项
                list_items = navigation.find_all('li')
                for item in list_items:
                    # 找到每个列表项中的链接
                    link_tag = item.find('a')
                    if link_tag:
                        # 提取链接文本
                        step_text = link_tag.get_text(strip=True)
                        steps.append(step_text)
            course_class = steps[-2] if len(steps) >= 2 else ''
            course_subject = steps[-1] if len(steps) >= 1 else ''
 
            # 提取现有字段
            course_title = soup.find('h1').get_text(strip=True)
            
            # 提取目录
            content, description = parse_course_content(link)
            
            # 从当前行中提取 Skills 和 Description
            skills = row['Skills']
            # description = row['Description']
 
            courses_data.append({
                'CUID': generate_cuid(link),
                'Class': course_class,
                'Subject': course_subject,
                'SubjectInfo': skills,
                'CourseName': course_title,
                'CourseContents': json.dumps(content, ensure_ascii=False) if content else None,
                'CourseContentsPlain': '',
                'Url': link,
                'Description': description
            })
            
            # print(f"Successfully parsed {course_title}")
            time.sleep(1)  # 礼貌性延迟
            
        except requests.exceptions.RequestException as e:
            print(f"id {row['Unnamed: 0']}: Failed to access url: {link}: {str(e)}")
            continue
        except Exception as e:
            print(f"id {row['Unnamed: 0']}: Failed to parse {link}: {str(e)}")
            continue
 
        # 每处理50门课程后保存一次
        if (idx + 1) % 50 == 0:
            df = pd.DataFrame(courses_data)
            df.to_csv(f'Coursera_Courses_with_TableofContents.csv', index=False, encoding='utf-8-sig')
            print(f"Saved progress at course {idx + 1}")
 
    # 最终保存
    df = pd.DataFrame(courses_data)
    df.to_csv('Coursera_Courses_with_TableofContents.csv', index=False, encoding='utf-8-sig')
    print("\nDone! Check Coursera_Courses_with_Contents.csv")
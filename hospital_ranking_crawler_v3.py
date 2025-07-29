#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
医院排行榜爬虫脚本（V3）
专门处理医院排行榜数据，按照指定格式输出CSV文件
"""
import requests
import csv
import os
import re
from bs4 import BeautifulSoup
import time

def get_page_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        return response.text
    except Exception as e:
        print(f"获取页面失败 {url}: {e}")
        return None

def clean_text(text):
    return re.sub(r'[\r\n\t\xa0\u3000]+', '', text).strip()

def extract_comprehensive_ranking(soup):
    """提取综合排行榜数据"""
    tables = soup.find_all('table')
    
    # 查找包含"等级"和"医院"表头的表格
    for i, table in enumerate(tables):
        rows = table.find_all('tr')
        if len(rows) > 0:
            first_row = rows[0]
            cells = first_row.find_all(['td', 'th'])
            headers = [clean_text(cell.get_text()) for cell in cells]
            
            if '等级' in headers and '医院' in headers:
                print(f"找到综合排行榜表格: 表格{i+1}")
                
                data = []
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    row_data = [clean_text(cell.get_text()) for cell in cells]
                    if any(row_data) and len(row_data) >= 2:
                        data.append(row_data)
                
                if len(data) > 1:
                    return data
    
    return []

def extract_specialty_ranking(soup, is_national=False):
    """提取专科声誉排行榜数据"""
    text = soup.get_text()
    
    # 定义科室列表
    departments = [
        '病理科', '传染感染', '耳鼻喉科', '放射科', '呼吸科', '风湿病', '妇产科', '骨科', 
        '精神医学', '口腔科', '麻醉科', '泌尿外科', '内分泌', '皮肤科', '普通外科', 
        '神经内科', '肾脏病', '神经外科', '消化病', '小儿内科', '小儿外科', '心血管病', 
        '心外科', '胸外科', '血液学', '眼科', '整形外科', '肿瘤学', '老年医学', '康复医学', 
        '检验医学', '烧伤科', '核医学', '超声医学', '急诊医学', '重症医学', '临床药学',
        '生殖医学', '变态反应', '健康管理', '结核病', '全科医学', '疼痛学', '运动医学', '罕见病'
    ]
    
    data = []
    
    for dept in departments:
        # 查找科室数据
        pattern = f"{dept}医院名.*?平均声誉值"
        match = re.search(pattern, text)
        if match:
            start_pos = match.start()
            # 提取该科室的所有数据
            dept_text = text[start_pos:start_pos + 5000]  # 取足够长的文本
            
            # 提取排名和医院信息
            if is_national:
                # 全国专科声誉排行榜格式
                rank_pattern = r'(\d+)\s*([^0-9\n]+?)\s*(\d+\.\d+)'
                matches = re.findall(rank_pattern, dept_text)
                for rank, hospital, score in matches:
                    hospital = clean_text(hospital)
                    if hospital and len(hospital) > 2:
                        data.append([dept, rank, hospital, score])
            else:
                # 区域专科声誉排行榜格式
                rank_pattern = r'(\d+)\s*([^0-9\n]+?)(?=\d+|$)'
                matches = re.findall(rank_pattern, dept_text)
                for rank, hospital in matches:
                    hospital = clean_text(hospital)
                    if hospital and len(hospital) > 2:
                        data.append([dept, rank, hospital])
    
    return data

def parse_and_save_table(url, filename, ranking_type):
    """解析并保存表格数据"""
    html = get_page_content(url)
    if not html:
        print(f"无法获取 {url}")
        return False
    
    soup = BeautifulSoup(html, 'html.parser')
    
    if ranking_type == "comprehensive":
        # 综合排行榜
        data = extract_comprehensive_ranking(soup)
        if data:
            with open(filename, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['等级', '医院'])
                for row in data[1:]:  # 跳过表头
                    if len(row) >= 2:
                        writer.writerow([row[0], row[1]])
            print(f"已保存: {filename}，共{len(data)-1}条数据")
            return True
    else:
        # 专科声誉排行榜
        is_national = (ranking_type == "national")
        data = extract_specialty_ranking(soup, is_national)
        if data:
            with open(filename, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                if is_national:
                    writer.writerow(['科室', '排名', '医院名称', '平均声誉值'])
                else:
                    writer.writerow(['科室', '排名', '医院名称'])
                writer.writerows(data)
            print(f"已保存: {filename}，共{len(data)}条数据")
            return True
    
    print(f"未找到有效数据: {filename}")
    return False

def main():
    url_map = [
        ("https://www.fdygs.com/news2023-1.aspx", "2023年度中国医院专科声誉排行榜.csv", "national"),
        ("https://www.fdygs.com/news2023-2.aspx", "2023年度中国医院综合排行榜.csv", "comprehensive"),
        ("https://www.fdygs.com/news2023-1-11.aspx", "2023年度东北区专科声誉排行榜.csv", "regional"),
        ("https://www.fdygs.com/news2023-1-21.aspx", "2023年度华北区专科声誉排行榜.csv", "regional"),
        ("https://www.fdygs.com/news2023-1-31.aspx", "2023年度华东区专科声誉排行榜.csv", "regional"),
        ("https://www.fdygs.com/news2023-1-41.aspx", "2023年度华南区专科声誉排行榜.csv", "regional"),
        ("https://www.fdygs.com/news2023-1-51.aspx", "2023年度华中区专科声誉排行榜.csv", "regional"),
        ("https://www.fdygs.com/news2023-1-61.aspx", "2023年度西北区专科声誉排行榜.csv", "regional"),
        ("https://www.fdygs.com/news2023-1-71.aspx", "2023年度西南区专科声誉排行榜.csv", "regional"),
    ]
    
    for url, filename, ranking_type in url_map:
        print(f"正在处理: {filename}")
        parse_and_save_table(url, filename, ranking_type)
        time.sleep(1)  # 避免请求过快

if __name__ == "__main__":
    main() 
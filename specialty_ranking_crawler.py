#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专科声誉排行榜爬虫（包含获提名医院）
"""
import requests
import csv
import re
from bs4 import BeautifulSoup

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
    """清理文本，去除多余的空白字符"""
    return re.sub(r'[\r\n\t\xa0\u3000]+', ' ', text).strip()

def parse_specialty_ranking(html):
    """解析专科排行榜数据"""
    soup = BeautifulSoup(html, 'html.parser')
    
    # 查找所有表格
    tables = soup.find_all('table')
    data = []
    
    for table in tables:
        rows = table.find_all('tr')
        if len(rows) < 2:
            continue
            
        # 检查是否是专科排行榜表格
        header_text = ' '.join([cell.get_text(strip=True) for cell in rows[0].find_all(['td', 'th'])])
        
        if '医院名' in header_text and '平均声誉值' in header_text:
            # 找到科室名称
            dept_name = ""
            for i, row in enumerate(rows):
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    cell_text = clean_text(cells[0].get_text())
                    if cell_text and '医院名' not in cell_text and '排名' not in cell_text:
                        # 提取科室名称（去掉"医院名"等后缀）
                        dept_match = re.match(r'^(.+?)(?:医院名|排名|平均)', cell_text)
                        if dept_match:
                            dept_name = dept_match.group(1).strip()
                            break
            
            if not dept_name:
                continue
                
            # 解析数据行
            current_rank = ""
            for i, row in enumerate(rows[1:], 1):  # 跳过表头
                cells = row.find_all(['td', 'th'])
                if len(cells) < 2:
                    continue
                    
                cell_texts = [clean_text(cell.get_text()) for cell in cells]
                
                # 跳过空行或标题行
                if not any(cell_texts) or '医院名' in ' '.join(cell_texts):
                    continue
                
                # 处理排名医院（有具体排名和分数）
                if len(cell_texts) >= 3:
                    rank_text = cell_texts[0]
                    hospital_text = cell_texts[1] 
                    score_text = cell_texts[2] if len(cell_texts) > 2 else ""
                    
                    # 检查是否是数字排名
                    rank_match = re.match(r'^(\d+)$', rank_text)
                    score_match = re.match(r'^(\d+\.?\d*)$', score_text)
                    
                    if rank_match and score_match and hospital_text:
                        rank = rank_match.group(1)
                        score = score_match.group(1)
                        # 处理医院名称（可能包含多个医院，用顿号分隔）
                        hospitals = re.split(r'[、，,]', hospital_text)
                        for hospital in hospitals:
                            hospital = hospital.strip()
                            if hospital and len(hospital) > 2:
                                data.append([dept_name, rank, hospital, score])
                
                # 处理获提名医院
                for cell in cells:
                    cell_text = clean_text(cell.get_text())
                    if '获提名医院' in cell_text:
                        # 提取获提名医院列表
                        hospitals_text = re.sub(r'.*?获提名医院[：:]\s*', '', cell_text)
                        if hospitals_text:
                            # 分割医院名称
                            hospitals = re.split(r'[、，,]', hospitals_text)
                            for hospital in hospitals:
                                hospital = hospital.strip()
                                if hospital and len(hospital) > 2:
                                    data.append([dept_name, "获提名", hospital, ""])
    
    return data

def save_to_csv(data, filename):
    """保存数据到CSV文件"""
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['科室', '排名', '医院名称', '平均声誉值'])
        writer.writerows(data)
    print(f"已保存: {filename}，共{len(data)}条数据")

def main():
    url = "https://www.fdygs.com/news2023-1.aspx"
    filename = "2023年度中国医院专科声誉排行榜.csv"
    
    print(f"正在爬取: {url}")
    html = get_page_content(url)
    if not html:
        print("页面获取失败")
        return
    
    print("正在解析数据...")
    data = parse_specialty_ranking(html)
    if not data:
        print("未提取到有效数据")
        return
    
    save_to_csv(data, filename)
    
    # 显示部分数据预览
    print("\n数据预览（前10条）:")
    for i, row in enumerate(data[:10]):
        print(f"{i+1}: {row}")

if __name__ == "__main__":
    main() 
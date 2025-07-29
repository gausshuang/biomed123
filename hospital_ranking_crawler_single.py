#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专科声誉排行榜单页专用爬虫（修正版）
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
    return re.sub(r'[\r\n\t\xa0\u3000]+', '', text).strip()

def parse_specialty_ranking(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    # 科室分块
    dept_pattern = r'(\S+?)医院名.*?平均声誉值(.*?)(?=\S+?医院名|$)'
    dept_blocks = re.findall(dept_pattern, text, re.DOTALL)
    data = []
    for dept, block in dept_blocks:
        lines = block.split('\n')
        for line in lines:
            line = clean_text(line)
            if not line or '获提名' in line:
                break  # 跳过空行和遇到获提名医院即停止
            # 匹配“排名 医院名 分数”
            m = re.match(r'^(\d+)[、.\s]+([\u4e00-\u9fa5A-Za-z0-9（）\(\)\-·、\s]+?)[、.\s]+(\d+\.\d+)$', line)
            if m:
                rank, hospital, score = m.groups()
                hospital = clean_text(hospital)
                if hospital and len(hospital) > 2:
                    data.append([dept, rank, hospital, score])
    return data

def save_to_csv(data, filename):
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['科室', '排名', '医院名称', '平均声誉值'])
        writer.writerows(data)
    print(f"已保存: {filename}，共{len(data)}条数据")

def main():
    url = "https://www.fdygs.com/news2023-1.aspx"
    filename = "2023年度中国医院专科声誉排行榜.csv"
    html = get_page_content(url)
    if not html:
        print("页面获取失败")
        return
    data = parse_specialty_ranking(html)
    if not data:
        print("未提取到有效数据")
        return
    save_to_csv(data, filename)

if __name__ == "__main__":
    main() 
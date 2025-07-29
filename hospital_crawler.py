#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2023年度中国医院专科声誉排行榜爬虫
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

def crawl_hospital_ranking():
    """爬取医院排行榜数据"""
    
    url = "https://www.fdygs.com/news2023-1.aspx"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        print(f"正在访问: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            print("成功获取网页内容")
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找所有包含排行榜数据的表格或列表
            data = []
            
            # 尝试多种方式提取数据
            # 方法1: 查找表格
            tables = soup.find_all('table')
            print(f"找到 {len(tables)} 个表格")
            
            for i, table in enumerate(tables):
                print(f"处理表格 {i+1}")
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 3:  # 至少包含科室、排名、医院名称
                        row_data = [cell.get_text(strip=True) for cell in cells]
                        if any(row_data):  # 确保不是空行
                            data.append(row_data)
            
            # 方法2: 查找包含排行榜信息的div或其他元素
            if not data:
                print("表格中未找到数据，尝试其他方式...")
                content_divs = soup.find_all('div', class_=re.compile(r'content|ranking|list'))
                for div in content_divs:
                    text = div.get_text()
                    if '排名' in text or '医院' in text:
                        print(f"找到可能的内容区域: {text[:100]}...")
            
            # 方法3: 查找所有文本内容，用正则表达式提取
            if not data:
                print("尝试从全文提取数据...")
                full_text = soup.get_text()
                
                # 查找包含排名信息的行
                lines = full_text.split('\n')
                for line in lines:
                    line = line.strip()
                    if line and ('医院' in line or '排名' in line or '科室' in line):
                        # 尝试提取结构化数据
                        if re.search(r'\d+', line) and '医院' in line:
                            data.append([line])
            
            if data:
                print(f"提取到 {len(data)} 行数据")
                
                # 处理数据，确保格式正确
                processed_data = []
                for row in data:
                    if isinstance(row, list) and len(row) >= 3:
                        processed_data.append(row[:4])  # 只取前4列
                    elif isinstance(row, list) and len(row) == 1:
                        # 尝试分割单个字符串
                        text = row[0]
                        parts = re.split(r'[，,\s]+', text)
                        if len(parts) >= 3:
                            processed_data.append(parts[:4])
                
                return processed_data
            else:
                print("未找到排行榜数据")
                # 输出网页内容的前1000个字符用于调试
                print("网页内容预览:")
                print(soup.get_text()[:1000])
                return []
                
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"爬取过程中出现错误: {str(e)}")
        return []

def save_to_csv(data, filename="2023年度中国医院专科声誉排行榜.csv"):
    """保存数据到CSV文件"""
    
    if not data:
        print("没有数据可保存")
        return
    
    # 确定列名
    columns = ['科室', '排名', '医院名称', '平均声誉值']
    
    # 处理数据，确保每行都有4列
    processed_data = []
    for row in data:
        if len(row) < 4:
            row.extend([''] * (4 - len(row)))  # 补充空值
        elif len(row) > 4:
            row = row[:4]  # 截取前4列
        processed_data.append(row)
    
    # 创建DataFrame
    df = pd.DataFrame(processed_data, columns=columns)
    
    # 清理数据
    df = df.dropna(how='all')  # 删除全空行
    df = df[df['医院名称'].str.strip() != '']  # 删除医院名称为空的行
    
    # 保存到CSV
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"数据已保存到 {filename}")
    print(f"共保存 {len(df)} 条记录")
    
    # 显示前几行数据
    print("\n数据预览:")
    print(df.head(10))

if __name__ == "__main__":
    print("开始爬取2023年度中国医院专科声誉排行榜...")
    
    # 爬取数据
    ranking_data = crawl_hospital_ranking()
    
    if ranking_data:
        # 保存数据
        save_to_csv(ranking_data)
    else:
        print("爬取失败，未获取到数据") 
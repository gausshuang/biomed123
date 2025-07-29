#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2023年度中国医院专科声誉排行榜爬虫
爬取网站：https://www.fdygs.com/news2023-1.aspx
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
    }
    
    try:
        print(f"正在访问: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找包含排行榜数据的表格或内容
            data = []
            
            # 尝试多种方式查找数据
            # 方法1: 查找表格
            tables = soup.find_all('table')
            print(f"找到 {len(tables)} 个表格")
            
            if tables:
                for i, table in enumerate(tables):
                    print(f"处理第 {i+1} 个表格...")
                    rows = table.find_all('tr')
                    for row in rows:
                        cells = row.find_all(['td', 'th'])
                        if len(cells) >= 3:  # 至少要有3列数据
                            row_data = [cell.get_text(strip=True) for cell in cells]
                            if any(row_data):  # 确保不是空行
                                data.append(row_data)
            
            # 方法2: 查找包含排行榜信息的div或其他容器
            if not data:
                print("未在表格中找到数据，尝试其他方式...")
                # 查找可能包含排行榜的div
                content_divs = soup.find_all('div', class_=re.compile(r'content|article|main', re.I))
                for div in content_divs:
                    text = div.get_text()
                    if '排行榜' in text or '医院' in text:
                        print("找到可能包含排行榜的内容区域")
                        # 这里可以添加更具体的解析逻辑
                        break
            
            # 方法3: 直接从页面文本中提取
            if not data:
                print("尝试从页面文本中提取数据...")
                page_text = soup.get_text()
                
                # 查找包含医院名称和排名的行
                lines = page_text.split('\n')
                for line in lines:
                    line = line.strip()
                    if line and ('医院' in line or '排名' in line or '声誉' in line):
                        print(f"找到相关行: {line}")
            
            print(f"共提取到 {len(data)} 行数据")
            
            if data:
                # 创建DataFrame
                # 假设前几行可能是标题，尝试识别
                df_data = []
                headers = ['科室', '排名', '医院名称', '平均声誉值']
                
                for row in data:
                    if len(row) >= 3:
                        # 尝试解析每行数据
                        processed_row = process_row(row)
                        if processed_row:
                            df_data.append(processed_row)
                
                if df_data:
                    df = pd.DataFrame(df_data, columns=headers)
                    df.to_csv('2023年度中国医院专科声誉排行榜.csv', index=False, encoding='utf-8-sig')
                    print(f"数据已保存到 CSV 文件，共 {len(df)} 行数据")
                    print(df.head())
                else:
                    print("未能解析出有效数据")
                    # 保存原始HTML用于调试
                    with open('debug_page.html', 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    print("已保存原始HTML到 debug_page.html 用于调试")
            else:
                print("未找到任何数据")
                # 保存页面内容用于分析
                with open('page_content.txt', 'w', encoding='utf-8') as f:
                    f.write(soup.get_text())
                print("已保存页面文本到 page_content.txt")
        
        else:
            print(f"请求失败，状态码: {response.status_code}")
            
    except Exception as e:
        print(f"爬取过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

def process_row(row_data):
    """处理单行数据，尝试提取科室、排名、医院名称、声誉值"""
    if len(row_data) < 3:
        return None
    
    # 这里需要根据实际的数据格式来调整解析逻辑
    # 暂时返回原始数据，后续根据实际情况调整
    processed = []
    for i in range(4):  # 确保有4列
        if i < len(row_data):
            processed.append(row_data[i])
        else:
            processed.append('')
    
    return processed

if __name__ == "__main__":
    print("开始爬取2023年度中国医院专科声誉排行榜...")
    crawl_hospital_ranking()
    print("爬取完成！") 
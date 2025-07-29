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

def scrape_hospital_ranking():
    url = "https://www.fdygs.com/news2023-1.aspx"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        print("正在访问网页...")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        print("正在解析网页内容...")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找所有可能包含排行榜数据的表格
        tables = soup.find_all('table')
        print(f"找到 {len(tables)} 个表格")
        
        all_data = []
        
        # 遍历所有表格
        for i, table in enumerate(tables):
            print(f"处理第 {i+1} 个表格...")
            rows = table.find_all('tr')
            
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 3:  # 至少需要3列数据
                    row_text = [cell.get_text(strip=True) for cell in cells]
                    # 过滤掉空行和标题行
                    if row_text[0] and not any(keyword in row_text[0] for keyword in ['科室', '专科', '排名', '序号']):
                        all_data.append(row_text)
        
        # 如果表格数据不够，尝试从文本中提取
        if len(all_data) < 50:  # 预期应该有很多医院数据
            print("表格数据不足，尝试从文本中提取...")
            text_content = soup.get_text()
            
            # 查找包含医院排名信息的文本段落
            paragraphs = soup.find_all(['p', 'div', 'span'])
            for para in paragraphs:
                text = para.get_text(strip=True)
                if '医院' in text and ('排名' in text or '第' in text):
                    print("找到相关段落:", text[:100])
        
        # 处理数据并创建DataFrame
        processed_data = []
        current_specialty = ""
        
        for row in all_data:
            if len(row) >= 3:
                # 尝试识别科室名称（通常在第一列或作为标题）
                if '科' in row[0] or '专业' in row[0]:
                    current_specialty = row[0]
                    continue
                
                # 提取排名、医院名称等信息
                rank_match = re.search(r'(\d+|获提名)', str(row))
                if rank_match:
                    rank = rank_match.group(1)
                    hospital_name = ""
                    reputation_score = ""
                    
                    # 查找医院名称
                    for cell in row:
                        if '医院' in cell or '大学' in cell or '中心' in cell:
                            hospital_name = cell
                            break
                    
                    # 查找声誉值
                    for cell in row:
                        if re.search(r'\d+\.\d+', cell):
                            reputation_score = cell
                            break
                    
                    if hospital_name:
                        processed_data.append({
                            '科室': current_specialty,
                            '排名': rank,
                            '医院名称': hospital_name,
                            '平均声誉值': reputation_score
                        })
        
        print(f"提取到 {len(processed_data)} 条数据")
        
        if processed_data:
            # 创建DataFrame并保存为CSV
            df = pd.DataFrame(processed_data)
            df.to_csv('2023年度中国医院专科声誉排行榜.csv', index=False, encoding='utf-8-sig')
            print("数据已保存到 2023年度中国医院专科声誉排行榜.csv")
            print("\n前10条数据预览:")
            print(df.head(10))
        else:
            print("未能提取到有效数据，正在保存原始HTML用于调试...")
            with open('debug_page.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("原始HTML已保存到 debug_page.html")
            
            # 显示页面的主要内容结构
            print("\n页面主要内容结构:")
            for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'table']):
                print(f"{tag.name}: {tag.get_text(strip=True)[:100]}")
        
    except requests.RequestException as e:
        print(f"网络请求错误: {e}")
    except Exception as e:
        print(f"处理过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    scrape_hospital_ranking() 
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
    }
    
    try:
        print(f"正在访问: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容长度: {len(response.text)}")
        
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
                if len(cells) >= 3:  # 至少要有3列数据
                    cell_texts = [cell.get_text(strip=True) for cell in cells]
                    
                    # 检查是否包含医院排名信息
                    if any('医院' in text or '排名' in text or '声誉' in text for text in cell_texts):
                        print(f"找到相关行: {cell_texts}")
                        
                        # 尝试解析排名、医院名称等信息
                        for j, text in enumerate(cell_texts):
                            if '医院' in text and len(text) > 3:
                                # 可能是医院名称
                                ranking = ""
                                hospital_name = text
                                department = ""
                                reputation_score = ""
                                
                                # 查找排名信息
                                if j > 0:
                                    prev_text = cell_texts[j-1]
                                    if re.search(r'\d+', prev_text):
                                        ranking = prev_text
                                
                                # 查找科室信息
                                if j > 1:
                                    dept_text = cell_texts[j-2]
                                    if '科' in dept_text or '内科' in dept_text or '外科' in dept_text:
                                        department = dept_text
                                
                                # 查找声誉值
                                if j < len(cell_texts) - 1:
                                    next_text = cell_texts[j+1]
                                    if re.search(r'\d+\.?\d*', next_text):
                                        reputation_score = next_text
                                
                                if hospital_name and (ranking or department):
                                    all_data.append({
                                        '科室': department,
                                        '排名': ranking,
                                        '医院名称': hospital_name,
                                        '平均声誉值': reputation_score
                                    })
        
        # 如果没有找到表格数据，尝试查找其他格式的数据
        if not all_data:
            print("在表格中未找到数据，尝试查找其他格式...")
            
            # 查找所有包含"医院"的文本
            all_text = soup.get_text()
            lines = all_text.split('\n')
            
            current_department = ""
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                # 检查是否是科室标题
                if any(keyword in line for keyword in ['科室', '专科', '内科', '外科', '妇产科', '儿科', '眼科', '耳鼻喉科']):
                    if len(line) < 20:  # 科室名称通常较短
                        current_department = line
                        print(f"找到科室: {current_department}")
                        continue
                
                # 检查是否包含医院排名信息
                if '医院' in line and len(line) > 5:
                    # 尝试提取排名和医院名称
                    match = re.search(r'(\d+)[\s\.\、]*([^0-9]+医院[^0-9]*)', line)
                    if match:
                        ranking = match.group(1)
                        hospital_name = match.group(2).strip()
                        
                        # 尝试提取声誉值
                        reputation_match = re.search(r'(\d+\.?\d*)', line.replace(ranking, '').replace(hospital_name, ''))
                        reputation_score = reputation_match.group(1) if reputation_match else ""
                        
                        all_data.append({
                            '科室': current_department,
                            '排名': ranking,
                            '医院名称': hospital_name,
                            '平均声誉值': reputation_score
                        })
                        print(f"提取数据: {current_department} | {ranking} | {hospital_name} | {reputation_score}")
        
        print(f"总共提取到 {len(all_data)} 条数据")
        
        if all_data:
            # 创建DataFrame并保存为CSV
            df = pd.DataFrame(all_data)
            df.to_csv('2023年度中国医院专科声誉排行榜.csv', index=False, encoding='utf-8-sig')
            print("数据已保存到 2023年度中国医院专科声誉排行榜.csv")
            
            # 显示前几行数据
            print("\n前10行数据预览:")
            print(df.head(10).to_string(index=False))
        else:
            print("未能提取到有效数据")
            # 保存原始HTML用于调试
            with open('debug_page.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("原始页面已保存到 debug_page.html 用于调试")
        
        return all_data
        
    except requests.RequestException as e:
        print(f"网络请求错误: {e}")
        return []
    except Exception as e:
        print(f"处理错误: {e}")
        return []

if __name__ == "__main__":
    print("开始爬取2023年度中国医院专科声誉排行榜...")
    data = crawl_hospital_ranking()
    print("爬取完成！") 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2023年度中国医院专科声誉排行榜爬虫 - 最终版
爬取网站：https://www.fdygs.com/news2023-1.aspx
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def get_hospital_ranking():
    """爬取医院排行榜数据"""
    url = 'https://www.fdygs.com/news2023-1.aspx'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive'
    }
    
    try:
        print("正在访问网页...")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        print("正在解析页面内容...")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找包含排行榜数据的主表格
        data = []
        tables = soup.find_all('table')
        
        # 找到包含584行的主数据表格
        main_table = None
        for table in tables:
            rows = table.find_all('tr')
            if len(rows) > 500:  # 主表格有584行
                main_table = table
                print(f"找到主数据表格，共 {len(rows)} 行")
                break
        
        if main_table:
            rows = main_table.find_all('tr')
            current_specialty = ""
            
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 3:
                    cell_texts = [cell.get_text(strip=True) for cell in cells]
                    
                    # 检查是否是专科标题行
                    if len(cell_texts) == 3 and cell_texts[1] in ['医院名', '医院名称'] and cell_texts[2] == '平均声誉值':
                        current_specialty = cell_texts[0]
                        print(f"找到专科: {current_specialty}")
                        continue
                    
                    # 检查是否是数据行
                    if len(cell_texts) >= 3 and current_specialty:
                        rank = cell_texts[0].strip()
                        hospital = cell_texts[1].strip()
                        score = cell_texts[2].strip()
                        
                        # 跳过空行和标题行
                        if not rank or not hospital or not score:
                            continue
                        if rank in ['排名', '医院名', '医院名称'] or hospital in ['医院名', '医院名称']:
                            continue
                        
                        # 处理并列排名（如"并7"）
                        if rank.startswith('并'):
                            rank = rank[1:]
                        
                        # 验证排名是数字
                        try:
                            int(rank)
                        except ValueError:
                            continue
                        
                        # 验证分数是数字
                        try:
                            float(score)
                        except ValueError:
                            continue
                        
                        # 添加数据
                        data.append({
                            '科室': current_specialty,
                            '排名': rank,
                            '医院名称': hospital,
                            '平均声誉值': score
                        })
                        
                        print(f"{current_specialty} - 排名{rank}: {hospital} ({score})")
        
        print(f"总共提取到 {len(data)} 条记录")
        return data
        
    except Exception as e:
        print(f"爬取失败: {e}")
        return []

def add_nominated_hospitals():
    """添加获提名医院数据"""
    # 这里可以根据需要添加获提名医院的数据
    # 通常获提名医院没有具体分数，可以标记为"获提名"
    nominated_data = []
    
    # 示例：如果有获提名医院数据，可以在这里添加
    # nominated_data.append({
    #     '科室': '某科室',
    #     '排名': '获提名',
    #     '医院名称': '某医院',
    #     '平均声誉值': '获提名'
    # })
    
    return nominated_data

def main():
    print("开始爬取2023年度中国医院专科声誉排行榜...")
    
    # 获取排行榜数据
    ranking_data = get_hospital_ranking()
    
    # 获取提名医院数据
    nominated_data = add_nominated_hospitals()
    
    # 合并数据
    all_data = ranking_data + nominated_data
    
    if all_data:
        # 创建DataFrame
        df = pd.DataFrame(all_data)
        
        # 确保列的顺序
        df = df[['科室', '排名', '医院名称', '平均声誉值']]
        
        # 保存到CSV文件
        output_file = '2023年度中国医院专科声誉排行榜.csv'
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        print(f"\n成功保存 {len(all_data)} 条记录到 {output_file}")
        
        # 显示统计信息
        specialties = df['科室'].unique()
        print(f"包含 {len(specialties)} 个专科:")
        for specialty in specialties:
            count = len(df[df['科室'] == specialty])
            print(f"  {specialty}: {count} 家医院")
        
        # 显示前几条数据作为示例
        print(f"\n前10条数据预览:")
        print(df.head(10).to_string(index=False))
        
    else:
        print("未获取到数据，请检查网页结构")

if __name__ == "__main__":
    main() 
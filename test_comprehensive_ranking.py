#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专门测试中国医院综合排行榜页面
"""
import requests
from bs4 import BeautifulSoup

def analyze_comprehensive_ranking():
    """分析中国医院综合排行榜页面"""
    url = "https://www.fdygs.com/news2023-2.aspx"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        print(f"页面标题: {soup.title.string if soup.title else '无标题'}")
        print(f"页面长度: {len(response.text)} 字符")
        print(f"状态码: {response.status_code}")
        
        # 查找所有表格
        tables = soup.find_all('table')
        print(f"找到 {len(tables)} 个表格")
        
        for i, table in enumerate(tables):
            print(f"\n表格 {i+1}:")
            rows = table.find_all('tr')
            print(f"  行数: {len(rows)}")
            
            if rows:
                # 显示前几行的内容
                for j, row in enumerate(rows[:10]):
                    cells = row.find_all(['td', 'th'])
                    cell_texts = [cell.get_text(strip=True) for cell in cells]
                    print(f"  行 {j+1}: {cell_texts}")
        
        # 查找可能包含数据的div
        divs = soup.find_all('div')
        print(f"\n找到 {len(divs)} 个div")
        
        # 查找包含"医院"或"排名"的文本
        text_content = soup.get_text()
        lines = text_content.split('\n')
        hospital_lines = [line.strip() for line in lines if '医院' in line or '排名' in line or '综合' in line]
        
        print(f"\n包含'医院'或'排名'或'综合'的行数: {len(hospital_lines)}")
        for line in hospital_lines[:20]:
            print(f"  {line}")
            
    except Exception as e:
        print(f"分析失败: {e}")

if __name__ == "__main__":
    analyze_comprehensive_ranking() 
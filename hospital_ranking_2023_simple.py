#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2023年度中国医院专科声誉排行榜爬虫 - 简化版
爬取网站：https://www.fdygs.com/news2023-1.aspx
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

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
        
        # 查找包含排行榜数据的表格或div
        data = []
        
        # 先尝试查找表格
        tables = soup.find_all('table')
        print(f"找到 {len(tables)} 个表格")
        
        if tables:
            for table in tables:
                rows = table.find_all('tr')
                print(f"表格有 {len(rows)} 行")
                
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 3:  # 至少有科室、排名、医院名称
                        cell_texts = [cell.get_text(strip=True) for cell in cells]
                        print(f"行数据: {cell_texts}")
        
        # 如果没有表格，查找其他结构
        if not tables:
            print("没有找到表格，尝试查找其他结构...")
            
            # 查找所有包含排行榜信息的div或p标签
            content_divs = soup.find_all(['div', 'p'], text=re.compile(r'(排名|医院|科室|声誉)'))
            print(f"找到 {len(content_divs)} 个相关内容块")
            
            for div in content_divs[:10]:  # 只显示前10个
                print(f"内容: {div.get_text(strip=True)[:100]}")
        
        # 尝试查找特定的排行榜模式
        text_content = soup.get_text()
        
        # 查找包含医院名称的模式
        hospital_patterns = [
            r'(\d+)\s*[、.]\s*([^，\n]+医院[^，\n]*)\s*[，\s]*(\d+\.?\d*)',
            r'第(\d+)名[：:\s]*([^，\n]+医院[^，\n]*)',
            r'(\d+)\s*[、.]\s*([^，\n]+)\s*[：:\s]*(\d+\.?\d*)',
        ]
        
        for pattern in hospital_patterns:
            matches = re.findall(pattern, text_content)
            if matches:
                print(f"找到 {len(matches)} 个匹配项，模式: {pattern}")
                for match in matches[:5]:  # 显示前5个
                    print(f"匹配: {match}")
        
        # 保存原始HTML用于调试
        with open('debug_page.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("已保存原始HTML到 debug_page.html")
        
        return data
        
    except Exception as e:
        print(f"爬取失败: {e}")
        return []

def main():
    print("开始爬取2023年度中国医院专科声誉排行榜...")
    data = get_hospital_ranking()
    
    if data:
        # 创建DataFrame并保存
        df = pd.DataFrame(data, columns=['科室', '排名', '医院名称', '平均声誉值'])
        df.to_csv('2023年度中国医院专科声誉排行榜.csv', index=False, encoding='utf-8-sig')
        print(f"成功保存 {len(data)} 条记录到CSV文件")
    else:
        print("未获取到数据，请检查网页结构")

if __name__ == "__main__":
    main() 
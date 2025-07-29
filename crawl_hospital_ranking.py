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
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        print(f"正在访问: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        print(f"响应状态码: {response.status_code}")
        print(f"页面大小: {len(response.text)} 字符")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找所有可能包含排行榜数据的表格
        tables = soup.find_all('table')
        print(f"找到 {len(tables)} 个表格")
        
        all_data = []
        
        for i, table in enumerate(tables):
            print(f"\n处理第 {i+1} 个表格...")
            rows = table.find_all('tr')
            
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 3:  # 至少有3列数据
                    row_data = [cell.get_text(strip=True) for cell in cells]
                    if any(row_data):  # 确保不是空行
                        print(f"  行数据: {row_data}")
                        all_data.append(row_data)
        
        # 如果没有找到表格，尝试查找其他结构
        if not all_data:
            print("没有找到表格数据，尝试查找其他结构...")
            
            # 查找包含"排名"、"医院"等关键词的内容
            content_divs = soup.find_all(['div', 'p', 'span'], string=re.compile(r'(排名|医院|科室|声誉)', re.I))
            print(f"找到 {len(content_divs)} 个相关内容块")
            
            for div in content_divs[:10]:  # 只显示前10个
                print(f"内容: {div.get_text(strip=True)[:100]}...")
        
        # 保存原始HTML用于调试
        with open('debug_page.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("已保存原始页面到 debug_page.html")
        
        return all_data
        
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return []
    except Exception as e:
        print(f"解析错误: {e}")
        return []

def process_data(raw_data):
    """处理原始数据"""
    if not raw_data:
        print("没有数据可处理")
        return pd.DataFrame()
    
    # 创建DataFrame
    df = pd.DataFrame(raw_data)
    print(f"原始数据形状: {df.shape}")
    print("前几行数据:")
    print(df.head())
    
    return df

def main():
    """主函数"""
    print("开始爬取2023年度中国医院专科声誉排行榜...")
    
    # 爬取数据
    raw_data = crawl_hospital_ranking()
    
    if raw_data:
        # 处理数据
        df = process_data(raw_data)
        
        if not df.empty:
            # 保存为CSV
            output_file = "2023年度中国医院专科声誉排行榜.csv"
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"数据已保存到: {output_file}")
        else:
            print("没有有效数据可保存")
    else:
        print("爬取失败，没有获取到数据")

if __name__ == "__main__":
    main() 
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
    """爬取医院专科声誉排行榜数据"""
    
    url = "https://www.fdygs.com/news2023-1.aspx"
    
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
    }
    
    try:
        print(f"正在访问: {url}")
        
        # 发送请求
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容长度: {len(response.text)}")
        
        # 解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找所有可能包含排行榜数据的表格
        tables = soup.find_all('table')
        print(f"找到 {len(tables)} 个表格")
        
        all_data = []
        
        # 遍历所有表格
        for i, table in enumerate(tables):
            print(f"\n处理第 {i+1} 个表格...")
            
            # 查找表格行
            rows = table.find_all('tr')
            print(f"表格有 {len(rows)} 行")
            
            # 跳过表头，处理数据行
            for j, row in enumerate(rows[1:], 1):  # 跳过第一行（表头）
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 3:  # 至少需要3列数据
                    cell_texts = [cell.get_text().strip() for cell in cells]
                    print(f"第{j}行数据: {cell_texts}")
                    
                    # 尝试解析数据
                    if len(cell_texts) >= 3:
                        # 假设格式为：排名、医院名称、科室、声誉值等
                        # 需要根据实际网页结构调整
                        row_data = {
                            '原始数据': ' | '.join(cell_texts),
                            '列数': len(cell_texts)
                        }
                        all_data.append(row_data)
        
        # 如果没有找到表格，尝试查找其他结构
        if not tables:
            print("未找到表格，尝试查找其他结构...")
            
            # 查找包含排行榜信息的div或其他元素
            content_divs = soup.find_all('div', class_=re.compile(r'content|article|news'))
            print(f"找到 {len(content_divs)} 个内容区域")
            
            for div in content_divs:
                text = div.get_text()
                if '排行榜' in text or '医院' in text:
                    print(f"找到相关内容: {text[:200]}...")
        
        # 保存原始HTML用于调试
        with open('page_source.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("原始HTML已保存到 page_source.html")
        
        # 如果有数据，保存到CSV
        if all_data:
            df = pd.DataFrame(all_data)
            df.to_csv('raw_data.csv', index=False, encoding='utf-8-sig')
            print(f"原始数据已保存到 raw_data.csv，共 {len(all_data)} 条记录")
        else:
            print("未找到有效数据")
            
        return all_data
        
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return None
    except Exception as e:
        print(f"处理错误: {e}")
        return None

def parse_ranking_data(raw_data):
    """解析原始数据为标准格式"""
    
    parsed_data = []
    
    for item in raw_data:
        # 这里需要根据实际数据格式进行解析
        # 暂时保存原始数据
        parsed_data.append({
            '科室': '待解析',
            '排名': '待解析', 
            '医院名称': '待解析',
            '平均声誉值': '待解析',
            '原始数据': item.get('原始数据', '')
        })
    
    return parsed_data

def main():
    """主函数"""
    print("开始爬取2023年度中国医院专科声誉排行榜...")
    
    # 爬取数据
    raw_data = crawl_hospital_ranking()
    
    if raw_data:
        # 解析数据
        parsed_data = parse_ranking_data(raw_data)
        
        # 保存到CSV
        df = pd.DataFrame(parsed_data)
        df.to_csv('2023年度中国医院专科声誉排行榜.csv', index=False, encoding='utf-8-sig')
        
        print(f"数据已保存到 2023年度中国医院专科声誉排行榜.csv")
        print(f"共获取 {len(parsed_data)} 条记录")
    else:
        print("爬取失败")

if __name__ == "__main__":
    main() 
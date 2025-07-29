#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
医院排行榜爬虫脚本 v2
爬取复旦大学医院管理研究所发布的2023年度医院排行榜
"""
import requests
import csv
import os
import re
from bs4 import BeautifulSoup
import time

def get_page_content(url):
    """获取网页内容"""
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

def parse_hospital_ranking(html_content, ranking_type):
    """解析医院排行榜HTML内容"""
    if not html_content:
        return []
    
    soup = BeautifulSoup(html_content, 'html.parser')
    data = []
    
    # 查找表格内容
    tables = soup.find_all('table')
    
    for table in tables:
        rows = table.find_all('tr')
        current_dept = ""
        
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if not cells:
                continue
                
            # 检查是否是科室标题行
            cell_text = ' '.join([cell.get_text(strip=True) for cell in cells])
            if '医院名' in cell_text or '科室' in cell_text:
                # 提取科室名称
                for cell in cells:
                    text = cell.get_text(strip=True)
                    if text and '医院名' not in text and '科室' not in text:
                        current_dept = text
                        break
                continue
            
            # 处理排名数据
            if len(cells) >= 2:
                rank_cell = cells[0].get_text(strip=True)
                hospital_cell = cells[1].get_text(strip=True)
                
                if rank_cell.isdigit() and hospital_cell:
                    data.append([current_dept, rank_cell, hospital_cell])
                elif '获提名' in rank_cell and hospital_cell:
                    # 处理获提名医院
                    hospitals = hospital_cell.replace('、', ',').split(',')
                    for hospital in hospitals:
                        hospital = hospital.strip()
                        if hospital:
                            data.append([current_dept, '获提名医院', hospital])
    
    return data

def save_to_csv(data, filename):
    """保存数据到CSV文件"""
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['科室', '排名', '医院名'])
        writer.writerows(data)
    print(f"已保存 {len(data)} 条记录到 {filename}")

def main():
    """主函数"""
    urls = {
        '2023年度中国医院专科声誉排行榜': 'https://www.fdygs.com/news2023-1.aspx',
        '2023年度中国医院综合排行榜': 'https://www.fdygs.com/news2023-2.aspx',
        '2023年度东北区专科声誉排行榜': 'https://www.fdygs.com/news2023-1-11.aspx',
        '2023年度华北区专科声誉排行榜': 'https://www.fdygs.com/news2023-1-21.aspx',
        '2023年度华东区专科声誉排行榜': 'https://www.fdygs.com/news2023-1-31.aspx',
        '2023年度华南区专科声誉排行榜': 'https://www.fdygs.com/news2023-1-41.aspx',
        '2023年度华中区专科声誉排行榜': 'https://www.fdygs.com/news2023-1-51.aspx',
        '2023年度西北区专科声誉排行榜': 'https://www.fdygs.com/news2023-1-61.aspx',
        '2023年度西南区专科声誉排行榜': 'https://www.fdygs.com/news2023-1-71.aspx'
    }
    
    for name, url in urls.items():
        print(f"\n正在爬取: {name}")
        print(f"URL: {url}")
        
        html_content = get_page_content(url)
        if html_content:
            data = parse_hospital_ranking(html_content, name)
            if data:
                filename = f"{name}.csv"
                save_to_csv(data, filename)
            else:
                print(f"未找到数据: {name}")
        else:
            print(f"获取页面失败: {name}")
        
        # 添加延迟避免请求过快
        time.sleep(2)

if __name__ == "__main__":
    main() 
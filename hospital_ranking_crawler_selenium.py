#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
医院排行榜爬虫脚本 - Selenium版本
爬取复旦大学医院管理研究所发布的2023年度医院排行榜
"""
import csv
import os
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def setup_driver():
    """设置Chrome浏览器驱动"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"Chrome驱动初始化失败: {e}")
        print("请确保已安装Chrome浏览器和ChromeDriver")
        return None

def get_page_content_selenium(url, driver):
    """使用Selenium获取网页内容"""
    try:
        print(f"正在访问: {url}")
        driver.get(url)
        
        # 等待页面加载
        time.sleep(3)
        
        # 等待页面内容加载完成
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # 获取页面源码
        page_source = driver.page_source
        print(f"页面长度: {len(page_source)} 字符")
        
        return page_source
    except Exception as e:
        print(f"获取页面失败 {url}: {e}")
        return None

def parse_hospital_ranking(html_content, ranking_type):
    """解析医院排行榜HTML内容"""
    if not html_content:
        return []
    
    soup = BeautifulSoup(html_content, 'html.parser')
    data = []
    
    print(f"解析 {ranking_type} 数据...")
    
    # 查找所有可能的表格和内容区域
    tables = soup.find_all('table')
    divs = soup.find_all('div')
    
    print(f"找到 {len(tables)} 个表格，{len(divs)} 个div")
    
    # 尝试从表格中提取数据
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 2:
                row_data = [cell.get_text(strip=True) for cell in cells]
                if any('医院' in cell or '排名' in cell or '科室' in cell for cell in row_data):
                    print(f"表格行: {row_data}")
    
    # 尝试从div中提取数据
    for div in divs:
        text = div.get_text(strip=True)
        if len(text) > 50 and ('医院' in text or '排名' in text or '科室' in text):
            print(f"Div内容: {text[:200]}...")
    
    # 尝试提取所有文本内容
    all_text = soup.get_text()
    lines = all_text.split('\n')
    
    # 查找包含医院信息的行
    hospital_lines = []
    for line in lines:
        line = line.strip()
        if line and ('医院' in line or '排名' in line or '科室' in line):
            hospital_lines.append(line)
    
    print(f"找到 {len(hospital_lines)} 行可能包含医院信息的内容")
    for line in hospital_lines[:10]:  # 显示前10行
        print(f"  {line}")
    
    return data

def main():
    """主函数"""
    # 定义要爬取的URL和对应的文件名
    urls = [
        ("https://www.fdygs.com/news2023-1.aspx", "2023年度中国医院专科声誉排行榜.csv"),
        ("https://www.fdygs.com/news2023-2.aspx", "2023年度中国医院综合排行榜.csv"),
        ("https://www.fdygs.com/news2023-1-11.aspx", "2023年度东北区专科声誉排行榜.csv"),
        ("https://www.fdygs.com/news2023-1-21.aspx", "2023年度华北区专科声誉排行榜.csv"),
        ("https://www.fdygs.com/news2023-1-31.aspx", "2023年度中国医院专科声誉排行榜.csv"),
        ("https://www.fdygs.com/news2023-1-41.aspx", "2023年度华东区专科声誉排行榜.csv"),
        ("https://www.fdygs.com/news2023-1-51.aspx", "2023年度华南区专科声誉排行榜.csv"),
        ("https://www.fdygs.com/news2023-1-51.aspx", "2023年度华中区专科声誉排行榜.csv"),
        ("https://www.fdygs.com/news2023-1-61.aspx", "2023年度西北区专科声誉排行榜.csv"),
        ("https://www.fdygs.com/news2023-1-71.aspx", "2023年度西南区专科声誉排行榜.csv")
    ]
    
    driver = setup_driver()
    if not driver:
        print("无法初始化浏览器驱动，尝试使用requests方法...")
        return
    
    try:
        for url, filename in urls:
            print(f"\n{'='*50}")
            print(f"处理: {filename}")
            print(f"URL: {url}")
            
            # 获取页面内容
            html_content = get_page_content_selenium(url, driver)
            
            if html_content:
                # 解析数据
                data = parse_hospital_ranking(html_content, filename)
                
                # 保存到CSV文件
                if data:
                    with open(filename, 'w', encoding='utf-8', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(['科室', '排名', '医院名'])
                        writer.writerows(data)
                    print(f"成功保存 {len(data)} 条记录到 {filename}")
                else:
                    print(f"未找到有效数据，保存原始HTML内容")
                    with open(filename.replace('.csv', '_raw.html'), 'w', encoding='utf-8') as f:
                        f.write(html_content)
            
            time.sleep(2)  # 避免请求过于频繁
    
    finally:
        driver.quit()
        print("\n爬虫任务完成！")

if __name__ == "__main__":
    main() 
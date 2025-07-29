from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import os

def setup_driver():
    """
    设置Chrome浏览器驱动
    """
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
        print(f"设置Chrome驱动失败: {str(e)}")
        print("请确保已安装Chrome浏览器和ChromeDriver")
        return None

def scrape_hospital_rankings_selenium(url, region_name):
    """
    使用Selenium爬取医院专科声誉排行榜数据
    """
    driver = setup_driver()
    if not driver:
        return None
    
    try:
        print(f"正在访问: {url}")
        driver.get(url)
        
        # 等待页面加载
        time.sleep(5)
        
        # 等待页面内容加载完成
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except:
            print("页面加载超时")
        
        # 获取页面源码
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # 查找所有可能包含内容的区域
        content_selectors = [
            'div.content',
            'div.main',
            'div.article',
            'div.text',
            'div.body',
            'div#content',
            'div#main',
            'div#article',
            'div.container',
            'div.wrapper'
        ]
        
        content_div = None
        for selector in content_selectors:
            content_div = soup.select_one(selector)
            if content_div:
                print(f"找到内容区域: {selector}")
                break
        
        if not content_div:
            # 如果没有找到特定类名的div，尝试查找包含"科"字的div
            all_divs = soup.find_all('div')
            for div in all_divs:
                text = div.get_text()
                if '科' in text and len(text) > 500:
                    content_div = div
                    print("找到包含医疗信息的div")
                    break
        
        if not content_div:
            # 如果还是没找到，使用整个body
            content_div = soup.find('body')
            print("使用body作为内容区域")
        
        # 提取文本内容
        text_content = content_div.get_text() if content_div else ""
        
        print(f"提取的文本长度: {len(text_content)}")
        print(f"文本前500字符: {text_content[:500]}")
        
        # 解析科室和排名数据
        all_data = []
        lines = text_content.split('\n')
        
        current_department = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 检查是否是科室名称
            if '科' in line and re.search(r'\d+', line):
                current_department = line
                print(f"找到科室: {current_department}")
            elif current_department and line:
                # 检查是否是排名行
                if re.match(r'^\d+[、\.]', line):
                    # 正常排名
                    match = re.match(r'^(\d+)[、\.]\s*(.+)', line)
                    if match:
                        rank = match.group(1)
                        hospital_name = match.group(2).strip()
                        # 清理医院名称
                        hospital_name = re.sub(r'[（\(].*?[）\)]', '', hospital_name)
                        hospital_name = hospital_name.strip()
                        if hospital_name and len(hospital_name) > 2:
                            all_data.append({
                                '科室': current_department,
                                '排名': rank,
                                '医院名称': hospital_name
                            })
                elif '获提名' in line:
                    # 获提名医院
                    hospitals = re.findall(r'([^，,]+医院)', line)
                    for hospital in hospitals:
                        hospital = hospital.strip()
                        if hospital and len(hospital) > 2:
                            all_data.append({
                                '科室': current_department,
                                '排名': '获提名',
                                '医院名称': hospital
                            })
        
        # 创建DataFrame
        df = pd.DataFrame(all_data)
        
        if len(df) > 0:
            # 保存到CSV文件
            filename = f"2023年度{region_name}专科声誉排行榜.csv"
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"成功爬取 {region_name} 数据，共 {len(df)} 条记录")
            print(f"保存到: {filename}")
            return df
        else:
            print(f"未找到有效数据: {region_name}")
            return None
        
    except Exception as e:
        print(f"爬取 {region_name} 时出错: {str(e)}")
        return None
    finally:
        driver.quit()

def main():
    """
    主函数：爬取所有区域的数据
    """
    # 定义要爬取的URL和区域名称
    urls_and_regions = [
        ("https://www.fdygs.com/news2023-1-11.aspx", "东北区"),
        ("https://www.fdygs.com/news2023-1-21.aspx", "华北区"),
        ("https://www.fdygs.com/news2023-1-31.aspx", "华东区"),
        ("https://www.fdygs.com/news2023-1-41.aspx", "华南区"),
        ("https://www.fdygs.com/news2023-1-51.aspx", "华中区"),
        ("https://www.fdygs.com/news2023-1-61.aspx", "西北区"),
        ("https://www.fdygs.com/news2023-1-71.aspx", "西南区")
    ]
    
    print("开始使用Selenium爬取医院专科声誉排行榜数据...")
    
    for url, region in urls_and_regions:
        print(f"\n正在爬取 {region} 数据...")
        df = scrape_hospital_rankings_selenium(url, region)
        if df is not None:
            print(f"{region} 数据爬取完成")
        else:
            print(f"{region} 数据爬取失败")
        
        # 添加延时避免请求过于频繁
        time.sleep(3)
    
    print("\n所有数据爬取完成！")

if __name__ == "__main__":
    main() 
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

def parse_hospital_data(text_content, region_name):
    """
    解析医院排名数据
    """
    all_data = []
    lines = text_content.split('\n')
    
    # 定义科室列表
    departments = [
        '病理科', '传染科', '耳鼻喉科', '放射科', '呼吸科', '风湿科', '妇产科', 
        '骨科', '精神医学', '口腔科', '麻醉科', '泌尿外科', '内分泌科', '皮肤科', 
        '普通外科', '神经内科', '神经外科', '肾脏病', '消化病', '小儿内科', 
        '小儿外科', '心血管病', '心外科', '胸外科', '血液学', '眼科', '整形外科', 
        '肿瘤学', '老年医学', '康复医学', '检验医学', '烧伤科', '核医学', '超声医学'
    ]
    
    current_department = None
    current_hospitals = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 检查是否是科室名称
        is_department = False
        for dept in departments:
            if dept in line:
                # 保存之前的科室数据
                if current_department and current_hospitals:
                    # 处理当前科室的医院数据
                    for i, hospital in enumerate(current_hospitals):
                        if i < 10:  # 前10名有具体排名
                            all_data.append({
                                '科室': current_department,
                                '排名': str(i + 1),
                                '医院名称': hospital
                            })
                        else:  # 其他为获提名
                            all_data.append({
                                '科室': current_department,
                                '排名': '获提名',
                                '医院名称': hospital
                            })
                
                # 开始新的科室
                current_department = dept
                current_hospitals = []
                is_department = True
                print(f"找到科室: {current_department}")
                break
        
        if not is_department and current_department and line:
            # 提取医院名称
            # 使用正则表达式匹配医院名称
            hospitals = re.findall(r'([^，,、]+(?:医院|大学|医学院|附属|中心|总医院|人民医院|医科大学|军医大学|军区总医院|联勤保障部队|肿瘤医院|妇幼保健院|中医院|中西医结合医院|骨科医院|肿瘤医院|第一附属医院|第二附属医院|第三附属医院|第四附属医院|第五附属医院|第六附属医院|第七附属医院|第八附属医院|第九附属医院|第十附属医院))', line)
            
            for hospital in hospitals:
                hospital = hospital.strip()
                # 清理医院名称
                hospital = re.sub(r'[（\(].*?[）\)]', '', hospital)
                hospital = hospital.strip()
                if hospital and len(hospital) > 2 and hospital not in current_hospitals:
                    current_hospitals.append(hospital)
    
    # 处理最后一个科室
    if current_department and current_hospitals:
        for i, hospital in enumerate(current_hospitals):
            if i < 10:  # 前10名有具体排名
                all_data.append({
                    '科室': current_department,
                    '排名': str(i + 1),
                    '医院名称': hospital
                })
            else:  # 其他为获提名
                all_data.append({
                    '科室': current_department,
                    '排名': '获提名',
                    '医院名称': hospital
                })
    
    return all_data

def scrape_hospital_rankings_improved(url, region_name):
    """
    改进的医院专科声誉排行榜数据爬取
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
        
        # 提取文本内容
        text_content = soup.get_text()
        
        print(f"提取的文本长度: {len(text_content)}")
        
        # 解析医院数据
        all_data = parse_hospital_data(text_content, region_name)
        
        if all_data:
            # 创建DataFrame
            df = pd.DataFrame(all_data)
            
            # 保存到CSV文件
            filename = f"2023年度{region_name}专科声誉排行榜.csv"
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"成功爬取 {region_name} 数据，共 {len(df)} 条记录")
            print(f"保存到: {filename}")
            
            # 显示前几条数据作为示例
            print(f"\n{region_name} 数据示例:")
            print(df.head(10).to_string(index=False))
            
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
    
    print("开始使用改进的爬虫爬取医院专科声誉排行榜数据...")
    
    for url, region in urls_and_regions:
        print(f"\n正在爬取 {region} 数据...")
        df = scrape_hospital_rankings_improved(url, region)
        if df is not None:
            print(f"{region} 数据爬取完成")
        else:
            print(f"{region} 数据爬取失败")
        
        # 添加延时避免请求过于频繁
        time.sleep(3)
    
    print("\n所有数据爬取完成！")

if __name__ == "__main__":
    main() 
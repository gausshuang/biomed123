import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import os

def scrape_hospital_rankings(url, region_name):
    """
    爬取医院专科声誉排行榜数据
    """
    try:
        # 发送请求
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(f"请求失败: {url}, 状态码: {response.status_code}")
            return None
        
        # 解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找主要内容区域
        content_div = soup.find('div', class_='content')
        if not content_div:
            print(f"未找到内容区域: {url}")
            return None
        
        # 提取所有文本内容
        text_content = content_div.get_text()
        
        # 按科室分割内容
        departments = []
        current_department = None
        current_rankings = []
        
        lines = text_content.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 检查是否是科室名称（通常包含"科"字且后面跟着数字）
            if '科' in line and re.search(r'\d+', line):
                # 保存之前的科室数据
                if current_department and current_rankings:
                    departments.append({
                        'department': current_department,
                        'rankings': current_rankings
                    })
                
                # 开始新的科室
                current_department = line
                current_rankings = []
            elif current_department and line:
                # 检查是否是排名行
                if re.match(r'^\d+[、\.]', line) or '获提名' in line:
                    current_rankings.append(line)
        
        # 添加最后一个科室
        if current_department and current_rankings:
            departments.append({
                'department': current_department,
                'rankings': current_rankings
            })
        
        # 解析排名数据
        all_data = []
        for dept in departments:
            department_name = dept['department']
            for ranking_line in dept['rankings']:
                # 解析排名和医院名称
                if '获提名' in ranking_line:
                    # 处理获提名医院
                    hospitals = re.findall(r'([^，,]+医院)', ranking_line)
                    for hospital in hospitals:
                        all_data.append({
                            '科室': department_name,
                            '排名': '获提名',
                            '医院名称': hospital.strip()
                        })
                else:
                    # 处理正常排名
                    match = re.match(r'^(\d+)[、\.]\s*(.+)', ranking_line)
                    if match:
                        rank = match.group(1)
                        hospital_name = match.group(2).strip()
                        # 清理医院名称
                        hospital_name = re.sub(r'[（\(].*?[）\)]', '', hospital_name)
                        hospital_name = hospital_name.strip()
                        if hospital_name:
                            all_data.append({
                                '科室': department_name,
                                '排名': rank,
                                '医院名称': hospital_name
                            })
        
        # 创建DataFrame
        df = pd.DataFrame(all_data)
        
        # 保存到CSV文件
        filename = f"2023年度{region_name}专科声誉排行榜.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f"成功爬取 {region_name} 数据，共 {len(df)} 条记录")
        return df
        
    except Exception as e:
        print(f"爬取 {region_name} 时出错: {str(e)}")
        return None

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
    
    print("开始爬取医院专科声誉排行榜数据...")
    
    for url, region in urls_and_regions:
        print(f"\n正在爬取 {region} 数据...")
        df = scrape_hospital_rankings(url, region)
        if df is not None:
            print(f"{region} 数据爬取完成，保存到: 2023年度{region}专科声誉排行榜.csv")
        else:
            print(f"{region} 数据爬取失败")
        
        # 添加延时避免请求过于频繁
        time.sleep(2)
    
    print("\n所有数据爬取完成！")

if __name__ == "__main__":
    main() 
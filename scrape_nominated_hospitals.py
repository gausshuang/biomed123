import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def scrape_nominated_hospitals():
    """抓取获提名医院数据"""
    url = 'https://www.fdygs.com/news2023-1.aspx'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 查找所有表格
    tables = soup.find_all('table')
    nominated_data = []
    
    for table in tables:
        # 查找表格标题（科室名称）
        table_text = table.get_text()
        if '获提名' in table_text:
            # 提取科室名称
            department_match = re.search(r'([^获提名]+)获提名', table_text)
            if department_match:
                department = department_match.group(1).strip()
                
                # 查找获提名医院列表
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        # 提取医院名称
                        hospital_name = cells[1].get_text().strip()
                        if hospital_name and hospital_name != '医院名称' and '获提名' not in hospital_name:
                            nominated_data.append({
                                '科室': department,
                                '排名': '获提名',
                                '医院名称': hospital_name,
                                '平均声誉值': '0.000'  # 获提名医院通常没有具体声誉值
                            })
    
    return nominated_data

def update_csv_with_nominated():
    """更新CSV文件，添加获提名医院数据"""
    # 读取现有数据
    existing_df = pd.read_csv('2023年度中国医院专科声誉排行榜.csv')
    
    # 抓取获提名医院数据
    nominated_data = scrape_nominated_hospitals()
    
    if nominated_data:
        # 创建获提名医院DataFrame
        nominated_df = pd.DataFrame(nominated_data)
        
        # 合并数据
        updated_df = pd.concat([existing_df, nominated_df], ignore_index=True)
        
        # 保存更新后的数据
        updated_df.to_csv('2023年度中国医院专科声誉排行榜.csv', index=False, encoding='utf-8-sig')
        
        print(f"成功添加了 {len(nominated_data)} 条获提名医院数据")
        print("数据已更新到 2023年度中国医院专科声誉排行榜.csv")
        
        # 显示添加的数据预览
        print("\n添加的获提名医院数据预览:")
        print(nominated_df.head(10))
    else:
        print("未找到获提名医院数据")

if __name__ == "__main__":
    update_csv_with_nominated() 
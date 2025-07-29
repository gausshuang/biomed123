import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
import random
from urllib.parse import quote

def search_hospital_website_baidu(hospital_name):
    """使用百度搜索医院官网"""
    try:
        # 构建搜索关键词
        search_query = f"{hospital_name} 官网"
        encoded_query = quote(search_query)
        
        # 百度搜索URL
        search_url = f"https://www.baidu.com/s?wd={encoded_query}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找搜索结果中的链接
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link.get('href', '')
            text = link.get_text().strip()
            
            # 检查是否是医院官网链接
            if any(keyword in text.lower() for keyword in ['官网', '官方网站', '医院官网']):
                # 提取实际URL
                if href.startswith('/baidu.php?url='):
                    # 百度跳转链接
                    match = re.search(r'url=([^&]+)', href)
                    if match:
                        return match.group(1)
                elif href.startswith('http'):
                    return href
        
        # 如果没有找到明确的官网链接，尝试从搜索结果中提取
        for link in links:
            href = link.get('href', '')
            text = link.get_text().strip()
            
            # 检查链接是否包含医院名称
            if hospital_name in text and href.startswith('http'):
                # 检查是否是医院相关域名
                if any(domain in href for domain in ['hospital', 'med', 'health', 'gov.cn', 'edu.cn']):
                    return href
        
        return ''
        
    except Exception as e:
        print(f"搜索 {hospital_name} 官网时出错: {str(e)}")
        return ''

def guess_hospital_website(hospital_name):
    """根据医院名称猜测可能的官网域名"""
    try:
        # 提取医院名称的关键部分
        name_parts = hospital_name.replace('医院', '').replace('附属', '').replace('大学', '').replace('中国', '').replace('医科大学', '').replace('医学院', '').strip()
        
        # 常见的医院官网域名模式
        possible_domains = [
            f"www.{name_parts}.com",
            f"www.{name_parts}.cn",
            f"www.{name_parts}.org",
            f"{name_parts}.com",
            f"{name_parts}.cn",
            f"{name_parts}.org",
            f"www.{name_parts}hospital.com",
            f"www.{name_parts}hospital.cn",
            f"{name_parts}hospital.com",
            f"{name_parts}hospital.cn"
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        for domain in possible_domains:
            try:
                url = f"http://{domain}"
                response = requests.get(url, headers=headers, timeout=5)
                if response.status_code == 200:
                    # 检查页面内容是否包含医院相关信息
                    soup = BeautifulSoup(response.text, 'html.parser')
                    page_text = soup.get_text().lower()
                    if any(keyword in page_text for keyword in ['医院', 'hospital', '医疗', 'medical']):
                        return url
            except:
                continue
        
        return ''
        
    except Exception as e:
        print(f"猜测 {hospital_name} 官网时出错: {str(e)}")
        return ''

def get_hospital_website_url(hospital_name):
    """获取医院官网URL的综合方法"""
    # 首先尝试百度搜索
    url = search_hospital_website_baidu(hospital_name)
    if url:
        return url
    
    # 如果百度搜索失败，尝试域名猜测
    url = guess_hospital_website(hospital_name)
    if url:
        return url
    
    return ''

def supplement_website_urls_for_file(filename):
    """为单个CSV文件补充官网URL"""
    try:
        df = pd.read_csv(filename, encoding='utf-8-sig')
        
        # 确保官网URL列存在
        if '官网URL' not in df.columns:
            df['官网URL'] = ''
        
        # 处理NaN值
        df['官网URL'] = df['官网URL'].fillna('')
        
        print(f"处理文件: {filename}")
        print(f"总记录数: {len(df)}")
        
        # 统计缺失的URL数量
        missing_count = len(df[df['官网URL'] == ''])
        print(f"缺失官网URL的记录数: {missing_count}")
        
        if missing_count == 0:
            print("该文件没有缺失的官网URL")
            return 0
        
        updated_count = 0
        
        for index, row in df.iterrows():
            hospital_name = row['医院名称']
            current_url = row['官网URL']
            
            # 如果已经有URL，跳过
            if current_url and current_url.strip():
                continue
            
            print(f"正在搜索 {hospital_name} 的官网...")
            
            # 获取官网URL
            website_url = get_hospital_website_url(hospital_name)
            
            if website_url:
                df.at[index, '官网URL'] = website_url
                updated_count += 1
                print(f"  ✓ 找到官网: {website_url}")
            else:
                print(f"  ✗ 未找到官网")
            
            # 添加随机延迟避免被封
            time.sleep(random.uniform(1, 3))
        
        # 保存更新后的文件
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f"文件 {filename} 处理完成，新增 {updated_count} 个官网URL")
        return updated_count
        
    except Exception as e:
        print(f"处理文件 {filename} 时出错: {str(e)}")
        return 0

def main():
    """主函数"""
    csv_files = [
        "2023年度东北区专科声誉排行榜_with_info.csv",
        "2023年度华北区专科声誉排行榜_with_info.csv",
        "2023年度华东区专科声誉排行榜_with_info.csv",
        "2023年度华南区专科声誉排行榜_with_info.csv",
        "2023年度华中区专科声誉排行榜_with_info.csv",
        "2023年度西北区专科声誉排行榜_with_info.csv",
        "2023年度西南区专科声誉排行榜_with_info.csv"
    ]
    
    total_updated = 0
    
    for filename in csv_files:
        try:
            updated_count = supplement_website_urls_for_file(filename)
            total_updated += updated_count
            print("-" * 50)
        except Exception as e:
            print(f"处理文件 {filename} 时出错: {str(e)}")
            print("-" * 50)
    
    print(f"\n所有文件处理完成！总共新增了 {total_updated} 个官网URL")

if __name__ == "__main__":
    main() 
import pandas as pd
import requests
import json
from urllib.parse import urlparse

def quick_validate_url(url, timeout=5):
    """快速验证URL是否有效"""
    if not url or url.strip() == '':
        return False, "空URL"
        
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        parsed = urlparse(url)
        if not parsed.netloc:
            return False, "无效URL格式"
        
        response = requests.get(url, timeout=timeout, allow_redirects=True, 
                              headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        
        if response.status_code == 200:
            return True, f"有效 ({response.status_code})"
        else:
            return False, f"HTTP {response.status_code}"
            
    except Exception as e:
        return False, f"错误: {str(e)[:50]}"

def sample_validate_and_prepare_data():
    """快速验证并准备网站数据"""
    csv_files = [
        "2023年度东北区专科声誉排行榜_with_info.csv",
        "2023年度华北区专科声誉排行榜_with_info.csv", 
        "2023年度华东区专科声誉排行榜_with_info.csv",
        "2023年度华南区专科声誉排行榜_with_info.csv",
        "2023年度华中区专科声誉排行榜_with_info.csv",
        "2023年度西北区专科声誉排行榜_with_info.csv",
        "2023年度西南区专科声誉排行榜_with_info.csv"
    ]
    
    all_hospitals = []
    validation_results = []
    
    print("快速验证医院URL并准备网站数据...")
    print("=" * 60)
    
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file, encoding='utf-8-sig')
            df = df.fillna('')
            
            region = extract_region(csv_file)
            print(f"\n处理 {region} ({csv_file})")
            
            # 只验证前10个有URL的记录作为示例
            validated_count = 0
            for index, row in df.iterrows():
                if validated_count >= 10:  # 限制验证数量
                    break
                    
                hospital_name = row['医院名称']
                url = row['官网URL']
                department = row['科室']
                rank = row['排名']
                province = row.get('省份', '')
                city = row.get('城市', '')
                
                if url and url.strip():
                    is_valid, status = quick_validate_url(url)
                    print(f"  {hospital_name[:20]:<20} - {status}")
                    
                    validation_results.append({
                        'hospital': hospital_name,
                        'url': url,
                        'valid': is_valid,
                        'status': status,
                        'region': region
                    })
                    
                    validated_count += 1
                
                # 将所有医院数据添加到列表中（无论URL是否有效）
                all_hospitals.append({
                    'hospital_name': hospital_name,
                    'department': department,
                    'rank': rank,
                    'url': url if url and url.strip() else '',
                    'province': province,
                    'city': city,
                    'region': region
                })
            
        except FileNotFoundError:
            print(f"文件 {csv_file} 不存在")
        except Exception as e:
            print(f"处理 {csv_file} 时出错: {str(e)}")
    
    # 生成网站数据格式
    website_data = generate_website_data(all_hospitals)
    
    # 保存数据
    with open('hospitals_data.json', 'w', encoding='utf-8') as f:
        json.dump(website_data, f, ensure_ascii=False, indent=2)
    
    # 保存验证结果
    if validation_results:
        results_df = pd.DataFrame(validation_results)
        results_df.to_csv('url_validation_sample.csv', index=False, encoding='utf-8-sig')
    
    # 统计信息
    total_hospitals = len(all_hospitals)
    total_departments = len(website_data)
    valid_urls = sum(1 for r in validation_results if r['valid'])
    
    print(f"\n数据准备完成:")
    print(f"  总医院数量: {total_hospitals}")
    print(f"  总科室数量: {total_departments}")
    print(f"  验证的URL样本: {len(validation_results)}")
    print(f"  有效URL样本: {valid_urls}")
    print(f"\n生成文件:")
    print(f"  - hospitals_data.json (网站数据)")
    print(f"  - url_validation_sample.csv (验证样本)")
    
    return website_data

def extract_region(filename):
    """从文件名提取地区"""
    regions = ['东北区', '华北区', '华东区', '华南区', '华中区', '西北区', '西南区']
    for region in regions:
        if region in filename:
            return region
    return '未知区域'

def generate_website_data(hospitals):
    """生成网站需要的数据格式"""
    departments_data = {}
    
    for hospital in hospitals:
        department = hospital['department']
        if department not in departments_data:
            departments_data[department] = []
        
        departments_data[department].append({
            'rank': hospital['rank'],
            'hospital': hospital['hospital_name'],
            'url': hospital['url'],
            'province': hospital['province'],
            'city': hospital['city'],
            'region': hospital['region']
        })
    
    # 按排名排序
    for department in departments_data:
        departments_data[department].sort(key=lambda x: (
            0 if x['rank'].isdigit() else 1,
            int(x['rank']) if x['rank'].isdigit() else 999,
            x['rank']
        ))
    
    return departments_data

if __name__ == "__main__":
    sample_validate_and_prepare_data()
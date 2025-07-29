import pandas as pd
import json
import os

def prepare_complete_hospital_data():
    """准备完整的医院数据用于网站"""
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
    stats = {
        'total_hospitals': 0,
        'by_region': {},
        'by_department': {},
        'with_urls': 0,
        'with_province': 0,
        'with_city': 0
    }
    
    print("准备完整医院数据...")
    print("=" * 60)
    
    for csv_file in csv_files:
        if not os.path.exists(csv_file):
            print(f"文件 {csv_file} 不存在，跳过...")
            continue
            
        try:
            df = pd.read_csv(csv_file, encoding='utf-8-sig')
            df = df.fillna('')  # 处理NaN值
            
            region = extract_region(csv_file)
            print(f"处理 {region} - {len(df)} 条记录")
            
            stats['by_region'][region] = len(df)
            
            for index, row in df.iterrows():
                hospital_name = str(row['医院名称']).strip()
                department = str(row['科室']).strip()
                rank = str(row['排名']).strip()
                url = str(row['官网URL']).strip()
                province = str(row.get('省份', '')).strip()
                city = str(row.get('城市', '')).strip()
                
                # 跳过空记录
                if not hospital_name or hospital_name == 'nan':
                    continue
                
                # 统计
                stats['total_hospitals'] += 1
                if url and url != 'nan':
                    stats['with_urls'] += 1
                if province and province != 'nan':
                    stats['with_province'] += 1
                if city and city != 'nan':
                    stats['with_city'] += 1
                
                if department not in stats['by_department']:
                    stats['by_department'][department] = 0
                stats['by_department'][department] += 1
                
                all_hospitals.append({
                    'hospital_name': hospital_name,
                    'department': department,
                    'rank': rank,
                    'url': url if url != 'nan' else '',
                    'province': province if province != 'nan' else '',
                    'city': city if city != 'nan' else '',
                    'region': region
                })
                
        except Exception as e:
            print(f"处理文件 {csv_file} 时出错: {str(e)}")
    
    # 生成网站数据格式
    website_data = generate_website_data(all_hospitals)
    
    # 保存完整数据
    with open('complete_hospitals_data.json', 'w', encoding='utf-8') as f:
        json.dump(website_data, f, ensure_ascii=False, indent=2)
    
    # 保存统计信息
    with open('hospital_stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    # 生成CSV格式的完整数据
    if all_hospitals:
        complete_df = pd.DataFrame(all_hospitals)
        complete_df.to_csv('complete_hospitals.csv', index=False, encoding='utf-8-sig')
    
    # 打印统计信息
    print_statistics(stats, website_data)
    
    return website_data, stats

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
        if not department:
            continue
            
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
            0 if x['rank'].isdigit() else 1,  # 数字排名优先
            int(x['rank']) if x['rank'].isdigit() else 999,  # 按数字大小排序
            x['rank']  # 获提名等非数字排名按字母排序
        ))
    
    return departments_data

def print_statistics(stats, website_data):
    """打印统计信息"""
    print(f"\n数据统计:")
    print(f"  总医院数量: {stats['total_hospitals']}")
    print(f"  总科室数量: {len(website_data)}")
    print(f"  有官网URL: {stats['with_urls']} ({stats['with_urls']/stats['total_hospitals']*100:.1f}%)")
    print(f"  有省份信息: {stats['with_province']} ({stats['with_province']/stats['total_hospitals']*100:.1f}%)")
    print(f"  有城市信息: {stats['with_city']} ({stats['with_city']/stats['total_hospitals']*100:.1f}%)")
    
    print(f"\n按地区统计:")
    for region, count in sorted(stats['by_region'].items()):
        print(f"  {region}: {count}个医院")
    
    print(f"\n主要科室 (前15个):")
    sorted_depts = sorted(stats['by_department'].items(), key=lambda x: x[1], reverse=True)
    for dept, count in sorted_depts[:15]:
        print(f"  {dept}: {count}个医院")
    
    print(f"\n生成文件:")
    print(f"  - complete_hospitals_data.json (网站使用)")
    print(f"  - complete_hospitals.csv (完整数据)")
    print(f"  - hospital_stats.json (统计信息)")

def create_sample_valid_urls():
    """创建一个包含已知有效URL的示例文件"""
    sample_valid_urls = {
        "北京协和医院": "https://www.pumch.cn/",
        "北京大学第三医院": "https://www.puh3.net.cn/",
        "中山大学附属第一医院": "https://www.gzsums.net/",
        "复旦大学附属华山医院": "https://www.huashan.org.cn/",
        "上海交通大学医学院附属瑞金医院": "https://www.rjh.com.cn/",
        "四川大学华西医院": "https://www.wchscu.cn/",
        "中南大学湘雅医院": "https://www.xiangya.com.cn/",
        "华中科技大学同济医学院附属同济医院": "https://www.tjh.com.cn/",
        "西安交通大学第一附属医院": "https://www.dyyy.xjtu.edu.cn/",
        "山东大学齐鲁医院": "https://www.qiluhospital.com/"
    }
    
    with open('sample_valid_urls.json', 'w', encoding='utf-8') as f:
        json.dump(sample_valid_urls, f, ensure_ascii=False, indent=2)
    
    print(f"创建了示例有效URL文件: sample_valid_urls.json")

if __name__ == "__main__":
    website_data, stats = prepare_complete_hospital_data()
    create_sample_valid_urls()
    print("\n" + "=" * 60)
    print("医院数据准备完成！")
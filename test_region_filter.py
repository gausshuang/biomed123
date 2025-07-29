import json

def test_region_filtering():
    """测试地区筛选功能"""
    print("🧪 测试地区筛选功能")
    print("=" * 50)
    
    # 加载医院数据
    try:
        with open('complete_hospitals_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("✅ 医院数据加载成功")
    except Exception as e:
        print(f"❌ 数据加载失败: {e}")
        return
    
    # 统计每个地区的医院数量
    region_stats = {}
    total_hospitals = 0
    
    for dept, hospitals in data.items():
        for hospital in hospitals:
            region = hospital.get('region', '未知地区')
            if region not in region_stats:
                region_stats[region] = 0
            region_stats[region] += 1
            total_hospitals += 1
    
    print(f"\n📊 地区分布统计:")
    print(f"总医院数量: {total_hospitals}")
    
    for region, count in sorted(region_stats.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_hospitals) * 100
        print(f"  {region}: {count} 个医院 ({percentage:.1f}%)")
    
    # 测试按地区筛选
    print(f"\n🔍 测试地区筛选功能:")
    
    regions_to_test = ['华东区', '华北区', '华南区', '西南区']
    
    for test_region in regions_to_test:
        filtered_hospitals = []
        for dept, hospitals in data.items():
            for hospital in hospitals:
                if hospital.get('region') == test_region:
                    filtered_hospitals.append(hospital)
        
        print(f"  {test_region}: {len(filtered_hospitals)} 个医院")
        
        # 显示该地区的前3个医院作为示例
        if filtered_hospitals:
            print(f"    示例医院:")
            for i, hospital in enumerate(filtered_hospitals[:3]):
                print(f"      {i+1}. {hospital.get('hospital', '未知医院')} - {hospital.get('province', '未知省份')}")
    
    # 测试科室和地区组合筛选
    print(f"\n🔍 测试组合筛选 (华东区 + 病理科):")
    
    combined_results = []
    for dept, hospitals in data.items():
        if '病理科' in dept:
            for hospital in hospitals:
                if hospital.get('region') == '华东区':
                    combined_results.append({
                        'hospital': hospital.get('hospital'),
                        'dept': dept,
                        'rank': hospital.get('rank'),
                        'province': hospital.get('province'),
                        'city': hospital.get('city')
                    })
    
    print(f"找到 {len(combined_results)} 个结果:")
    for result in combined_results[:5]:  # 显示前5个
        print(f"  - {result['hospital']} (排名: {result['rank']}) - {result['province']} {result['city']}")
    
    print(f"\n✅ 地区筛选功能测试完成！")

def generate_region_summary():
    """生成地区汇总信息"""
    print(f"\n📋 生成地区汇总信息...")
    
    try:
        with open('complete_hospitals_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ 数据加载失败: {e}")
        return
    
    region_summary = {}
    
    for dept, hospitals in data.items():
        for hospital in hospitals:
            region = hospital.get('region', '未知地区')
            if region not in region_summary:
                region_summary[region] = {
                    'total_hospitals': 0,
                    'departments': set(),
                    'provinces': set(),
                    'with_url': 0,
                    'sample_hospitals': []
                }
            
            region_summary[region]['total_hospitals'] += 1
            region_summary[region]['departments'].add(dept)
            if hospital.get('province'):
                region_summary[region]['provinces'].add(hospital.get('province'))
            if hospital.get('url') and hospital.get('url').strip():
                region_summary[region]['with_url'] += 1
            
            # 收集示例医院
            if len(region_summary[region]['sample_hospitals']) < 3:
                region_summary[region]['sample_hospitals'].append(hospital.get('hospital'))
    
    # 保存汇总信息
    summary_for_save = {}
    for region, info in region_summary.items():
        summary_for_save[region] = {
            'total_hospitals': info['total_hospitals'],
            'departments': list(info['departments']),
            'provinces': list(info['provinces']),
            'with_url': info['with_url'],
            'url_percentage': round((info['with_url'] / info['total_hospitals']) * 100, 1),
            'sample_hospitals': info['sample_hospitals']
        }
    
    with open('region_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary_for_save, f, ensure_ascii=False, indent=2)
    
    print("✅ 地区汇总信息已保存到 region_summary.json")
    
    # 打印汇总
    print(f"\n📊 各地区详细信息:")
    for region in ['华东区', '华北区', '华南区', '西南区', '华中区', '西北区', '东北区']:
        if region in summary_for_save:
            info = summary_for_save[region]
            print(f"\n{region}:")
            print(f"  医院数量: {info['total_hospitals']}")
            print(f"  科室数量: {len(info['departments'])}")
            print(f"  省份数量: {len(info['provinces'])}")
            print(f"  有官网URL: {info['with_url']} ({info['url_percentage']}%)")
            print(f"  主要省份: {', '.join(info['provinces'][:3])}")

if __name__ == "__main__":
    test_region_filtering()
    generate_region_summary()
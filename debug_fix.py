import pandas as pd

def test_hospital_matching():
    """测试医院名称匹配逻辑"""
    
    # 军队医院和特殊医院映射
    military_hospitals = {
        '陆军军医大学第一附属医院': ('重庆', '重庆'),
        '陆军军医大学第二附属医院': ('重庆', '重庆'),
        '中国人民解放军陆军特色医学中心': ('重庆', '重庆'),
        '中国人民解放军联勤保障部队第920医院': ('云南', '昆明'),
        '中国人民解放军西部战区总医院': ('四川', '成都'),
    }
    
    # 医学院附属医院映射
    medical_school_hospitals = {
        '西南医科大学附属医院': ('四川', '泸州'),
        '西南医科大学口腔医学院·附属口腔医院': ('四川', '泸州'),
        '西南医科大学中西医结合学院·附属中医医院': ('四川', '泸州'),
        '川北医学院附属医院': ('四川', '南充'),
    }
    
    # 特殊医院映射
    special_hospitals = {
        '贵黔国际总医院': ('贵州', '贵阳'),
    }
    
    # 测试医院名称
    test_hospitals = [
        '陆军军医大学第一附属医院',
        '陆军军医大学第二附属医院',
        '中国人民解放军陆军特色医学中心',
        '中国人民解放军联勤保障部队第920医院',
        '中国人民解放军西部战区总医院',
        '西南医科大学附属医院',
        '西南医科大学口腔医学院·附属口腔医院',
        '西南医科大学中西医结合学院·附属中医医院',
        '川北医学院附属医院',
        '贵黔国际总医院',
    ]
    
    print("测试医院名称匹配逻辑:")
    print("=" * 50)
    
    for hospital_name in test_hospitals:
        print(f"\n测试医院: {hospital_name}")
        
        # 测试军队医院匹配
        for key, (province, city) in military_hospitals.items():
            if key in hospital_name:
                print(f"  军队医院匹配: {key} -> {province}, {city}")
                break
        else:
            print("  军队医院匹配: 未找到")
        
        # 测试医学院附属医院匹配
        for key, (province, city) in medical_school_hospitals.items():
            if key in hospital_name:
                print(f"  医学院附属医院匹配: {key} -> {province}, {city}")
                break
        else:
            print("  医学院附属医院匹配: 未找到")
        
        # 测试特殊医院匹配
        for key, (province, city) in special_hospitals.items():
            if key in hospital_name:
                print(f"  特殊医院匹配: {key} -> {province}, {city}")
                break
        else:
            print("  特殊医院匹配: 未找到")

def check_csv_missing_data():
    """检查CSV文件中的缺失数据"""
    filename = "2023年度西南区专科声誉排行榜_with_info.csv"
    df = pd.read_csv(filename, encoding='utf-8-sig')
    
    print(f"\n检查文件: {filename}")
    print("=" * 50)
    
    missing_province = df[df['省份'] == '']
    missing_city = df[df['城市'] == '']
    
    print(f"缺失省份信息的记录数: {len(missing_province)}")
    print(f"缺失城市信息的记录数: {len(missing_city)}")
    
    print("\n缺失省份信息的医院:")
    for _, row in missing_province.iterrows():
        print(f"  {row['医院名称']}")
    
    print("\n缺失城市信息的医院:")
    for _, row in missing_city.iterrows():
        print(f"  {row['医院名称']}")

if __name__ == "__main__":
    test_hospital_matching()
    check_csv_missing_data() 
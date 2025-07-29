import pandas as pd

def simple_fix_hospital_info():
    """简单修复医院地理位置信息"""
    filename = "2023年度西南区专科声誉排行榜_with_info.csv"
    df = pd.read_csv(filename, encoding='utf-8-sig')
    
    print(f"正在修复文件: {filename}")
    print(f"总记录数: {len(df)}")
    
    # 统计修复前的信息
    before_province_count = len(df[df['省份'] != ''])
    before_city_count = len(df[df['城市'] != ''])
    print(f"修复前 - 有省份信息的记录数: {before_province_count}")
    print(f"修复前 - 有城市信息的记录数: {before_city_count}")
    
    updated_count = 0
    
    # 直接修复缺失的信息
    for index, row in df.iterrows():
        hospital_name = row['医院名称']
        province = row['省份']
        city = row['城市']
        
        # 如果省份或城市为空，尝试获取信息
        if province == '' or city == '':
            new_province = ''
            new_city = ''
            
            # 军队医院
            if '陆军军医大学第一附属医院' in hospital_name:
                new_province, new_city = '重庆', '重庆'
            elif '陆军军医大学第二附属医院' in hospital_name:
                new_province, new_city = '重庆', '重庆'
            elif '中国人民解放军陆军特色医学中心' in hospital_name:
                new_province, new_city = '重庆', '重庆'
            elif '中国人民解放军联勤保障部队第920医院' in hospital_name:
                new_province, new_city = '云南', '昆明'
            elif '中国人民解放军西部战区总医院' in hospital_name:
                new_province, new_city = '四川', '成都'
            # 医学院附属医院
            elif '西南医科大学附属医院' in hospital_name:
                new_province, new_city = '四川', '泸州'
            elif '西南医科大学口腔医学院·附属口腔医院' in hospital_name:
                new_province, new_city = '四川', '泸州'
            elif '西南医科大学中西医结合学院·附属中医医院' in hospital_name:
                new_province, new_city = '四川', '泸州'
            elif '川北医学院附属医院' in hospital_name:
                new_province, new_city = '四川', '南充'
            # 特殊医院
            elif '贵黔国际总医院' in hospital_name:
                new_province, new_city = '贵州', '贵阳'
            
            # 更新信息
            if new_province != '' and province == '':
                df.at[index, '省份'] = new_province
                updated_count += 1
                print(f"  添加省份信息: {hospital_name} -> {new_province}")
            
            if new_city != '' and city == '':
                df.at[index, '城市'] = new_city
                updated_count += 1
                print(f"  添加城市信息: {hospital_name} -> {new_city}")
    
    # 统计修复后的信息
    after_province_count = len(df[df['省份'] != ''])
    after_city_count = len(df[df['城市'] != ''])
    
    print(f"修复后 - 有省份信息的记录数: {after_province_count}")
    print(f"修复后 - 有城市信息的记录数: {after_city_count}")
    print(f"新增省份信息: {after_province_count - before_province_count}")
    print(f"新增城市信息: {after_city_count - before_city_count}")
    print(f"总更新次数: {updated_count}")
    
    # 保存文件
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"文件已更新: {filename}")
    
    return df

if __name__ == "__main__":
    simple_fix_hospital_info() 
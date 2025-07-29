import pandas as pd
import os

def manual_fix_missing_info():
    """
    手动修复缺失的医院地理位置信息
    """
    # 读取西南区文件
    filename = "2023年度西南区专科声誉排行榜_with_info.csv"
    df = pd.read_csv(filename, encoding='utf-8-sig')
    
    print(f"正在手动修复文件: {filename}")
    
    # 统计修复前的信息
    before_province_count = len(df[df['省份'] != ''])
    before_city_count = len(df[df['城市'] != ''])
    
    print(f"修复前 - 有省份信息的记录数: {before_province_count}")
    print(f"修复前 - 有城市信息的记录数: {before_city_count}")
    
    # 手动修复缺失的信息
    updated_count = 0
    
    # 遍历所有行，手动修复缺失的省份和城市信息
    for index, row in df.iterrows():
        hospital_name = row['医院名称']
        province = row['省份']
        city = row['城市']
        
        # 修复缺失的省份信息
        if province == '':
            if '四川大学华西' in hospital_name:
                df.at[index, '省份'] = '四川'
                updated_count += 1
            elif '陆军军医大学' in hospital_name:
                df.at[index, '省份'] = '重庆'
                updated_count += 1
            elif '中国人民解放军陆军特色医学中心' in hospital_name:
                df.at[index, '省份'] = '重庆'
                updated_count += 1
            elif '中国人民解放军联勤保障部队第920医院' in hospital_name:
                df.at[index, '省份'] = '云南'
                updated_count += 1
            elif '中国人民解放军西部战区总医院' in hospital_name:
                df.at[index, '省份'] = '四川'
                updated_count += 1
            elif '西南医科大学' in hospital_name:
                df.at[index, '省份'] = '四川'
                updated_count += 1
            elif '川北医学院' in hospital_name:
                df.at[index, '省份'] = '四川'
                updated_count += 1
            elif '四川省' in hospital_name:
                df.at[index, '省份'] = '四川'
                updated_count += 1
            elif '贵州省' in hospital_name:
                df.at[index, '省份'] = '贵州'
                updated_count += 1
            elif '云南省' in hospital_name:
                df.at[index, '省份'] = '云南'
                updated_count += 1
            elif '西藏自治区' in hospital_name:
                df.at[index, '省份'] = '西藏'
                updated_count += 1
            elif '重庆市' in hospital_name:
                df.at[index, '省份'] = '重庆'
                updated_count += 1
        
        # 修复缺失的城市信息
        if city == '':
            if '四川大学华西' in hospital_name:
                df.at[index, '城市'] = '成都'
                updated_count += 1
            elif '陆军军医大学' in hospital_name:
                df.at[index, '城市'] = '重庆'
                updated_count += 1
            elif '中国人民解放军陆军特色医学中心' in hospital_name:
                df.at[index, '城市'] = '重庆'
                updated_count += 1
            elif '中国人民解放军联勤保障部队第920医院' in hospital_name:
                df.at[index, '城市'] = '昆明'
                updated_count += 1
            elif '中国人民解放军西部战区总医院' in hospital_name:
                df.at[index, '城市'] = '成都'
                updated_count += 1
            elif '西南医科大学' in hospital_name:
                df.at[index, '城市'] = '泸州'
                updated_count += 1
            elif '川北医学院' in hospital_name:
                df.at[index, '城市'] = '南充'
                updated_count += 1
            elif '四川省人民医院' in hospital_name:
                df.at[index, '城市'] = '成都'
                updated_count += 1
            elif '四川省肿瘤医院' in hospital_name:
                df.at[index, '城市'] = '成都'
                updated_count += 1
            elif '四川省妇幼保健院' in hospital_name:
                df.at[index, '城市'] = '成都'
                updated_count += 1
            elif '贵州省人民医院' in hospital_name:
                df.at[index, '城市'] = '贵阳'
                updated_count += 1
            elif '贵州医科大学附属医院' in hospital_name:
                df.at[index, '城市'] = '贵阳'
                updated_count += 1
            elif '贵州医科大学附属口腔医院' in hospital_name:
                df.at[index, '城市'] = '贵阳'
                updated_count += 1
            elif '云南省第一人民医院' in hospital_name:
                df.at[index, '城市'] = '昆明'
                updated_count += 1
            elif '云南省传染病医院' in hospital_name:
                df.at[index, '城市'] = '昆明'
                updated_count += 1
            elif '云南省精神病医院' in hospital_name:
                df.at[index, '城市'] = '昆明'
                updated_count += 1
            elif '西藏自治区人民医院' in hospital_name:
                df.at[index, '城市'] = '拉萨'
                updated_count += 1
    
    # 统计修复后的信息
    after_province_count = len(df[df['省份'] != ''])
    after_city_count = len(df[df['城市'] != ''])
    
    print(f"修复后 - 有省份信息的记录数: {after_province_count}")
    print(f"修复后 - 有城市信息的记录数: {after_city_count}")
    print(f"新增省份信息: {after_province_count - before_province_count}")
    print(f"新增城市信息: {after_city_count - before_city_count}")
    print(f"总更新次数: {updated_count}")
    
    # 保存更新后的文件
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"文件已更新: {filename}\n")
    
    return df

def main():
    """
    主函数
    """
    print("开始手动修复缺失的医院地理位置信息...")
    
    try:
        df = manual_fix_missing_info()
        print("手动修复完成！")
    except Exception as e:
        print(f"修复过程中出错: {str(e)}")

if __name__ == "__main__":
    main() 
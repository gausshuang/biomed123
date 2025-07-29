import pandas as pd
import os

def fix_specific_missing_info():
    """
    修复特定的缺失医院地理位置信息
    """
    # 读取西南区文件
    filename = "2023年度西南区专科声誉排行榜_with_info.csv"
    df = pd.read_csv(filename, encoding='utf-8-sig')
    
    print(f"正在修复文件: {filename}")
    
    # 特定的医院地理位置映射
    specific_fixes = {
        '陆军军医大学第一附属医院': ('重庆', '重庆'),
        '陆军军医大学第二附属医院': ('重庆', '重庆'),
        '中国人民解放军陆军特色医学中心': ('重庆', '重庆'),
        '中国人民解放军联勤保障部队第920医院': ('云南', '昆明'),
        '中国人民解放军西部战区总医院': ('四川', '成都'),
        '西南医科大学附属医院': ('四川', '泸州'),
        '西南医科大学口腔医学院·附属口腔医院': ('四川', '泸州'),
        '川北医学院附属医院': ('四川', '南充'),
        '四川大学华西医院': ('四川', '成都'),
        '四川大学华西第二医院': ('四川', '成都'),
        '四川大学华西口腔医院': ('四川', '成都'),
        '四川省人民医院': ('四川', '成都'),
        '四川省肿瘤医院': ('四川', '成都'),
        '四川省妇幼保健院': ('四川', '成都'),
        '贵州省人民医院': ('贵州', '贵阳'),
        '贵州医科大学附属医院': ('贵州', '贵阳'),
        '贵州医科大学附属口腔医院': ('贵州', '贵阳'),
        '云南省第一人民医院（昆华医院': ('云南', '昆明'),
        '云南省传染病医院/省艾滋病关爱中心/省心理卫生中心': ('云南', '昆明'),
        '云南省精神病医院': ('云南', '昆明'),
        '西藏自治区人民医院': ('西藏', '拉萨'),
    }
    
    # 统计修复前的信息
    before_province_count = len(df[df['省份'] != ''])
    before_city_count = len(df[df['城市'] != ''])
    
    print(f"修复前 - 有省份信息的记录数: {before_province_count}")
    print(f"修复前 - 有城市信息的记录数: {before_city_count}")
    
    # 修复缺失的信息
    updated_count = 0
    for index, row in df.iterrows():
        hospital_name = row['医院名称']
        
        # 检查是否在特定修复列表中
        for key, (province, city) in specific_fixes.items():
            if key in hospital_name:
                if row['省份'] == '' and province != '':
                    df.at[index, '省份'] = province
                    updated_count += 1
                if row['城市'] == '' and city != '':
                    df.at[index, '城市'] = city
                    updated_count += 1
                break
    
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
    print("开始修复特定的缺失医院地理位置信息...")
    
    try:
        df = fix_specific_missing_info()
        print("特定缺失信息修复完成！")
    except Exception as e:
        print(f"修复过程中出错: {str(e)}")

if __name__ == "__main__":
    main() 
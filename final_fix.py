import pandas as pd
import numpy as np

def final_fix_hospital_info():
    """最终修复医院地理位置信息，处理NaN值"""
    filename = "2023年度西南区专科声誉排行榜_with_info.csv"
    df = pd.read_csv(filename, encoding='utf-8-sig')
    
    print(f"正在修复文件: {filename}")
    print(f"总记录数: {len(df)}")
    
    # 将NaN值替换为空字符串
    df['省份'] = df['省份'].fillna('')
    df['城市'] = df['城市'].fillna('')
    
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

def fix_all_files():
    """修复所有文件"""
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
            df = pd.read_csv(filename, encoding='utf-8-sig')
            print(f"\n正在修复文件: {filename}")
            print(f"总记录数: {len(df)}")
            
            # 将NaN值替换为空字符串
            df['省份'] = df['省份'].fillna('')
            df['城市'] = df['城市'].fillna('')
            
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
                    elif '中国人民解放军南部战区总医院' in hospital_name:
                        new_province, new_city = '广东', '广州'
                    elif '中国人民解放军东部战区总医院' in hospital_name:
                        new_province, new_city = '江苏', '南京'
                    elif '中国人民解放军北部战区总医院' in hospital_name:
                        new_province, new_city = '辽宁', '沈阳'
                    elif '中国人民解放军中部战区总医院' in hospital_name:
                        new_province, new_city = '湖北', '武汉'
                    elif '中国人民解放军空军军医大学第一附属医院' in hospital_name:
                        new_province, new_city = '陕西', '西安'
                    elif '中国人民解放军空军军医大学第二附属医院' in hospital_name:
                        new_province, new_city = '陕西', '西安'
                    elif '中国人民解放军海军军医大学第一附属医院' in hospital_name:
                        new_province, new_city = '上海', '上海'
                    elif '中国人民解放军海军军医大学第二附属医院' in hospital_name:
                        new_province, new_city = '上海', '上海'
                    elif '中国人民解放军海军军医大学第三附属医院' in hospital_name:
                        new_province, new_city = '上海', '上海'
                    elif '中国人民解放军战略支援部队特色医学中心' in hospital_name:
                        new_province, new_city = '北京', '北京'
                    elif '中国人民解放军总医院' in hospital_name:
                        new_province, new_city = '北京', '北京'
                    # 医学院附属医院
                    elif '西南医科大学附属医院' in hospital_name:
                        new_province, new_city = '四川', '泸州'
                    elif '西南医科大学口腔医学院·附属口腔医院' in hospital_name:
                        new_province, new_city = '四川', '泸州'
                    elif '西南医科大学中西医结合学院·附属中医医院' in hospital_name:
                        new_province, new_city = '四川', '泸州'
                    elif '川北医学院附属医院' in hospital_name:
                        new_province, new_city = '四川', '南充'
                    elif '南方医科大学南方医院' in hospital_name:
                        new_province, new_city = '广东', '广州'
                    elif '南方医科大学珠江医院' in hospital_name:
                        new_province, new_city = '广东', '广州'
                    elif '南方医科大学第三附属医院' in hospital_name:
                        new_province, new_city = '广东', '广州'
                    elif '南方医科大学口腔医院' in hospital_name:
                        new_province, new_city = '广东', '广州'
                    elif '暨南大学附属穗华口腔医院' in hospital_name:
                        new_province, new_city = '广东', '广州'
                    elif '暨南大学附属第一医院' in hospital_name:
                        new_province, new_city = '广东', '广州'
                    elif '暨南大学附属第二医院' in hospital_name:
                        new_province, new_city = '广东', '广州'
                    elif '中山大学附属第一医院' in hospital_name:
                        new_province, new_city = '广东', '广州'
                    elif '中山大学附属第二医院' in hospital_name:
                        new_province, new_city = '广东', '广州'
                    elif '中山大学附属第三医院' in hospital_name:
                        new_province, new_city = '广东', '广州'
                    elif '中山大学附属第六医院' in hospital_name:
                        new_province, new_city = '广东', '广州'
                    elif '中山大学附属第七医院' in hospital_name:
                        new_province, new_city = '广东', '深圳'
                    elif '中山大学附属第八医院' in hospital_name:
                        new_province, new_city = '广东', '深圳'
                    elif '中山大学附属第九医院' in hospital_name:
                        new_province, new_city = '广东', '深圳'
                    elif '中山大学附属第十医院' in hospital_name:
                        new_province, new_city = '广东', '深圳'
                    elif '中山大学附属口腔医院' in hospital_name:
                        new_province, new_city = '广东', '广州'
                    elif '中山大学附属眼科医院' in hospital_name:
                        new_province, new_city = '广东', '广州'
                    elif '中山大学附属肿瘤医院' in hospital_name:
                        new_province, new_city = '广东', '广州'
                    # 特殊医院
                    elif '贵黔国际总医院' in hospital_name:
                        new_province, new_city = '贵州', '贵阳'
                    elif '云南省传染病医院' in hospital_name:
                        new_province, new_city = '云南', '昆明'
                    elif '云南省艾滋病关爱中心' in hospital_name:
                        new_province, new_city = '云南', '昆明'
                    elif '云南省心理卫生中心' in hospital_name:
                        new_province, new_city = '云南', '昆明'
                    elif '云南省精神病医院' in hospital_name:
                        new_province, new_city = '云南', '昆明'
                    elif '四川省精神卫生中心' in hospital_name:
                        new_province, new_city = '四川', '绵阳'
                    elif '绵阳市第三人民医院' in hospital_name:
                        new_province, new_city = '四川', '绵阳'
                    elif '自贡市第五人民医院' in hospital_name:
                        new_province, new_city = '四川', '自贡'
                    elif '遂宁市中心医院' in hospital_name:
                        new_province, new_city = '四川', '遂宁'
                    elif '绵阳市中心医院' in hospital_name:
                        new_province, new_city = '四川', '绵阳'
                    elif '成都市第四人民医院' in hospital_name:
                        new_province, new_city = '四川', '成都'
                    elif '成都市公共卫生临床医疗中心' in hospital_name:
                        new_province, new_city = '四川', '成都'
                    elif '成都市妇女儿童中心医院' in hospital_name:
                        new_province, new_city = '四川', '成都'
                    elif '重庆市精神卫生中心' in hospital_name:
                        new_province, new_city = '重庆', '重庆'
                    elif '重庆市妇幼保健院' in hospital_name:
                        new_province, new_city = '重庆', '重庆'
                    elif '四川省妇幼保健院' in hospital_name:
                        new_province, new_city = '四川', '成都'
                    elif '昆明市第三人民医院' in hospital_name:
                        new_province, new_city = '云南', '昆明'
                    elif '贵州省第二人民医院' in hospital_name:
                        new_province, new_city = '贵州', '贵阳'
                    elif '贵州医科大学第三附属医院' in hospital_name:
                        new_province, new_city = '贵州', '都匀'
                    
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
            
            total_updated += updated_count
            
        except Exception as e:
            print(f"修复文件 {filename} 时出错: {str(e)}")
    
    print(f"\n全面修复完成！总共更新了 {total_updated} 条记录的地理位置信息。")

if __name__ == "__main__":
    # final_fix_hospital_info()
    fix_all_files() 
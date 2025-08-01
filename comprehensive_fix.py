import pandas as pd
import os

def get_hospital_location_comprehensive(hospital_name):
    """综合方法获取医院地理位置信息"""
    
    # 军队医院和特殊医院映射
    military_hospitals = {
        '陆军军医大学第一附属医院': ('重庆', '重庆'),
        '陆军军医大学第二附属医院': ('重庆', '重庆'),
        '陆军军医大学第三附属医院': ('重庆', '重庆'),
        '中国人民解放军陆军特色医学中心': ('重庆', '重庆'),
        '中国人民解放军联勤保障部队第920医院': ('云南', '昆明'),
        '中国人民解放军西部战区总医院': ('四川', '成都'),
        '中国人民解放军南部战区总医院': ('广东', '广州'),
        '中国人民解放军东部战区总医院': ('江苏', '南京'),
        '中国人民解放军北部战区总医院': ('辽宁', '沈阳'),
        '中国人民解放军中部战区总医院': ('湖北', '武汉'),
        '中国人民解放军空军军医大学第一附属医院': ('陕西', '西安'),
        '中国人民解放军空军军医大学第二附属医院': ('陕西', '西安'),
        '中国人民解放军海军军医大学第一附属医院': ('上海', '上海'),
        '中国人民解放军海军军医大学第二附属医院': ('上海', '上海'),
        '中国人民解放军海军军医大学第三附属医院': ('上海', '上海'),
        '中国人民解放军战略支援部队特色医学中心': ('北京', '北京'),
        '中国人民解放军总医院': ('北京', '北京'),
        '中国人民解放军总医院第一医学中心': ('北京', '北京'),
        '中国人民解放军总医院第二医学中心': ('北京', '北京'),
        '中国人民解放军总医院第三医学中心': ('北京', '北京'),
        '中国人民解放军总医院第四医学中心': ('北京', '北京'),
        '中国人民解放军总医院第五医学中心': ('北京', '北京'),
        '中国人民解放军总医院第六医学中心': ('北京', '北京'),
        '中国人民解放军总医院第七医学中心': ('北京', '北京'),
        '中国人民解放军总医院第八医学中心': ('北京', '北京'),
    }
    
    # 医学院附属医院映射
    medical_school_hospitals = {
        '西南医科大学附属医院': ('四川', '泸州'),
        '西南医科大学口腔医学院·附属口腔医院': ('四川', '泸州'),
        '西南医科大学中西医结合学院·附属中医医院': ('四川', '泸州'),
        '川北医学院附属医院': ('四川', '南充'),
        '川北医学院附属第二医院': ('四川', '南充'),
        '川北医学院附属第三医院': ('四川', '南充'),
        '川北医学院附属第四医院': ('四川', '南充'),
        '川北医学院附属第五医院': ('四川', '南充'),
        '川北医学院附属第六医院': ('四川', '南充'),
        '川北医学院附属第七医院': ('四川', '南充'),
        '川北医学院附属第八医院': ('四川', '南充'),
        '川北医学院附属第九医院': ('四川', '南充'),
        '川北医学院附属第十医院': ('四川', '南充'),
        '南方医科大学南方医院': ('广东', '广州'),
        '南方医科大学珠江医院': ('广东', '广州'),
        '南方医科大学第三附属医院': ('广东', '广州'),
        '南方医科大学口腔医院': ('广东', '广州'),
        '暨南大学附属穗华口腔医院': ('广东', '广州'),
        '暨南大学附属第一医院': ('广东', '广州'),
        '暨南大学附属第二医院': ('广东', '广州'),
        '中山大学附属第一医院': ('广东', '广州'),
        '中山大学附属第二医院': ('广东', '广州'),
        '中山大学附属第三医院': ('广东', '广州'),
        '中山大学附属第六医院': ('广东', '广州'),
        '中山大学附属第七医院': ('广东', '深圳'),
        '中山大学附属第八医院': ('广东', '深圳'),
        '中山大学附属第九医院': ('广东', '深圳'),
        '中山大学附属第十医院': ('广东', '深圳'),
        '中山大学附属口腔医院': ('广东', '广州'),
        '中山大学附属眼科医院': ('广东', '广州'),
        '中山大学附属肿瘤医院': ('广东', '广州'),
        '中山大学附属第三医院': ('广东', '广州'),
        '中山大学附属第六医院': ('广东', '广州'),
        '中山大学附属第七医院': ('广东', '深圳'),
        '中山大学附属第八医院': ('广东', '深圳'),
        '中山大学附属第九医院': ('广东', '深圳'),
        '中山大学附属第十医院': ('广东', '深圳'),
        '中山大学附属口腔医院': ('广东', '广州'),
        '中山大学附属眼科医院': ('广东', '广州'),
        '中山大学附属肿瘤医院': ('广东', '广州'),
    }
    
    # 特殊医院映射
    special_hospitals = {
        '贵黔国际总医院': ('贵州', '贵阳'),
        '云南省传染病医院': ('云南', '昆明'),
        '云南省艾滋病关爱中心': ('云南', '昆明'),
        '云南省心理卫生中心': ('云南', '昆明'),
        '云南省精神病医院': ('云南', '昆明'),
        '四川省精神卫生中心': ('四川', '绵阳'),
        '绵阳市第三人民医院': ('四川', '绵阳'),
        '自贡市第五人民医院': ('四川', '自贡'),
        '遂宁市中心医院': ('四川', '遂宁'),
        '绵阳市中心医院': ('四川', '绵阳'),
        '成都市第四人民医院': ('四川', '成都'),
        '成都市公共卫生临床医疗中心': ('四川', '成都'),
        '成都市妇女儿童中心医院': ('四川', '成都'),
        '重庆市精神卫生中心': ('重庆', '重庆'),
        '重庆市妇幼保健院': ('重庆', '重庆'),
        '四川省妇幼保健院': ('四川', '成都'),
        '昆明市第三人民医院': ('云南', '昆明'),
        '贵州省第二人民医院': ('贵州', '贵阳'),
        '贵州医科大学第三附属医院': ('贵州', '都匀'),
    }
    
    # 省份城市映射
    province_city_map = {
        '北京': '北京',
        '天津': '天津',
        '上海': '上海',
        '重庆': '重庆',
        '河北': '石家庄',
        '山西': '太原',
        '辽宁': '沈阳',
        '吉林': '长春',
        '黑龙江': '哈尔滨',
        '江苏': '南京',
        '浙江': '杭州',
        '安徽': '合肥',
        '福建': '福州',
        '江西': '南昌',
        '山东': '济南',
        '河南': '郑州',
        '湖北': '武汉',
        '湖南': '长沙',
        '广东': '广州',
        '海南': '海口',
        '四川': '成都',
        '贵州': '贵阳',
        '云南': '昆明',
        '陕西': '西安',
        '甘肃': '兰州',
        '青海': '西宁',
        '内蒙古': '呼和浩特',
        '广西': '南宁',
        '西藏': '拉萨',
        '宁夏': '银川',
        '新疆': '乌鲁木齐',
        '香港': '香港',
        '澳门': '澳门',
        '台湾': '台北'
    }
    
    # 城市省份映射
    city_province_map = {
        '北京': '北京',
        '天津': '天津',
        '上海': '上海',
        '重庆': '重庆',
        '石家庄': '河北',
        '太原': '山西',
        '沈阳': '辽宁',
        '长春': '吉林',
        '哈尔滨': '黑龙江',
        '南京': '江苏',
        '杭州': '浙江',
        '合肥': '安徽',
        '福州': '福建',
        '南昌': '江西',
        '济南': '山东',
        '郑州': '河南',
        '武汉': '湖北',
        '长沙': '湖南',
        '广州': '广东',
        '深圳': '广东',
        '海口': '海南',
        '成都': '四川',
        '泸州': '四川',
        '南充': '四川',
        '绵阳': '四川',
        '自贡': '四川',
        '遂宁': '四川',
        '贵阳': '贵州',
        '遵义': '贵州',
        '都匀': '贵州',
        '昆明': '云南',
        '拉萨': '西藏',
        '西安': '陕西',
        '兰州': '甘肃',
        '西宁': '青海',
        '呼和浩特': '内蒙古',
        '南宁': '广西',
        '银川': '宁夏',
        '乌鲁木齐': '新疆',
        '香港': '香港',
        '澳门': '澳门',
        '台北': '台湾'
    }
    
    # 首先检查特殊医院映射
    for key, (province, city) in military_hospitals.items():
        if key in hospital_name:
            return province, city
    
    for key, (province, city) in medical_school_hospitals.items():
        if key in hospital_name:
            return province, city
    
    for key, (province, city) in special_hospitals.items():
        if key in hospital_name:
            return province, city
    
    # 然后检查省份关键词
    for province, city in province_city_map.items():
        if province in hospital_name:
            return province, city
    
    # 最后检查城市关键词
    for city, province in city_province_map.items():
        if city in hospital_name:
            return province, city
    
    return '', ''

def comprehensive_fix_csv_file(filename):
    """全面修复CSV文件中的缺失信息"""
    print(f"正在修复文件: {filename}")
    
    # 读取CSV文件
    df = pd.read_csv(filename, encoding='utf-8-sig')
    
    # 统计修复前的信息
    before_province_count = len(df[df['省份'] != ''])
    before_city_count = len(df[df['城市'] != ''])
    print(f"修复前 - 有省份信息的记录数: {before_province_count}")
    print(f"修复前 - 有城市信息的记录数: {before_city_count}")
    
    updated_count = 0
    
    # 遍历每一行
    for index, row in df.iterrows():
        hospital_name = row['医院名称']
        province = row['省份']
        city = row['城市']
        
        # 如果省份或城市为空，尝试获取信息
        if province == '' or city == '':
            new_province, new_city = get_hospital_location_comprehensive(hospital_name)
            
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
    print(f"文件已更新: {filename}\n")
    
    return df

def main():
    """主函数"""
    print("开始全面修复所有医院排行榜文件中的缺失地理位置信息...")
    
    # 所有需要修复的文件
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
        if os.path.exists(filename):
            try:
                df = comprehensive_fix_csv_file(filename)
                # 统计这个文件的更新数量
                before_count = len(df[df['省份'] == '']) + len(df[df['城市'] == ''])
                after_count = len(df[df['省份'] == '']) + len(df[df['城市'] == ''])
                total_updated += (before_count - after_count)
            except Exception as e:
                print(f"修复文件 {filename} 时出错: {str(e)}")
        else:
            print(f"文件不存在: {filename}")
    
    print(f"全面修复完成！总共更新了 {total_updated} 条记录的地理位置信息。")

if __name__ == "__main__":
    main() 
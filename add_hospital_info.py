import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
import os
from urllib.parse import urljoin, urlparse

def search_hospital_website(hospital_name):
    """
    搜索医院官网URL
    """
    try:
        # 构建搜索关键词
        search_keywords = f"{hospital_name} 官网"
        
        # 使用百度搜索
        search_url = f"https://www.baidu.com/s?wd={search_keywords}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找搜索结果链接
            links = soup.find_all('a', href=True)
            
            for link in links:
                href = link.get('href')
                if href and 'http' in href:
                    # 提取真实URL
                    if 'baidu.com' in href:
                        # 处理百度跳转链接
                        try:
                            real_response = requests.get(href, headers=headers, timeout=5, allow_redirects=True)
                            real_url = real_response.url
                        except:
                            continue
                    else:
                        real_url = href
                    
                    # 检查是否是医院官网
                    if is_hospital_website(real_url, hospital_name):
                        return real_url
            
            # 如果没有找到明确的官网，返回第一个看起来像医院的链接
            for link in links:
                href = link.get('href')
                if href and 'http' in href and not 'baidu.com' in href:
                    return href
                    
    except Exception as e:
        print(f"搜索 {hospital_name} 官网时出错: {str(e)}")
    
    return ""

def is_hospital_website(url, hospital_name):
    """
    判断是否是医院官网
    """
    try:
        # 检查URL中是否包含医院相关关键词
        hospital_keywords = ['hospital', 'medical', 'health', 'clinic', 'hospital.com', 'hospital.cn']
        url_lower = url.lower()
        
        for keyword in hospital_keywords:
            if keyword in url_lower:
                return True
        
        # 检查是否包含医院名称的关键词
        hospital_name_keywords = hospital_name.replace('医院', '').replace('大学', '').replace('附属', '')
        if hospital_name_keywords in url:
            return True
            
    except:
        pass
    
    return False

def get_hospital_location(hospital_name):
    """
    根据医院名称推断地理位置
    """
    # 省份和城市映射
    province_city_map = {
        # 东北区
        '辽宁': ['沈阳', '大连', '鞍山', '抚顺', '本溪', '丹东', '锦州', '营口', '阜新', '辽阳', '盘锦', '铁岭', '朝阳', '葫芦岛'],
        '吉林': ['长春', '吉林市', '四平', '辽源', '通化', '白山', '松原', '白城', '延边'],
        '黑龙江': ['哈尔滨', '齐齐哈尔', '鸡西', '鹤岗', '双鸭山', '大庆', '伊春', '佳木斯', '七台河', '牡丹江', '黑河', '绥化', '大兴安岭'],
        
        # 华北区
        '北京': ['北京'],
        '天津': ['天津'],
        '河北': ['石家庄', '唐山', '秦皇岛', '邯郸', '邢台', '保定', '张家口', '承德', '沧州', '廊坊', '衡水'],
        '山西': ['太原', '大同', '阳泉', '长治', '晋城', '朔州', '晋中', '运城', '忻州', '临汾', '吕梁'],
        '内蒙古': ['呼和浩特', '包头', '乌海', '赤峰', '通辽', '鄂尔多斯', '呼伦贝尔', '巴彦淖尔', '乌兰察布', '兴安盟', '锡林郭勒盟', '阿拉善盟'],
        
        # 华东区
        '上海': ['上海'],
        '江苏': ['南京', '无锡', '徐州', '常州', '苏州', '南通', '连云港', '淮安', '盐城', '扬州', '镇江', '泰州', '宿迁'],
        '浙江': ['杭州', '宁波', '温州', '嘉兴', '湖州', '绍兴', '金华', '衢州', '舟山', '台州', '丽水'],
        '安徽': ['合肥', '芜湖', '蚌埠', '淮南', '马鞍山', '淮北', '铜陵', '安庆', '黄山', '滁州', '阜阳', '宿州', '六安', '亳州', '池州', '宣城'],
        '福建': ['福州', '厦门', '莆田', '三明', '泉州', '漳州', '南平', '龙岩', '宁德'],
        '江西': ['南昌', '景德镇', '萍乡', '九江', '新余', '鹰潭', '赣州', '吉安', '宜春', '抚州', '上饶'],
        '山东': ['济南', '青岛', '淄博', '枣庄', '东营', '烟台', '潍坊', '济宁', '泰安', '威海', '日照', '莱芜', '临沂', '德州', '聊城', '滨州', '菏泽'],
        
        # 华南区
        '广东': ['广州', '韶关', '深圳', '珠海', '汕头', '佛山', '江门', '湛江', '茂名', '肇庆', '惠州', '梅州', '汕尾', '河源', '阳江', '清远', '东莞', '中山', '潮州', '揭阳', '云浮'],
        '广西': ['南宁', '柳州', '桂林', '梧州', '北海', '防城港', '钦州', '贵港', '玉林', '百色', '贺州', '河池', '来宾', '崇左'],
        '海南': ['海口', '三亚', '三沙', '儋州'],
        
        # 华中区
        '河南': ['郑州', '开封', '洛阳', '平顶山', '安阳', '鹤壁', '新乡', '焦作', '濮阳', '许昌', '漯河', '三门峡', '南阳', '商丘', '信阳', '周口', '驻马店', '济源'],
        '湖北': ['武汉', '黄石', '十堰', '宜昌', '襄阳', '鄂州', '荆门', '孝感', '荆州', '黄冈', '咸宁', '随州', '恩施'],
        '湖南': ['长沙', '株洲', '湘潭', '衡阳', '邵阳', '岳阳', '常德', '张家界', '益阳', '郴州', '永州', '怀化', '娄底', '湘西'],
        
        # 西北区
        '陕西': ['西安', '铜川', '宝鸡', '咸阳', '渭南', '延安', '汉中', '榆林', '安康', '商洛'],
        '甘肃': ['兰州', '嘉峪关', '金昌', '白银', '天水', '武威', '张掖', '平凉', '酒泉', '庆阳', '定西', '陇南', '临夏', '甘南'],
        '青海': ['西宁', '海东', '海北', '黄南', '海南', '果洛', '玉树', '海西'],
        '宁夏': ['银川', '石嘴山', '吴忠', '固原', '中卫'],
        '新疆': ['乌鲁木齐', '克拉玛依', '吐鲁番', '哈密', '昌吉', '博尔塔拉', '巴音郭楞', '阿克苏', '克孜勒苏', '喀什', '和田', '伊犁', '塔城', '阿勒泰'],
        
        # 西南区
        '四川': ['成都', '自贡', '攀枝花', '泸州', '德阳', '绵阳', '广元', '遂宁', '内江', '乐山', '南充', '眉山', '宜宾', '广安', '达州', '雅安', '巴中', '资阳', '阿坝', '甘孜', '凉山'],
        '贵州': ['贵阳', '六盘水', '遵义', '安顺', '毕节', '铜仁', '黔西南', '黔东南', '黔南'],
        '云南': ['昆明', '曲靖', '玉溪', '保山', '昭通', '丽江', '普洱', '临沧', '楚雄', '红河', '文山', '西双版纳', '大理', '德宏', '怒江', '迪庆'],
        '西藏': ['拉萨', '日喀则', '昌都', '林芝', '山南', '那曲', '阿里'],
        '重庆': ['重庆']
    }
    
    # 根据医院名称推断省份和城市
    for province, cities in province_city_map.items():
        for city in cities:
            if city in hospital_name:
                return province, city
    
    # 如果没有找到具体城市，尝试根据省份关键词推断
    for province in province_city_map.keys():
        if province in hospital_name:
            # 返回省份和空城市
            return province, ""
    
    return "", ""

def process_csv_file(filename):
    """
    处理单个CSV文件，添加医院官网URL和地理位置信息
    """
    print(f"正在处理文件: {filename}")
    
    # 读取CSV文件
    df = pd.read_csv(filename, encoding='utf-8-sig')
    
    # 添加新列
    df['官网URL'] = ""
    df['省份'] = ""
    df['城市'] = ""
    
    # 获取唯一的医院名称
    unique_hospitals = df['医院名称'].unique()
    hospital_info = {}
    
    print(f"找到 {len(unique_hospitals)} 个唯一医院")
    
    # 为每个医院查找信息
    for i, hospital in enumerate(unique_hospitals):
        print(f"正在处理 {i+1}/{len(unique_hospitals)}: {hospital}")
        
        # 查找官网URL
        website_url = search_hospital_website(hospital)
        
        # 查找地理位置
        province, city = get_hospital_location(hospital)
        
        hospital_info[hospital] = {
            'website': website_url,
            'province': province,
            'city': city
        }
        
        # 添加延时避免请求过于频繁
        time.sleep(1)
    
    # 更新DataFrame
    for hospital, info in hospital_info.items():
        mask = df['医院名称'] == hospital
        df.loc[mask, '官网URL'] = info['website']
        df.loc[mask, '省份'] = info['province']
        df.loc[mask, '城市'] = info['city']
    
    # 保存更新后的文件
    output_filename = filename.replace('.csv', '_with_info.csv')
    df.to_csv(output_filename, index=False, encoding='utf-8-sig')
    
    print(f"文件已保存为: {output_filename}")
    print(f"数据统计:")
    print(f"总记录数: {len(df)}")
    print(f"有官网URL的记录数: {len(df[df['官网URL'] != ''])}")
    print(f"有省份信息的记录数: {len(df[df['省份'] != ''])}")
    print(f"有城市信息的记录数: {len(df[df['城市'] != ''])}")
    
    return df

def main():
    """
    主函数：处理所有CSV文件
    """
    # 定义要处理的CSV文件列表
    csv_files = [
        "2023年度东北区专科声誉排行榜.csv",
        "2023年度华北区专科声誉排行榜.csv",
        "2023年度华东区专科声誉排行榜.csv",
        "2023年度华南区专科声誉排行榜.csv",
        "2023年度华中区专科声誉排行榜.csv",
        "2023年度西北区专科声誉排行榜.csv",
        "2023年度西南区专科声誉排行榜.csv"
    ]
    
    print("开始处理医院排行榜CSV文件...")
    
    for csv_file in csv_files:
        if os.path.exists(csv_file):
            try:
                df = process_csv_file(csv_file)
                print(f"{csv_file} 处理完成\n")
            except Exception as e:
                print(f"处理 {csv_file} 时出错: {str(e)}\n")
        else:
            print(f"文件不存在: {csv_file}\n")
    
    print("所有文件处理完成！")

if __name__ == "__main__":
    main() 
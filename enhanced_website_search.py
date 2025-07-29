import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
import random
from urllib.parse import quote

# 已知的医院官网数据库
KNOWN_HOSPITAL_WEBSITES = {
    # 东北区
    "中国医科大学附属第一医院": "https://www.cmu1h.com/",
    "中国医科大学附属盛京医院": "https://www.shengjing.com/",
    "吉林大学第一医院": "https://www.jdyy.cn/",
    "吉林大学第二医院": "https://www.jdey.com.cn/",
    "吉林大学中日联谊医院": "https://www.zrlyyy.com/",
    "哈尔滨医科大学附属第一医院": "https://www.hydyy.org.cn/",
    "哈尔滨医科大学附属第二医院": "https://www.hrbmush.edu.cn/",
    "哈尔滨医科大学附属肿瘤医院": "https://www.hrbmush.edu.cn/",
    "大连医科大学附属第一医院": "https://www.dmu-1.com/",
    "大连医科大学附属第二医院": "https://www.shdmu.com/",
    "辽宁省肿瘤医院暨大连理工大学附属肿瘤医院": "https://www.lnszlyy.com/",
    "中国人民解放军北部战区总医院": "https://www.81hospital.com/",
    
    # 华北区
    "北京协和医院": "https://www.pumch.cn/",
    "北京大学第一医院": "https://www.bddyyy.com.cn/",
    "北京大学人民医院": "https://www.pkuph.cn/",
    "北京大学第三医院": "https://www.puh3.net.cn/",
    "首都医科大学附属北京天坛医院": "https://www.bjtth.org/",
    "首都医科大学附属北京安贞医院": "https://www.anzhen.org/",
    "首都医科大学附属北京同仁医院": "https://www.trhos.com/",
    "首都医科大学附属北京儿童医院": "https://www.bch.com.cn/",
    "中国医学科学院阜外医院": "https://www.fuwaihospital.org/",
    "中国医学科学院肿瘤医院": "https://www.cicams.ac.cn/",
    "天津医科大学总医院": "https://www.tjmugh.com.cn/",
    "天津医科大学第二医院": "https://www.tjmu2h.com.cn/",
    "天津市第一中心医院": "https://www.tjzx.org.cn/",
    "天津市肿瘤医院": "https://www.tjmuch.com/",
    "河北医科大学第一医院": "https://www.jyyy.com.cn/",
    "河北医科大学第二医院": "https://www.hb2h.com/",
    "河北医科大学第三医院": "https://www.cthhmu.com/",
    "河北医科大学第四医院": "https://www.hbydsy.com/",
    "山西省人民医院": "https://www.sxsrmyy.com/",
    "山西医科大学第一医院": "https://www.sydyy.net/",
    "山西医科大学第二医院": "https://www.sxedfy.com/",
    "内蒙古医科大学附属医院": "https://www.nmgfy.com/",
    "内蒙古自治区人民医院": "https://www.nmgyy.cn/",
    
    # 华东区
    "复旦大学附属中山医院": "https://www.zs-hospital.sh.cn/",
    "复旦大学附属华山医院": "https://www.huashan.org.cn/",
    "复旦大学附属肿瘤医院": "https://www.shca.org.cn/",
    "复旦大学附属儿科医院": "https://ch.shmu.edu.cn/",
    "上海交通大学医学院附属瑞金医院": "https://www.rjh.com.cn/",
    "上海交通大学医学院附属仁济医院": "https://www.renji.com/",
    "上海交通大学医学院附属新华医院": "https://www.xinhuamed.com.cn/",
    "上海交通大学医学院附属第九人民医院": "https://www.9hospital.com.cn/",
    "同济大学附属同济医院": "https://www.tongjihospital.com.cn/",
    "同济大学附属东方医院": "https://www.easthospital.cn/",
    "上海市第一人民医院": "https://www.firsthospital.cn/",
    "上海市第六人民医院": "https://www.6thhosp.com/",
    "上海市第九人民医院": "https://www.9hospital.com.cn/",
    "上海市胸科医院": "https://www.shxkyy.com/",
    "上海市肺科医院": "https://www.shsfkyy.com/",
    "上海市精神卫生中心": "https://www.smhc.org.cn/",
    "南京大学医学院附属鼓楼医院": "https://www.njglyy.com/",
    "南京医科大学第一附属医院": "https://www.jsph.org.cn/",
    "南京医科大学第二附属医院": "https://www.jsnydefy.com/",
    "东南大学附属中大医院": "https://www.njzyy.com/",
    "江苏省人民医院": "https://www.jsph.org.cn/",
    "江苏省中医院": "https://www.jshtcm.com/",
    "江苏省肿瘤医院": "https://www.jszlyy.com.cn/",
    "浙江大学医学院附属第一医院": "https://www.zy91.com/",
    "浙江大学医学院附属第二医院": "https://www.z2hospital.com/",
    "浙江大学医学院附属邵逸夫医院": "https://www.srrsh.com/",
    "浙江大学医学院附属儿童医院": "https://www.zju-ch.com/",
    "浙江省人民医院": "https://www.hospitalstar.com/",
    "浙江省肿瘤医院": "https://www.zchospital.com/",
    "山东大学齐鲁医院": "https://www.qiluhospital.com/",
    "山东大学第二医院": "https://www.eyhospital.com/",
    "山东省立医院": "https://www.sph.com.cn/",
    "山东省肿瘤医院": "https://www.sdzlyy.org.cn/",
    "青岛大学附属医院": "https://www.qduh.cn/",
    "安徽省立医院": "https://www.ahslyy.com.cn/",
    "安徽医科大学第一附属医院": "https://www.ayfy.com/",
    "安徽医科大学第二附属医院": "https://www.ay2fy.com/",
    "福建省立医院": "https://www.fjsl.com.cn/",
    "福建医科大学附属第一医院": "https://www.fyyy.com/",
    "福建医科大学附属协和医院": "https://www.fjxiehe.com/",
    "江西省人民医院": "https://www.jxsrmyy.cn/",
    "南昌大学第一附属医院": "https://www.cdyfy.com/",
    "南昌大学第二附属医院": "https://www.jxndefy.cn/",
    
    # 华南区
    "中山大学附属第一医院": "https://www.gzsums.net/",
    "中山大学附属第二医院": "https://www.syshospital.com/",
    "中山大学附属第三医院": "https://www.zssy.com.cn/",
    "中山大学附属肿瘤医院": "https://www.sysucc.org.cn/",
    "中山大学附属口腔医院": "https://www.zdkqyy.com/",
    "南方医科大学南方医院": "https://www.nfyy.com/",
    "南方医科大学珠江医院": "https://www.zjyy.com.cn/",
    "广东省人民医院": "https://www.gdghospital.org.cn/",
    "广东省中医院": "https://www.gdhtcm.com/",
    "广东省妇幼保健院": "https://www.e3861.com/",
    "广州市第一人民医院": "https://www.gzhospital.cn/",
    "广州市妇女儿童医疗中心": "https://www.gzfezx.com/",
    "深圳市人民医院": "https://www.szhospital.com/",
    "深圳市第二人民医院": "https://www.szrch.com/",
    "深圳市第三人民医院": "https://www.szdsrmyy.com/",
    "深圳市儿童医院": "https://www.szkid.com.cn/",
    "广西医科大学第一附属医院": "https://www.gxmuyfy.cn/",
    "广西医科大学第二附属医院": "https://www.gxmuefy.com/",
    "广西壮族自治区人民医院": "https://www.gxhospital.com/",
    "广西壮族自治区肿瘤医院": "https://www.gxzl.com/",
    "海南省人民医院": "https://www.phhp.com.cn/",
    "海南医学院第一附属医院": "https://www.hyfy.com.cn/",
    "海南医学院第二附属医院": "https://www.hy2fy.com/",
    
    # 华中区
    "华中科技大学同济医学院附属同济医院": "https://www.tjh.com.cn/",
    "华中科技大学同济医学院附属协和医院": "https://www.whuh.com/",
    "武汉大学人民医院": "https://www.rmhospital.com/",
    "武汉大学中南医院": "https://www.znhospital.cn/",
    "湖北省人民医院": "https://www.rmhospital.com/",
    "湖北省肿瘤医院": "https://www.hbch.com.cn/",
    "中南大学湘雅医院": "https://www.xiangya.com.cn/",
    "中南大学湘雅二医院": "https://www.xyeyy.com/",
    "中南大学湘雅三医院": "https://www.xy3yy.com/",
    "湖南省人民医院": "https://www.hnsrmyy.com/",
    "湖南省肿瘤医院": "https://www.hnzlyy.com/",
    "郑州大学第一附属医院": "https://www.fcc.zzu.edu.cn/",
    "郑州大学第二附属医院": "https://www.zzusah.com/",
    "河南省人民医院": "https://www.hnsrmyy.net/",
    "河南省肿瘤医院": "https://www.anti-cancer.com.cn/",
    
    # 西北区
    "西安交通大学第一附属医院": "https://www.dyyy.xjtu.edu.cn/",
    "西安交通大学第二附属医院": "https://www.2yuan.xjtu.edu.cn/",
    "空军军医大学第一附属医院（西京医院）": "https://www.fmmu.edu.cn/",
    "空军军医大学第二附属医院（唐都医院）": "https://www.tangdu.com/",
    "陕西省人民医院": "https://www.spph-sx.com/",
    "陕西省肿瘤医院": "https://www.sxszlyy.com/",
    "兰州大学第一医院": "https://www.lzdxdyyy.com/",
    "兰州大学第二医院": "https://www.ldey.com.cn/",
    "甘肃省人民医院": "https://www.gsrmyy.com/",
    "甘肃省肿瘤医院": "https://www.gszlyy.com/",
    "青海省人民医院": "https://www.qhsrmyy.com/",
    "青海大学附属医院": "https://www.qhuah.com/",
    "宁夏医科大学总医院": "https://www.nyfy.com.cn/",
    "宁夏回族自治区人民医院": "https://www.nxrmyy.com/",
    "新疆医科大学第一附属医院": "https://www.xydyfy.com/",
    "新疆维吾尔自治区人民医院": "https://www.xjrmyy.com/",
    
    # 西南区
    "四川大学华西医院": "https://www.wchscu.cn/",
    "四川大学华西第二医院": "https://www.motherchildren.com/",
    "四川大学华西口腔医院": "https://www.hxkq.org/",
    "陆军军医大学第一附属医院": "https://www.xqhospital.com.cn/",
    "陆军军医大学第二附属医院": "https://www.xinhuahospital.com/",
    "重庆医科大学附属第一医院": "https://www.hospital-cqmu.com/",
    "重庆医科大学附属第二医院": "https://www.cqumch.com.cn/",
    "重庆医科大学附属儿童医院": "https://www.chcmu.com/",
    "重庆医科大学附属口腔医院": "https://www.cqdent.com/",
    "四川省人民医院": "https://www.samsph.com/",
    "四川省肿瘤医院": "https://www.sichuancancer.org/",
    "贵州省人民医院": "https://www.gz5055.com/",
    "贵州医科大学附属医院": "https://www.gmcah.cn/",
    "云南省第一人民医院（昆华医院）": "https://www.ynsdyrmyy.com/",
    "昆明医科大学第一附属医院": "https://www.ydyy.cn/",
    "昆明医科大学第二附属医院": "https://www.kydefy.com/",
    "西藏自治区人民医院": "https://www.xzrmyy.com/",
}

def search_hospital_website_enhanced(hospital_name):
    """增强版医院官网搜索"""
    # 首先检查已知数据库
    if hospital_name in KNOWN_HOSPITAL_WEBSITES:
        return KNOWN_HOSPITAL_WEBSITES[hospital_name]
    
    # 尝试模糊匹配
    for known_name, url in KNOWN_HOSPITAL_WEBSITES.items():
        if hospital_name in known_name or known_name in hospital_name:
            return url
    
    # 如果已知数据库中没有，尝试百度搜索
    return search_hospital_website_baidu(hospital_name)

def search_hospital_website_baidu(hospital_name):
    """使用百度搜索医院官网"""
    try:
        # 构建搜索关键词
        search_query = f"{hospital_name} 官网"
        encoded_query = quote(search_query)
        
        # 百度搜索URL
        search_url = f"https://www.baidu.com/s?wd={encoded_query}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找搜索结果中的链接
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link.get('href', '')
            text = link.get_text().strip()
            
            # 检查是否是医院官网链接
            if any(keyword in text.lower() for keyword in ['官网', '官方网站', '医院官网']):
                # 提取实际URL
                if href.startswith('/baidu.php?url='):
                    # 百度跳转链接
                    match = re.search(r'url=([^&]+)', href)
                    if match:
                        return match.group(1)
                elif href.startswith('http'):
                    return href
        
        # 如果没有找到明确的官网链接，尝试从搜索结果中提取
        for link in links:
            href = link.get('href', '')
            text = link.get_text().strip()
            
            # 检查链接是否包含医院名称
            if hospital_name in text and href.startswith('http'):
                # 检查是否是医院相关域名
                if any(domain in href for domain in ['hospital', 'med', 'health', 'gov.cn', 'edu.cn']):
                    return href
        
        return ''
        
    except Exception as e:
        print(f"搜索 {hospital_name} 官网时出错: {str(e)}")
        return ''

def supplement_website_urls_enhanced(filename):
    """为单个CSV文件补充官网URL（增强版）"""
    try:
        df = pd.read_csv(filename, encoding='utf-8-sig')
        
        # 确保官网URL列存在
        if '官网URL' not in df.columns:
            df['官网URL'] = ''
        
        # 处理NaN值
        df['官网URL'] = df['官网URL'].fillna('')
        
        print(f"处理文件: {filename}")
        print(f"总记录数: {len(df)}")
        
        # 统计缺失的URL数量
        missing_count = len(df[df['官网URL'] == ''])
        print(f"缺失官网URL的记录数: {missing_count}")
        
        if missing_count == 0:
            print("该文件没有缺失的官网URL")
            return 0
        
        updated_count = 0
        
        for index, row in df.iterrows():
            hospital_name = row['医院名称']
            current_url = row['官网URL']
            
            # 如果已经有URL，跳过
            if current_url and current_url.strip():
                continue
            
            print(f"正在搜索 {hospital_name} 的官网...")
            
            # 获取官网URL
            website_url = search_hospital_website_enhanced(hospital_name)
            
            if website_url:
                df.at[index, '官网URL'] = website_url
                updated_count += 1
                print(f"  ✓ 找到官网: {website_url}")
            else:
                print(f"  ✗ 未找到官网")
            
            # 添加随机延迟避免被封
            time.sleep(random.uniform(0.5, 1.5))
        
        # 保存更新后的文件
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f"文件 {filename} 处理完成，新增 {updated_count} 个官网URL")
        return updated_count
        
    except Exception as e:
        print(f"处理文件 {filename} 时出错: {str(e)}")
        return 0

def main():
    """主函数"""
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
            updated_count = supplement_website_urls_enhanced(filename)
            total_updated += updated_count
            print("-" * 50)
        except Exception as e:
            print(f"处理文件 {filename} 时出错: {str(e)}")
            print("-" * 50)
    
    print(f"\n所有文件处理完成！总共新增了 {total_updated} 个官网URL")

if __name__ == "__main__":
    main()
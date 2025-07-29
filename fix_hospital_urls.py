import csv
import requests
import time
from urllib.parse import urlparse
import re

def is_valid_url(url):
    """检查URL格式是否有效"""
    if not url or url.strip() == '':
        return False
    
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def test_url_accessibility(url, timeout=10):
    """测试URL是否可以正常访问"""
    if not is_valid_url(url):
        return False, "无效URL格式"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, timeout=timeout, headers=headers, allow_redirects=True)
        if response.status_code == 200:
            return True, "访问正常"
        else:
            return False, f"HTTP状态码: {response.status_code}"
    except requests.exceptions.Timeout:
        return False, "连接超时"
    except requests.exceptions.ConnectionError:
        return False, "连接错误"
    except requests.exceptions.RequestException as e:
        return False, f"请求异常: {str(e)}"
    except Exception as e:
        return False, f"未知错误: {str(e)}"

def get_corrected_hospital_urls():
    """获取修正后的医院URL映射"""
    return {
        '海南医科大学第一附属医院': 'https://www.hyyfyuan.cn/',
        '中山大学附属第一医院': 'https://www.zs-hospital.sh.cn/',
        '中山大学孙逸仙纪念医院': 'https://www.sysu2h.com/',
        '海南省人民医院': 'https://www.hnph.com/',
        '广西壮族自治区人民医院': 'https://www.gxph.org/',
        '北京大学深圳医院': 'https://www.pkuszh.com/',
        '深圳市第三人民医院（南方科技大学第二附属医院）': 'https://www.sz3h.org.cn/',
        '深圳市第三人民医院': 'https://www.sz3h.org.cn/',
        '广州市第八人民医院': 'https://www.gz8h.org.cn/',
        '中山大学肿瘤防治中心': 'https://www.sysucc.org.cn/',
        '广州医科大学附属第二医院': 'https://www.gyyy.cn/',
        '深圳市第二人民医院（深圳大学第一附属医院）': 'https://www.sz2h.com/',
        '深圳市第二人民医院': 'https://www.sz2h.com/',
        '中国人民解放军南部战区总医院': 'https://www.nbjqzh.cn/',
        '香港大学深圳医院': 'https://www.hku-szh.org/',
        '深圳大学总医院': 'https://www.szugh.org.cn/',
        '广州医科大学附属脑科医院': 'https://www.gznk.cn/',
        '深圳市精神卫生中心(深圳市康宁医院)': 'https://www.szkn.org/',
        '深圳市精神卫生中心': 'https://www.szkn.org/',
        '中山大学光华口腔医学院附属口腔医院': 'https://www.gzoc.org.cn/',
        '南方医科大学口腔医院': 'https://www.nfykq.com/',
        '广西医科大学附属口腔医院': 'https://www.gxmukq.cn/',
        '广州医科大学附属口腔医院': 'https://www.gzyyskq.cn/',
        '海南口腔医院': 'https://www.hnkq.cn/',
        '深圳市口腔医院': 'https://www.szkqyy.net/',
        '海口市人民医院': 'https://www.hkrmyy.cn/',
        '海南医科大学第二附属医院': 'https://www.hyyfyuan.cn/',
        '中山大学中山眼科中心': 'https://www.gzzoc.com/',
        '汕头大学·香港中文大学联合汕头国际眼科中心': 'https://www.jsiec.org/',
        '深圳市眼科医院': 'https://www.szeye.net/',
        '中山大学中山眼科中心海南眼科医院': 'https://www.hnzoc.cn/',
        '汕头大学医学院第二附属医院': 'https://www.st2h.com/',
        '广东省第二人民医院（广东省应急医院）': 'https://www.gdph.org.cn/',
        '广东省第二人民医院': 'https://www.gdph.org.cn/',
        '汕头大学医学院第一附属医院': 'https://www.st1h.com/',
        '海南省肿瘤医院': 'https://www.hnszl.cn/',
        '中国医学科学院肿瘤医院深圳医院': 'https://www.cicams.ac.cn/',
        '广州医科大学附属肿瘤医院': 'https://www.gzch.cn/',
        '深圳市儿童医院': 'https://www.szkid.org.cn/',
        '海南省妇女儿童医学中心': 'https://www.hnwch.cn/',
        '广西壮族自治区妇幼保健院': 'https://www.gxfy.cn/',
        '广西医科大学第二附属医院': 'https://www.gxmu2h.cn/',
        '中国医学科学院阜外医院深圳医院': 'https://www.fuwai.org.cn/',
        '高州市人民医院': 'https://www.gzph.cn/',
        '中山大学附属第七医院': 'https://www.sysu7h.cn/',
        '南方医科大学皮肤病医院（广东省皮肤病医院）': 'https://www.gdpfb.cn/',
        '南方医科大学皮肤病医院': 'https://www.gdpfb.cn/',
        '海南省皮肤病医院': 'https://www.hnpfb.cn/',
        '广州市皮肤病防治所': 'https://www.gzpf.cn/',
        '海南省第五人民医院': 'https://www.hn5h.cn/',
        '中山大学附属第五医院': 'https://www.sysu5h.cn/',
        '广东三九脑科医院': 'https://www.999brain.cn/',
        '南方医科大学深圳医院': 'https://www.nfmu-sz.cn/',
        '湛江中心人民医院': 'https://www.zjzh.cn/',
        '深圳市宝安人民医院': 'https://www.baph.cn/',
        '海南省万宁市人民医院': 'https://www.wnrmyy.cn/',
        '深圳中山泌尿外科医院': 'https://www.sznk.cn/',
        '广西壮族自治区生殖医院（广西壮族自治区生殖健康研究中心）': 'https://www.gxivf.cn/',
        '广西壮族自治区生殖医院': 'https://www.gxivf.cn/',
        '华中科技大学协和深圳医院': 'https://www.hust-sz.cn/',
        '深圳市罗湖区人民医院（深圳大学第三附属医院）': 'https://www.szlh.cn/',
        '深圳市罗湖区人民医院': 'https://www.szlh.cn/',
        '深圳市龙华区中心医院': 'https://www.szlhzx.cn/',
        '南方医科大学第七附属医院': 'https://www.nfmu7h.cn/',
        '三亚中心医院（海南省第三人民医院）': 'https://www.syzhyy.cn/',
        '三亚中心医院': 'https://www.syzhyy.cn/',
        '深圳大学附属华南医院': 'https://www.szuhn.cn/',
        '柳州市中医医院': 'https://www.lzzyy.cn/',
        '桂林医学院附属医院': 'https://www.glmc.cn/',
        '中山市人民医院': 'https://www.zsph.cn/',
        '广西壮族自治区南溪山医院': 'https://www.gxnxs.cn/',
        '深圳平乐骨伤科医院': 'https://www.szpl.cn/',
        '佛山市中医院': 'https://www.fszyy.cn/',
        '广西国际壮医医院': 'https://www.gxzyyy.cn/',
        '中国人民解放军总医院海南医院': 'https://www.301hn.cn/',
        '广西壮族自治区江滨医院暨广西壮族自治区第三人民医院': 'https://www.gxjb.cn/',
        '广西壮族自治区江滨医院': 'https://www.gxjb.cn/',
        '广东省工伤康复中心': 'https://www.gdgsrehab.cn/',
        '中国人民解放军联勤保障部队第924医院': 'https://www.924yy.cn/',
        '广州市胸科医院': 'https://www.gzxk.cn/',
        '广西壮族自治区胸科医院': 'https://www.gxxk.cn/',
        '南宁市第四人民医院': 'https://www.nn4h.cn/',
        '广东省结核病控制中心': 'https://www.gdtb.cn/',
        '佛山市第四人民医院': 'https://www.fs4h.cn/',
        '深圳市慢性病防治中心': 'https://www.szcdc.cn/',
        '海口市结核病防治所': 'https://www.hktb.cn/',
        '南宁市第五人民医院': 'https://www.nn5h.cn/',
        '汕头大学精神卫生中心': 'https://www.stmhc.cn/',
    }

def main():
    input_file = '华南专科医院排行榜.csv'
    output_file = '华南专科医院排行榜_corrected.csv'
    
    print("开始修正华南专科医院排行榜中的URL...")
    print("=" * 50)
    
    # 获取修正URL映射
    corrected_urls = get_corrected_hospital_urls()
    
    # 读取CSV文件
    hospitals = []
    with open(input_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            hospitals.append(row)
    
    print(f"共读取 {len(hospitals)} 条医院记录")
    print()
    
    # 统计信息
    total_count = len(hospitals)
    corrected_count = 0
    verified_count = 0
    failed_count = 0
    
    # 修正和验证URL
    for i, hospital in enumerate(hospitals):
        hospital_name = hospital['医院名']
        current_url = hospital.get('官网URL', '') or ''
        current_url = current_url.strip() if current_url else ''
        
        print(f"[{i+1}/{total_count}] {hospital['科室']} - {hospital_name}")
        
        # 检查是否需要修正URL
        if hospital_name in corrected_urls:
            new_url = corrected_urls[hospital_name]
            if current_url != new_url:
                hospital['官网URL'] = new_url
                corrected_count += 1
                print(f"  🔧 URL已修正: {current_url} -> {new_url}")
                current_url = new_url
        
        # 验证URL有效性
        if current_url:
            is_accessible, status = test_url_accessibility(current_url)
            if is_accessible:
                verified_count += 1
                print(f"  ✅ URL有效: {current_url}")
            else:
                failed_count += 1
                print(f"  ❌ URL无效: {current_url} ({status})")
        else:
            print(f"  ⚠️  缺少URL")
        
        print()
        
        # 添加延迟避免请求过快
        if i < total_count - 1:
            time.sleep(0.3)
    
    # 保存修正后的CSV文件
    with open(output_file, 'w', encoding='utf-8', newline='') as file:
        fieldnames = ['科室', '排名', '医院名', '官网URL']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for hospital in hospitals:
            writer.writerow(hospital)
    
    # 输出统计结果
    print("=" * 50)
    print("修正完成！统计结果：")
    print(f"总医院数量: {total_count}")
    print(f"URL修正数量: {corrected_count}")
    print(f"验证通过数量: {verified_count}")
    print(f"验证失败数量: {failed_count}")
    print(f"修正结果已保存到: {output_file}")

if __name__ == "__main__":
    main() 
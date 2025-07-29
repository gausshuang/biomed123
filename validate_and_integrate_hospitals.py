import pandas as pd
import requests
import time
import json
from urllib.parse import urlparse
import concurrent.futures
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class HospitalURLValidator:
    def __init__(self):
        self.session = requests.Session()
        
        # 设置重试策略
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # 设置请求头
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        self.valid_hospitals = []
        self.invalid_urls = []
        
    def validate_url(self, url):
        """验证单个URL是否有效"""
        if not url or url.strip() == '':
            return False, "空URL"
            
        try:
            # 确保URL有协议
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
                
            # 解析URL
            parsed = urlparse(url)
            if not parsed.netloc:
                return False, "无效URL格式"
            
            # 发送请求
            response = self.session.get(url, timeout=10, allow_redirects=True)
            
            if response.status_code == 200:
                return True, f"有效 ({response.status_code})"
            else:
                return False, f"HTTP {response.status_code}"
                
        except requests.exceptions.Timeout:
            return False, "超时"
        except requests.exceptions.ConnectionError:
            return False, "连接错误"
        except requests.exceptions.RequestException as e:
            return False, f"请求错误: {str(e)}"
        except Exception as e:
            return False, f"未知错误: {str(e)}"
    
    def validate_csv_file(self, filename):
        """验证CSV文件中的所有URL"""
        print(f"\n开始验证文件: {filename}")
        print("=" * 80)
        
        try:
            df = pd.read_csv(filename, encoding='utf-8-sig')
            df = df.fillna('')  # 处理NaN值
            
            valid_count = 0
            invalid_count = 0
            
            for index, row in df.iterrows():
                hospital_name = row['医院名称']
                url = row['官网URL']
                department = row['科室']
                rank = row['排名']
                province = row.get('省份', '')
                city = row.get('城市', '')
                
                print(f"验证 {hospital_name} - {url}")
                
                is_valid, status = self.validate_url(url)
                
                if is_valid:
                    print(f"  ✓ 有效: {status}")
                    valid_count += 1
                    
                    # 添加到有效医院列表
                    self.valid_hospitals.append({
                        'hospital_name': hospital_name,
                        'department': department,
                        'rank': rank,
                        'url': url,
                        'province': province,
                        'city': city,
                        'region': self.extract_region_from_filename(filename)
                    })
                else:
                    print(f"  ✗ 无效: {status}")
                    invalid_count += 1
                    
                    self.invalid_urls.append({
                        'hospital_name': hospital_name,
                        'url': url,
                        'status': status,
                        'file': filename
                    })
                
                # 添加延迟避免过于频繁的请求
                time.sleep(0.5)
            
            print(f"\n文件 {filename} 验证完成:")
            print(f"  有效URL: {valid_count}")
            print(f"  无效URL: {invalid_count}")
            
        except Exception as e:
            print(f"处理文件 {filename} 时出错: {str(e)}")
    
    def extract_region_from_filename(self, filename):
        """从文件名提取地区信息"""
        if '东北区' in filename:
            return '东北区'
        elif '华北区' in filename:
            return '华北区'
        elif '华东区' in filename:
            return '华东区'
        elif '华南区' in filename:
            return '华南区'
        elif '华中区' in filename:
            return '华中区'
        elif '西北区' in filename:
            return '西北区'
        elif '西南区' in filename:
            return '西南区'
        else:
            return '未知区域'
    
    def generate_website_data(self):
        """生成网站需要的数据格式"""
        # 按科室分组
        departments_data = {}
        
        for hospital in self.valid_hospitals:
            department = hospital['department']
            if department not in departments_data:
                departments_data[department] = []
            
            departments_data[department].append({
                'rank': hospital['rank'],
                'hospital': hospital['hospital_name'],
                'url': hospital['url'],
                'province': hospital['province'],
                'city': hospital['city'],
                'region': hospital['region']
            })
        
        # 按排名排序
        for department in departments_data:
            departments_data[department].sort(key=lambda x: (
                0 if x['rank'].isdigit() else 1,  # 数字排名优先
                int(x['rank']) if x['rank'].isdigit() else 999,  # 按数字大小排序
                x['rank']  # 获提名等非数字排名按字母排序
            ))
        
        return departments_data
    
    def save_results(self):
        """保存验证结果"""
        # 保存有效医院数据为JSON格式（用于网站）
        website_data = self.generate_website_data()
        with open('valid_hospitals_data.json', 'w', encoding='utf-8') as f:
            json.dump(website_data, f, ensure_ascii=False, indent=2)
        
        # 保存有效医院数据为CSV格式
        if self.valid_hospitals:
            valid_df = pd.DataFrame(self.valid_hospitals)
            valid_df.to_csv('valid_hospitals.csv', index=False, encoding='utf-8-sig')
        
        # 保存无效URL列表
        if self.invalid_urls:
            invalid_df = pd.DataFrame(self.invalid_urls)
            invalid_df.to_csv('invalid_urls.csv', index=False, encoding='utf-8-sig')
        
        print(f"\n结果保存完成:")
        print(f"  有效医院总数: {len(self.valid_hospitals)}")
        print(f"  无效URL总数: {len(self.invalid_urls)}")
        print(f"  有效科室数量: {len(self.generate_website_data())}")
    
    def generate_summary_report(self):
        """生成汇总报告"""
        print("\n" + "=" * 80)
        print("URL验证汇总报告")
        print("=" * 80)
        
        # 按地区统计
        region_stats = {}
        for hospital in self.valid_hospitals:
            region = hospital['region']
            if region not in region_stats:
                region_stats[region] = 0
            region_stats[region] += 1
        
        print("\n按地区统计有效医院数量:")
        for region, count in sorted(region_stats.items()):
            print(f"  {region}: {count}个")
        
        # 按科室统计
        dept_stats = {}
        for hospital in self.valid_hospitals:
            dept = hospital['department']
            if dept not in dept_stats:
                dept_stats[dept] = 0
            dept_stats[dept] += 1
        
        print(f"\n按科室统计 (前10个科室):")
        sorted_depts = sorted(dept_stats.items(), key=lambda x: x[1], reverse=True)
        for dept, count in sorted_depts[:10]:
            print(f"  {dept}: {count}个医院")
        
        # 无效URL统计
        if self.invalid_urls:
            print(f"\n无效URL统计:")
            error_types = {}
            for invalid in self.invalid_urls:
                error_type = invalid['status']
                if error_type not in error_types:
                    error_types[error_type] = 0
                error_types[error_type] += 1
            
            for error_type, count in sorted(error_types.items(), key=lambda x: x[1], reverse=True):
                print(f"  {error_type}: {count}个")

def main():
    validator = HospitalURLValidator()
    
    # 需要验证的CSV文件列表
    csv_files = [
        "2023年度东北区专科声誉排行榜_with_info.csv",
        "2023年度华北区专科声誉排行榜_with_info.csv", 
        "2023年度华东区专科声誉排行榜_with_info.csv",
        "2023年度华南区专科声誉排行榜_with_info.csv",
        "2023年度华中区专科声誉排行榜_with_info.csv",
        "2023年度西北区专科声誉排行榜_with_info.csv",
        "2023年度西南区专科声誉排行榜_with_info.csv"
    ]
    
    print("开始验证所有医院官网URL...")
    print(f"待验证文件数量: {len(csv_files)}")
    
    # 验证每个文件
    for csv_file in csv_files:
        try:
            validator.validate_csv_file(csv_file)
        except FileNotFoundError:
            print(f"文件 {csv_file} 不存在，跳过...")
        except Exception as e:
            print(f"处理文件 {csv_file} 时发生错误: {str(e)}")
    
    # 保存结果
    validator.save_results()
    
    # 生成汇总报告
    validator.generate_summary_report()
    
    print("\n" + "=" * 80)
    print("URL验证完成！")
    print("生成的文件:")
    print("  - valid_hospitals_data.json (网站使用)")
    print("  - valid_hospitals.csv (有效医院列表)")
    print("  - invalid_urls.csv (无效URL列表)")
    print("=" * 80)

if __name__ == "__main__":
    main()
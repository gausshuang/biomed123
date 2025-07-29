import json
import requests
from urllib.parse import urlparse
import random

def test_hospital_data_loading():
    """测试医院数据文件是否能正确加载"""
    try:
        with open('complete_hospitals_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("✅ 医院数据文件加载成功")
        print(f"   科室数量: {len(data)}")
        
        total_hospitals = sum(len(hospitals) for hospitals in data.values())
        print(f"   医院总数: {total_hospitals}")
        
        # 统计有URL的医院
        hospitals_with_url = 0
        for dept_hospitals in data.values():
            for hospital in dept_hospitals:
                if hospital.get('url') and hospital['url'].strip():
                    hospitals_with_url += 1
        
        print(f"   有官网URL: {hospitals_with_url} ({hospitals_with_url/total_hospitals*100:.1f}%)")
        return True, data
        
    except Exception as e:
        print(f"❌ 医院数据文件加载失败: {str(e)}")
        return False, None

def test_sample_urls(data, sample_size=10):
    """测试部分医院URL的有效性"""
    print(f"\n🔍 测试 {sample_size} 个医院官网URL...")
    
    # 收集所有有URL的医院
    hospitals_with_url = []
    for dept, hospitals in data.items():
        for hospital in hospitals:
            if hospital.get('url') and hospital['url'].strip() and hospital['url'] != 'nan':
                hospitals_with_url.append((dept, hospital))
    
    if not hospitals_with_url:
        print("❌ 没有找到有效的URL进行测试")
        return
    
    # 随机选择样本
    sample_hospitals = random.sample(hospitals_with_url, min(sample_size, len(hospitals_with_url)))
    
    valid_count = 0
    for dept, hospital in sample_hospitals:
        url = hospital['url']
        hospital_name = hospital['hospital']
        
        try:
            response = requests.get(url, timeout=5, allow_redirects=True,
                                  headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
            if response.status_code == 200:
                print(f"   ✅ {hospital_name[:30]:<30} - 有效")
                valid_count += 1
            else:
                print(f"   ❌ {hospital_name[:30]:<30} - HTTP {response.status_code}")
        except Exception as e:
            print(f"   ❌ {hospital_name[:30]:<30} - 错误: {str(e)[:30]}")
    
    print(f"\n📊 URL测试结果: {valid_count}/{sample_size} 有效 ({valid_count/sample_size*100:.1f}%)")

def test_data_structure(data):
    """测试数据结构的完整性"""
    print("\n🔍 测试数据结构...")
    
    required_fields = ['rank', 'hospital', 'url', 'province', 'city', 'region']
    issues = []
    
    for dept, hospitals in data.items():
        for i, hospital in enumerate(hospitals):
            for field in required_fields:
                if field not in hospital:
                    issues.append(f"{dept} 第{i+1}个医院缺少字段: {field}")
    
    if issues:
        print(f"   ❌ 发现 {len(issues)} 个数据结构问题:")
        for issue in issues[:5]:  # 只显示前5个问题
            print(f"      - {issue}")
        if len(issues) > 5:
            print(f"      ... 还有 {len(issues)-5} 个问题")
    else:
        print("   ✅ 数据结构完整")

def generate_sample_html():
    """生成一个简单的HTML测试页面"""
    html_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>医院数据测试页面</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .hospital-card { border: 1px solid #ccc; margin: 10px 0; padding: 15px; border-radius: 5px; }
        .hospital-name { font-weight: bold; font-size: 16px; }
        .hospital-info { color: #666; margin: 5px 0; }
        .hospital-url { color: #0066cc; text-decoration: none; }
        .hospital-url:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>医院数据测试页面</h1>
    <div id="hospital-list"></div>
    
    <script>
        async function loadHospitalData() {
            try {
                const response = await fetch('complete_hospitals_data.json');
                const data = await response.json();
                
                const container = document.getElementById('hospital-list');
                let totalHospitals = 0;
                
                for (const [dept, hospitals] of Object.entries(data)) {
                    totalHospitals += hospitals.length;
                    
                    // 只显示每个科室的前3个医院作为示例
                    const sampleHospitals = hospitals.slice(0, 3);
                    
                    for (const hospital of sampleHospitals) {
                        const card = document.createElement('div');
                        card.className = 'hospital-card';
                        
                        card.innerHTML = `
                            <div class="hospital-name">${hospital.hospital}</div>
                            <div class="hospital-info">科室: ${dept} | 排名: ${hospital.rank}</div>
                            <div class="hospital-info">地区: ${hospital.region || '未知'} | 省份: ${hospital.province || '未知'} | 城市: ${hospital.city || '未知'}</div>
                            <div class="hospital-info">
                                ${hospital.url ? `<a href="${hospital.url}" target="_blank" class="hospital-url">访问官网</a>` : '暂无官网'}
                            </div>
                        `;
                        
                        container.appendChild(card);
                    }
                }
                
                document.querySelector('h1').textContent = `医院数据测试页面 (总计 ${totalHospitals} 个医院)`;
                
            } catch (error) {
                console.error('加载医院数据失败:', error);
                document.getElementById('hospital-list').innerHTML = '<p style="color: red;">数据加载失败: ' + error.message + '</p>';
            }
        }
        
        loadHospitalData();
    </script>
</body>
</html>'''
    
    with open('hospital_test.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("\n📄 生成测试HTML页面: hospital_test.html")

def main():
    print("🏥 生物医学导航网站 - 医院数据测试")
    print("=" * 50)
    
    # 测试数据加载
    success, data = test_hospital_data_loading()
    
    if success and data:
        # 测试数据结构
        test_data_structure(data)
        
        # 测试部分URL
        test_sample_urls(data, 5)
        
        # 生成测试页面
        generate_sample_html()
        
        print("\n🎉 测试完成！")
        print("\n📋 建议:")
        print("   1. 在浏览器中打开 hospital_test.html 查看数据显示效果")
        print("   2. 在浏览器中打开 index.html 查看完整网站")
        print("   3. 可以运行完整的URL验证脚本进行更全面的测试")
    else:
        print("\n❌ 无法继续测试，请检查数据文件")

if __name__ == "__main__":
    main()
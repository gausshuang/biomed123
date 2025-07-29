import csv

def main():
    input_file = '华南专科医院排行榜.csv'
    output_file = '华南专科医院排行榜_fixed_urls.csv'
    
    print("开始修正海南医科大学第一附属医院的URL...")
    
    # 读取CSV文件
    hospitals = []
    with open(input_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            hospitals.append(row)
    
    # 修正URL
    fixed_count = 0
    for hospital in hospitals:
        if hospital['医院名'] == '海南医科大学第一附属医院':
            if hospital['官网URL'] != 'https://www.hyyfyuan.cn/':
                hospital['官网URL'] = 'https://www.hyyfyuan.cn/'
                fixed_count += 1
                print(f"修正: {hospital['科室']} - {hospital['医院名']}")
    
    # 保存修正后的文件
    with open(output_file, 'w', encoding='utf-8', newline='') as file:
        fieldnames = ['科室', '排名', '医院名', '官网URL']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for hospital in hospitals:
            writer.writerow(hospital)
    
    print(f"修正完成！共修正了 {fixed_count} 条记录")
    print(f"结果已保存到: {output_file}")

if __name__ == "__main__":
    main() 
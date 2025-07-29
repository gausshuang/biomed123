import pandas as pd
import os

def clean_csv_file(filename):
    """清理单个CSV文件的最后4行垃圾数据"""
    if not os.path.exists(filename):
        print(f"文件 {filename} 不存在，跳过...")
        return False
    
    try:
        # 读取CSV文件
        df = pd.read_csv(filename, encoding='utf-8-sig')
        original_count = len(df)
        
        print(f"处理文件: {filename}")
        print(f"  原始记录数: {original_count}")
        
        # 检查最后4行是否包含垃圾数据
        last_4_rows = df.tail(4)
        garbage_indicators = ['版权声明', '复旦大学医院', '沪ICP备', '地址:上海市徐汇区医学院']
        
        has_garbage = False
        for idx, row in last_4_rows.iterrows():
            hospital_name = str(row.get('医院名称', ''))
            for indicator in garbage_indicators:
                if indicator in hospital_name:
                    has_garbage = True
                    break
            if has_garbage:
                break
        
        if has_garbage:
            # 删除最后4行
            df_cleaned = df.iloc[:-4]
            cleaned_count = len(df_cleaned)
            
            # 保存清理后的文件
            df_cleaned.to_csv(filename, index=False, encoding='utf-8-sig')
            
            print(f"  ✅ 已删除垃圾数据")
            print(f"  清理后记录数: {cleaned_count}")
            print(f"  删除了 {original_count - cleaned_count} 行垃圾数据")
            
            return True
        else:
            print(f"  ✅ 未发现垃圾数据，无需清理")
            return False
            
    except Exception as e:
        print(f"  ❌ 处理文件 {filename} 时出错: {str(e)}")
        return False

def clean_all_csv_files():
    """清理所有7个CSV文件"""
    csv_files = [
        "2023年度东北区专科声誉排行榜_with_info.csv",
        "2023年度华北区专科声誉排行榜_with_info.csv", 
        "2023年度华东区专科声誉排行榜_with_info.csv",
        "2023年度华南区专科声誉排行榜_with_info.csv",
        "2023年度华中区专科声誉排行榜_with_info.csv",
        "2023年度西北区专科声誉排行榜_with_info.csv",
        "2023年度西南区专科声誉排行榜_with_info.csv"
    ]
    
    print("开始清理CSV文件中的垃圾数据...")
    print("=" * 60)
    
    cleaned_files = []
    total_removed = 0
    
    for csv_file in csv_files:
        if clean_csv_file(csv_file):
            cleaned_files.append(csv_file)
            total_removed += 4  # 每个文件删除4行
        print()
    
    print("=" * 60)
    print(f"清理完成！")
    print(f"  处理的文件数: {len(csv_files)}")
    print(f"  清理的文件数: {len(cleaned_files)}")
    print(f"  总删除记录数: {total_removed}")
    
    if cleaned_files:
        print(f"\n清理的文件列表:")
        for file in cleaned_files:
            print(f"  - {file}")
    
    return cleaned_files

def regenerate_website_data():
    """重新生成网站数据"""
    print("\n重新生成网站数据...")
    print("=" * 40)
    
    # 重新运行数据准备脚本
    import subprocess
    try:
        result = subprocess.run(['python', 'prepare_hospital_data.py'], 
                              capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print("✅ 网站数据重新生成成功")
            # 打印输出的关键信息
            lines = result.stdout.split('\n')
            for line in lines:
                if '总医院数量' in line or '总科室数量' in line or '按地区统计' in line:
                    print(f"  {line}")
        else:
            print(f"❌ 网站数据重新生成失败: {result.stderr}")
    except Exception as e:
        print(f"❌ 重新生成数据时出错: {str(e)}")

if __name__ == "__main__":
    # 清理CSV文件
    cleaned_files = clean_all_csv_files()
    
    # 如果有文件被清理，重新生成网站数据
    if cleaned_files:
        regenerate_website_data()
        print("\n🎉 垃圾数据清理和网站数据同步完成！")
    else:
        print("\n✅ 所有文件都很干净，无需处理。")
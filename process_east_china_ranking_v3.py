#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理华东专科声誉排行榜.txt文件，转换为CSV格式 - 简化版本
"""

import re
import csv
import os

def process_east_china_ranking():
    """处理华东专科声誉排行榜.txt文件"""
    
    # 读取原始文件
    input_file = "华东专科声誉排行榜.txt"
    output_file = "华东专科医院排行榜.csv"
    
    if not os.path.exists(input_file):
        print(f"错误：找不到文件 {input_file}")
        return
    
    # 存储所有数据的列表
    all_data = []
    
    # 读取文件内容
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    current_department = None
    current_rank = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 跳过标题行
        if line == "2023年度华东区专科声誉排行榜":
            continue
        
        # 检查是否是科室行（包含"医院名"的行）
        if '\t医院名' in line:
            # 提取科室名
            parts = line.split('\t医院名')
            if len(parts) > 0:
                current_department = parts[0].strip()
            continue
        
        # 检查是否是排名行（纯数字）
        if re.match(r'^\d+$', line):
            current_rank = line
            continue
        
        # 检查是否是"获提名医院"行
        if line == '获提名医院' or line.startswith('获提名'):
            current_rank = '获提名医院'
            continue
        
        # 处理医院名行
        if current_department and current_rank and line and line != '　':
            # 清理医院名
            hospital_name = line.replace('（', '(').replace('）', ')').strip()
            
            # 如果包含多个医院（用顿号分隔）
            if '、' in hospital_name:
                hospitals = hospital_name.split('、')
                for hospital in hospitals:
                    hospital = hospital.strip()
                    if hospital and hospital != '　':
                        all_data.append([current_department, current_rank, hospital])
            else:
                if hospital_name and hospital_name != '　':
                    all_data.append([current_department, current_rank, hospital_name])
    
    # 写入CSV文件
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        # 写入表头
        writer.writerow(['科室', '排名', '医院名'])
        # 写入数据
        writer.writerows(all_data)
    
    print(f"处理完成！共处理 {len(all_data)} 条记录")
    print(f"输出文件：{output_file}")
    
    # 显示前10条记录作为示例
    print("\n前10条记录示例：")
    for i, record in enumerate(all_data[:10]):
        print(f"{i+1}. {record[0]} - {record[1]} - {record[2]}")

if __name__ == "__main__":
    process_east_china_ranking() 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理华东专科声誉排行榜.txt文件，转换为CSV格式 - 修正版本
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
    
    # 跳过标题行
    start_line = 0
    for i, line in enumerate(lines):
        if "2023年度华东区专科声誉排行榜" in line:
            start_line = i + 1
            break
    
    current_department1 = None
    current_department2 = None
    
    for line_num in range(start_line, len(lines)):
        line = lines[line_num].strip()
        if not line:
            continue
        
        # 检查是否是科室标题行
        if '\t医院名\t' in line:
            parts = line.split('\t医院名\t')
            if len(parts) >= 2:
                current_department1 = parts[0].strip()
                # 检查是否有第二个科室
                remaining = parts[1].strip()
                if remaining and not remaining.startswith('　'):
                    current_department2 = remaining
                else:
                    current_department2 = None
            continue
        
        # 处理数据行
        if current_department1 and '\t' in line:
            # 分割行数据
            parts = line.split('\t')
            
            # 处理第一个科室的数据
            if len(parts) >= 2:
                rank1 = parts[0].strip()
                hospital1 = parts[1].strip()
                
                if rank1 and hospital1 and rank1 != '　' and hospital1 != '　':
                    # 处理排名
                    if rank1.isdigit():
                        rank = rank1
                    elif '获提名' in rank1:
                        rank = '获提名医院'
                    else:
                        continue
                    
                    # 处理医院名
                    if hospital1 and hospital1 != '　':
                        # 清理医院名
                        hospital_name = hospital1.replace('（', '(').replace('）', ')').replace('\n', ' ').strip()
                        
                        # 如果包含多个医院（用顿号分隔）
                        if '、' in hospital_name:
                            hospitals = hospital_name.split('、')
                            for hospital in hospitals:
                                hospital = hospital.strip()
                                if hospital and hospital != '　':
                                    all_data.append([current_department1, rank, hospital])
                        else:
                            if hospital_name and hospital_name != '　':
                                all_data.append([current_department1, rank, hospital_name])
            
            # 处理第二个科室的数据（如果存在）
            if current_department2 and len(parts) >= 4:
                rank2 = parts[2].strip()
                hospital2 = parts[3].strip()
                
                if rank2 and hospital2 and rank2 != '　' and hospital2 != '　':
                    # 处理排名
                    if rank2.isdigit():
                        rank = rank2
                    elif '获提名' in rank2:
                        rank = '获提名医院'
                    else:
                        continue
                    
                    # 处理医院名
                    if hospital2 and hospital2 != '　':
                        # 清理医院名
                        hospital_name = hospital2.replace('（', '(').replace('）', ')').replace('\n', ' ').strip()
                        
                        # 如果包含多个医院（用顿号分隔）
                        if '、' in hospital_name:
                            hospitals = hospital_name.split('、')
                            for hospital in hospitals:
                                hospital = hospital.strip()
                                if hospital and hospital != '　':
                                    all_data.append([current_department2, rank, hospital])
                        else:
                            if hospital_name and hospital_name != '　':
                                all_data.append([current_department2, rank, hospital_name])
    
    # 清理数据：移除错误的科室名称
    cleaned_data = []
    for record in all_data:
        department, rank, hospital = record
        # 移除包含"医院名"的科室名称
        if '医院名' in department:
            continue
        cleaned_data.append([department, rank, hospital])
    
    # 写入CSV文件
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        # 写入表头
        writer.writerow(['科室', '排名', '医院名'])
        # 写入数据
        writer.writerows(cleaned_data)
    
    print(f"处理完成！共处理 {len(cleaned_data)} 条记录")
    print(f"输出文件：{output_file}")
    
    # 显示前10条记录作为示例
    print("\n前10条记录示例：")
    for i, record in enumerate(cleaned_data[:10]):
        print(f"{i+1}. {record[0]} - {record[1]} - {record[2]}")

if __name__ == "__main__":
    process_east_china_ranking() 
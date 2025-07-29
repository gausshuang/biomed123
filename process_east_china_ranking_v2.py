#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理华东专科声誉排行榜.txt文件，转换为CSV格式 - 改进版本
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
        content = f.read()
    
    # 移除标题行
    content = re.sub(r'^2023年度华东区专科声誉排行榜\n', '', content)
    
    # 按科室分割内容
    # 匹配模式：科室名\t医院名
    department_pattern = r'([^　\n]+)\t医院名'
    departments = re.findall(department_pattern, content)
    
    # 分割内容为各个科室部分
    sections = re.split(department_pattern, content)
    
    current_department = None
    
    for i, section in enumerate(sections):
        if i == 0:  # 跳过第一个空部分
            continue
            
        if i % 2 == 1:  # 科室名称
            current_department = section.strip()
        else:  # 排名信息部分
            if current_department:
                # 处理排名信息
                process_ranking_section(current_department, section, all_data)
    
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

def process_ranking_section(department, section, all_data):
    """处理排名信息部分"""
    
    # 按行分割
    lines = section.strip().split('\n')
    
    current_rank = None
    current_hospitals = []
    
    for line in lines:
        line = line.strip()
        if not line or line == '　':
            continue
        
        # 检查是否是排名行
        if re.match(r'^\d+$', line):
            # 保存之前的医院
            if current_rank and current_hospitals:
                for hospital in current_hospitals:
                    if hospital.strip():
                        all_data.append([department, current_rank, hospital.strip()])
            
            current_rank = line
            current_hospitals = []
            
        elif line == '获提名医院':
            # 保存之前的医院
            if current_rank and current_hospitals:
                for hospital in current_hospitals:
                    if hospital.strip():
                        all_data.append([department, current_rank, hospital.strip()])
            
            current_rank = '获提名医院'
            current_hospitals = []
            
        elif line.startswith('获提名'):
            # 保存之前的医院
            if current_rank and current_hospitals:
                for hospital in current_hospitals:
                    if hospital.strip():
                        all_data.append([department, current_rank, hospital.strip()])
            
            current_rank = '获提名医院'
            current_hospitals = []
            
        else:
            # 处理医院名
            # 清理医院名
            hospital_name = line.replace('（', '(').replace('）', ')').strip()
            
            # 检查是否包含多个医院（用逗号分隔）
            if '、' in hospital_name:
                hospitals = hospital_name.split('、')
                for hospital in hospitals:
                    if hospital.strip():
                        current_hospitals.append(hospital.strip())
            else:
                if hospital_name:
                    current_hospitals.append(hospital_name)
    
    # 保存最后的医院
    if current_rank and current_hospitals:
        for hospital in current_hospitals:
            if hospital.strip():
                all_data.append([department, current_rank, hospital.strip()])

if __name__ == "__main__":
    process_east_china_ranking() 
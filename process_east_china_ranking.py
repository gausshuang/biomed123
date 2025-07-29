#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理华东专科声誉排行榜.txt文件，转换为CSV格式
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
    
    # 按科室分割内容
    # 使用正则表达式匹配科室名称和对应的排名信息
    sections = re.split(r'\n([^　\n]+)\t医院名', content)
    
    current_department = None
    
    for i, section in enumerate(sections):
        if i == 0:  # 跳过标题部分
            continue
            
        if i % 2 == 1:  # 科室名称
            current_department = section.strip()
        else:  # 排名信息
            if current_department:
                # 处理排名信息
                lines = section.strip().split('\n')
                
                for line in lines:
                    line = line.strip()
                    if not line or line == '　' or line == '获提名医院':
                        continue
                    
                    # 匹配排名和医院名
                    # 格式可能是：1\t医院名 或者 获提名\n医院\t医院名
                    if '\t' in line:
                        parts = line.split('\t')
                        if len(parts) >= 2:
                            rank_part = parts[0].strip()
                            hospital_part = parts[1].strip()
                            
                            # 处理排名
                            if rank_part.isdigit():
                                rank = rank_part
                            elif '获提名' in rank_part:
                                rank = '获提名医院'
                            else:
                                continue
                            
                            # 处理医院名
                            if hospital_part and hospital_part != '　':
                                # 清理医院名中的换行符
                                hospital_name = hospital_part.replace('\n', '').replace('（', '(').replace('）', ')')
                                all_data.append([current_department, rank, hospital_name])
                    
                    # 处理获提名医院的情况
                    elif '获提名' in line:
                        continue  # 跳过"获提名"行，等待下一行的医院名
                    elif line and not line.startswith('　'):
                        # 可能是单独的医院名
                        hospital_name = line.replace('\n', '').replace('（', '(').replace('）', ')')
                        if hospital_name and hospital_name != '　':
                            all_data.append([current_department, '获提名医院', hospital_name])
    
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
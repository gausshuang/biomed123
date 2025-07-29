#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终修复版：正确处理两个科室的排名和获提名医院
"""
import csv
import os

def process_east_china_ranking():
    input_file = "华东专科声誉排行榜.txt"
    output_file = "华东专科医院排行榜.csv"
    if not os.path.exists(input_file):
        print(f"错误：找不到文件 {input_file}")
        return

    all_data = []
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f]

    # 跳过标题，定位到第一个含"医院名"的行
    i = 0
    while i < len(lines):
        if "医院名" in lines[i]:
            break
        i += 1

    dept1 = dept2 = None
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        # 新科室头部
        if '\t医院名' in line:
            parts = line.split('\t')
            dept1 = parts[0].strip()
            dept2 = None
            for idx, p in enumerate(parts):
                if p.strip() == '医院名' and idx+1 < len(parts):
                    dept2 = parts[idx+1].strip()
                    break
            i += 1
            continue
        parts = line.split('\t')
        # 处理第一个科室
        if len(parts) >= 2:
            p0, p1 = parts[0].strip(), parts[1].strip()
            if p0.isdigit():
                if dept1 and p1 and p1 != '　':
                    all_data.append([dept1, p0, p1])
            elif p0.startswith('获提名'):
                # 只归属于第一个科室
                hlist = [h.strip() for h in p1.replace('、', ',').split(',') if h.strip()]
                for h in hlist:
                    all_data.append([dept1, '获提名医院', h])
                # 继续向下提取，直到遇到新科室头/新排名/新获提名/空行
                j = i+1
                while j < len(lines):
                    l2 = lines[j].strip()
                    if not l2 or l2.startswith('获提名') or l2.startswith('1') or '\t医院名' in l2:
                        break
                    p2 = l2.split('\t')
                    if len(p2) >= 1:
                        hlist2 = [h.strip() for h in p2[0].replace('、', ',').split(',') if h.strip()]
                        for h in hlist2:
                            all_data.append([dept1, '获提名医院', h])
                    j += 1
                i = j-1
        # 处理第二个科室的排名
        if len(parts) >= 4:
            p2, p3 = parts[2].strip(), parts[3].strip()
            if p2.isdigit():
                if dept2 and p3 and p3 != '　':
                    all_data.append([dept2, p2, p3])
        # 处理第二个科室的获提名医院（检查下一行）
        if dept2 and i+1 < len(lines):
            next_line = lines[i+1].strip()
            next_parts = next_line.split('\t')
            if len(next_parts) >= 4 and next_parts[2].startswith('获提名'):
                p3 = next_parts[3].strip()
                hlist = [h.strip() for h in p3.replace('、', ',').split(',') if h.strip()]
                for h in hlist:
                    all_data.append([dept2, '获提名医院', h])
                # 继续向下提取，直到遇到新科室头/新排名/新获提名/空行
                j = i+2
                while j < len(lines):
                    l2 = lines[j].strip()
                    if not l2 or l2.startswith('获提名') or l2.startswith('1') or '\t医院名' in l2:
                        break
                    p2b = l2.split('\t')
                    if len(p2b) >= 3:
                        hlist2 = [h.strip() for h in p2b[2].replace('、', ',').split(',') if h.strip()]
                        for h in hlist2:
                            all_data.append([dept2, '获提名医院', h])
                    j += 1
                i = j-1
        i += 1

    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['科室', '排名', '医院名'])
        writer.writerows(all_data)
    print(f"处理完成！共处理 {len(all_data)} 条记录")
    print(f"输出文件：{output_file}")
    print("前10条示例：")
    for row in all_data[:10]:
        print(row)

if __name__ == "__main__":
    process_east_china_ranking() 
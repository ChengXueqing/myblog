#!/usr/bin/env python3
import os

src_base = r"C:\Users\chengxueqing\WorkBuddy\2026-05-28-23-33-23\myblog-gitee\docs"
dst_base = r"C:\Users\chengxueqing\WorkBuddy\2026-05-28-23-33-23\myblog-gitee\content"

def convert_front_matter(content, filepath):
    """Convert VuePress front matter to Hugo format"""
    lines = content.split('\n')

    # Find front matter boundaries
    if not lines or lines[0] != '---':
        return content

    # Find end of front matter
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            end_idx = i
            break

    if end_idx is None:
        return content

    # Parse front matter
    fm_lines = lines[1:end_idx]
    body_lines = lines[end_idx+1:]

    title = ''
    date_str = ''

    for line in fm_lines:
        if line.startswith('title:'):
            title = line[6:].strip().strip('"').strip("'")
        elif line.startswith('date:'):
            date_str = line[5:].strip()
        elif line.startswith('lastUpdated:') and not date_str:
            date_str = line[12:].strip()

    # Convert date
    if date_str and 'T' not in date_str:
        date_str = date_str.replace(' ', 'T') + '+08:00'

    # Determine category from path
    if '/basic/' in filepath:
        category = 'basic'
    elif '/advanced/' in filepath:
        category = 'advanced'
    elif '/interview/' in filepath:
        category = 'interview'
    elif '/others/' in filepath:
        category = 'others'
    elif '/engineering/' in filepath:
        category = 'engineering'
    else:
        category = ''

    # Generate new front matter
    new_fm = f'''---
title: "{title}"
date: {date_str}
lastmod: {date_str}
categories: [{category}]
tags: []
---

'''

    return new_fm + '\n'.join(body_lines)

# Walk through docs directory
count = 0
for root, dirs, files in os.walk(src_base):
    for filename in files:
        if filename.endswith('.md'):
            src_path = os.path.join(root, filename)
            rel_path = os.path.relpath(src_path, src_base)
            dst_path = os.path.join(dst_base, rel_path)

            with open(src_path, 'r', encoding='utf-8') as f:
                content = f.read()

            converted = convert_front_matter(content, src_path)

            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            with open(dst_path, 'w', encoding='utf-8') as f:
                f.write(converted)

            print(f"Converted: {rel_path}")
            count += 1

print(f"\nTotal: {count} files converted!")

import os
import re

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

def generate_summary(directory, base_path,  level, use_natural_sort):

    summary_lines = []
    items = [item for item in os.listdir(directory) if item!="readme.md"]
    
    # 根据是否使用自然排序进行排序
    if use_natural_sort:
        items.sort(key=natural_sort_key)
    else:
        items.sort(key=lambda x: x.lower())
    
    indent = '  ' * level

    for item in items:
        path = os.path.join(directory, item)
        if os.path.isdir(path):
            # 为文件夹添加一个标题，并递归处理该文件夹
            link1=os.path.join(base_path,item)
            link = os.path.join(link1, "readme.md")
            summary_lines.append(f"{indent}* [{item}]({link})")
            new_base = os.path.join(base_path, item)
            summary_lines += [generate_summary(path, new_base, level + 1, use_natural_sort)]
        elif item.endswith(".md"):
            # 为Markdown文件添加一个条目，保留相对路径
            link = os.path.join(base_path, item)
            name = os.path.splitext(item)[0]
            summary_lines.append(f"{indent}* [{name}]({link})")

    return '\n'.join(summary_lines)

def create_summary_file(src_directory,  use_natural_sort):
    summary_content = generate_summary(src_directory, "./posts/", 0, use_natural_sort)
    with open("SUMMARY2.md", "w", encoding="utf-8") as f:
        f.write(summary_content)

src_directory = "/home/taria/gitbook/posts"  
create_summary_file(src_directory, True)

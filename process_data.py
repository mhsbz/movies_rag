import pandas as pd
import os
from tqdm import tqdm

# 创建知识库目录（如果不存在）
knowledge_base_dir = 'knowledge_base'
os.makedirs(knowledge_base_dir, exist_ok=True)

# 读取Excel文件
print("读取电影数据...")
df = pd.read_excel('data/豆瓣电影Top250.xls')

# 处理每部电影的数据并保存为单独的文本文件
print("处理电影数据并保存到知识库...")
for idx, row in tqdm(df.iterrows()):
    # 构建电影信息文本
    movie_info = f"""# {row.get('影片中文名', '')}

## 基本信息
- 影片中文名: {row.get('影片中文名', '')}
- 影片外国名: {row.get('影片外国名', '')}
- 评分: {row.get('评分', '')}
- 评价数: {row.get('评价数', '')}

## 详细信息
- 电影详情链接: {row.get('电影详情链接', '')}
- 图片链接: {row.get('图片链接', '')}
- 相关信息: {row.get('相关信息', '')}

## 概括
{row.get('概括', '')}
"""
    
    # 保存为文本文件，使用电影名称和索引作为文件名
    movie_name = row.get('影片中文名', f'movie_{idx}')
    # 确保文件名合法
    movie_name = movie_name.replace('/', '_').replace('\\', '_').replace(':', '_')
    file_path = os.path.join(knowledge_base_dir, f"{movie_name}_{idx}.txt")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(movie_info)

print(f"处理完成！共处理了 {len(df)} 部电影，数据已保存到 {knowledge_base_dir} 目录")
    
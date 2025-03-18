# 电影知识库问答系统

## 项目概述
基于RAG架构的电影知识问答系统，使用豆瓣Top250电影数据构建知识库，结合DeepSeek大模型实现智能问答。

## 主要功能
- 自动处理电影数据并构建向量知识库
- 支持连续对话的问答交互
- 基于电影元数据和剧情摘要的精准检索

## 环境要求
- Python 3.8+
- ChromaDB向量数据库

## 配置说明
1. 设置API密钥：
```
DEEPSEEK_API_KEY=your_api_key_here
```
2. 确保ChromaDB服务运行在localhost:8000
```
chroma run --path ./chroma_data
```

## 快速开始
```bash
# 安装依赖
pip install -r requirements.txt

# 处理原始数据
python process_data.py

# 启动问答系统
python rag_app.py
```


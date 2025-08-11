
1. 利用LLM从知识库中提取实体以及实体关系;
2. 利用LLM对实体联系进行聚类，生成社区摘要；
3. 在回答用户问题时利用LLM结合社区摘进行回答。

1. 提取知识图谱（Knowledge Graph）
2. 以聚类算法（Leiden）将知识图谱划分为数个社区（community）
3. 总结每个社区所表达的含义（community summary）
4. 用户查询与每个社区含义进行相似度匹配
5. 将匹配结果作为prompt上下文进行回答


## 直接安装
```bash
conda create -n graphrag python=3.10
# git clone https://github.com/microsoft/graphrag.git
pip install graphrag

mkdir -p ./ragtest/input 



python -m graphrag.index --init --root ./ragtest



python -m graphrag.query --root ./ragtest --method global "贾元春和贾宝玉的关系？"
python -m graphrag.query --root ./ragtest --method global "红楼梦中金陵十二钗有哪些人物？"
```

1. 实体图：create_base_entity_graph
2. 关系图：create_final_relationship
3. 社区摘要：create_final_community_reports

详细的日志：indexing-engine.log 

## 源码安装
```bash
# 学术加速
# source /etc/network_turbo

# 1. 创建并激活虚拟环境
conda create -n graphrag python=3.11
conda activate graphrag

# 2. 克隆源码并进入
git clone https://github.com/microsoft/graphrag.git   
cd graphrag

# 3. 安装相关依赖
# pip install poetry 
# poetry install
poetry install --no-cache # 强制从源下载，不使用本地缓存
# pip install scikit-learn

# graphrag 2.3.0 
```

## 程序运行
```bash
# 初始化
poetry run poe index --init --root .   
# python -m graphrag index --init --root .
# https://microsoft.github.io/graphrag/get_started/

# 0. 帮助信息查询
graphrag --help

# 1. 初始化 init
# graphrag init --help
graphrag init --root ./ragtest
# 根目录下生成input、prompts、.env、settings.yaml文件

# 2. 进行索引 index
# graphrag index --help 
graphrag index --root ./ragtest  --verbose


# 3. 进行查询 query
# graphrag query --help 
graphrag query --root ./ragtest --method global -q "萧炎的父亲是谁？"
graphrag query --root ./ragtest --method global -q "贾元春和贾宝玉的关系？"

run poe query --root ./ragtest --method global "..."

python -m graphrag.query --root ./hlmtest --method global "贾元春和贾宝玉的关系？"
```

## 代码阅读
```bash
graphrag
  |--cli 
      |
      ---main.py    # 定义了一个命令行界面(CLI)工具，用于操作 GraphRAG，包括init，index，query, update等命令
      | 
      ----initialize.py  # 主要为init命令的函数，创建root目录以及settings.yaml文件、.env 文件等 prompts目录等
      |
      ----index.py  # 主要为index命令的函数，并通过api.build_index 中来运行pipeline，
      |
      ----prompt_tune.py # 主要用于prompt的修改
  | 
  ---api
        |
        ---index.py  # 构建索引的pipeline以及run pipeline，得到输出结果
  |
  ---index 
       |
       ----run
             |  
             ----run_pipeline.py  # 根据config运行pipeline整个流程  
  ----config
      

graphrag/
├── cli/ # Command Line Interface tools
│ ├── main.py # Main CLI entry point (init, index, query, update commands)
│ ├── initialize.py # init command - creates root dir, settings.yaml, .env, prompts
│ ├── index.py # index command - builds index via api.build_index
│ └── prompt_tune.py # Prompt modification utilities
│
├── api/
│ └── index.py # Index building pipeline and execution
│
├── index/
│ └── run/
  ├── workflows 
      ├── run_workflow   # 
  
│ └── run_pipeline.py # Runs entire pipeline based on config
│
│
├── config/ # Configuration files
│ ├── load_config.py  # 
│
│
└── config/ # Configuration files

rm -rf   ~/.vscode-server     
```

1. 利用LLM从知识库中提取实体以及实体关系;
2. 利用LLM对实体联系进行聚类，生成社区摘要；
3. 在回答用户问题时利用LLM结合社区摘进行回答。

1. 提取知识图谱（Knowledge Graph）
2. 以聚类算法（Leiden）将知识图谱划分为数个社区（community）
3. 总结每个社区所表达的含义（community summary）
4. 用户查询与每个社区含义进行相似度匹配
5. 将匹配结果作为prompt上下文进行回答


设置num_threads == 4 

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
  ├── operations/
      ├── build_noun_graph/  # 提取名词短语
          ├── np_extractors/ # 各种名词提取器
            ├── base.py  # 
            ├── syntactic_parsing_extractor.py # 句法分析提取器，通过SpaCy进行依赖项分析和命名实体识别NER，结果比较准确，但是速度比较慢
            ├── cfg_extractor.py # 上下文无关语法CFG提取器，使用上下文无关语法规则来识别名词，在准确性和速度之间取得平衡
            ├── regex_extractor.py # 正则表达式提取器，使用专门针对英文的正则表达式，速度最快，但是仅适用于英文内容，且准确性较差
          ├── build_noun_graph.py  # 用于使用提取的名词建立知识图谱  
      ├── cluster_graph.py # 社区检测算法，根据网络链接模式将图划分为多个聚类
  ├── workflows/
      ├── run_workflow   #
      ├── create_communities.py # 社区检测工作流，以实体和关系表作为输入，并生成具有层次结构的社区表

  
│ └── run_pipeline.py # Runs entire pipeline based on config
│
│
├── config/ # Configuration files
│ ├── load_config.py  # 
│
│
└── config/ # Configuration files


graphrag/
├── cli/                    # Command-line interface (CLI) tools
│   ├── main.py             # Main entry point for CLI commands: init, index, query, update
│   ├── initialize.py       # Implements `init`: creates project root, settings.yaml, .env, and prompt templates
│   ├── index.py            # Implements `index`: orchestrates index building via api.build_index
│   └── prompt_tune.py      # Utilities for modifying and testing prompt templates
│
├── api/                    # High-level application programming interface
│   └── index.py            # Public API for index building; exposes build_index() function for external use
│
├── index/                  # Core indexing logic and data processing
│   └── run/
│       ├── operations/     # Atomic data processing operations
│       │   ├── build_noun_graph/           # Noun phrase extraction and co-occurrence graph construction
│       │   │   ├── np_extractors/          # Noun phrase extraction strategies
│       │   │   │   ├── base.py             # Base abstract class: BaseNounPhraseExtractor
│       │   │   │   ├── syntactic_parsing_extractor.py  # Syntax-based extractor using SpaCy dependency parsing + NER (high accuracy, slower)
│       │   │   │   ├── cfg_extractor.py    # Context-Free Grammar (CFG) extractor – balances speed and accuracy
│       │   │   │   └── regex_extractor.py  # Regex-based extractor – fastest, English-only, lower accuracy
│       │   │   └── build_noun_graph.py     # Constructs noun co-occurrence graph from extracted phrases
│       │   │
│       │   └── cluster_graph.py            # Community detection algorithm (e.g., Leiden) to cluster nodes based on connectivity
│       │
│       └── workflows/                      # Composable workflow definitions
│           ├── run_workflow                # Workflow execution engine – runs modular processing steps
│           ├── factory.py                  # 模式选择，method分为fast和standard两种
│           └── create_communities.py       # Workflow: takes entities and relationships as input, outputs hierarchical community structure
│
├── config/                 # Configuration management
|   ├── models /
|   |   ├── graph_rag_config.py  # 
|   |
│   └── load_config.py      # Loads and validates configuration from settings.yaml and environment variables
├── storage/
|   ├── blob_pipeline_storage.py  # 
|   ├── Fcosmosdb_pipeline_storage.py  # 
|   ├── factory.py  # 
|   ├── file_pipeline_storage.py  # 
|   ├── memory_pipeline_storage.py  #
|   └── pipeline_storage.py  # 
|   
│
└── run_pipeline.py         # Entry script to execute the full indexing pipeline based on configuration

# rm -rf   ~/.vscode-server     
```
## 模型调用过程

```python
register_chat -> create_chat_model -> create_openai_chat_llm -> OpenAITextChatLLMImpl
```


## index 流程

```python
# standard 
"load_input_documets",
"create_base_text_units",
"create_final_documents",
"extract_graph",
"finalize_graph",
"extract_covariates",
"create_communities",
"create_final_text_units",
"create_community_reports",
"generate_text_embeddings",

# fast 
"create_base_text_units",
"create_final_documents",
"extract_graph_nlp",
"prune_graph",
"finalize_graph",
"create_communities",
"create_final_text_units",
"create_community_reports_text",
"generate_text_embeddings",


### 1. main command 
# graphrag/cli/index.index_cli
outputs = asyncio.run(
    api.build_index(
        config=config,
        method=method,
        is_update_run=is_update_run,
        memory_profile=memprofile,
        progress_logger=progress_logger,
    )
)

### 2. build index
# graphrag/api/index/api.build_index
pipeline = PipelineFactory.create_pipeline(config, method)
workflow_callbacks.pipeline_start(pipeline.names())
async for output in run_pipeline(
    pipeline,
    config,
    callbacks=workflow_callbacks,
    logger=logger,
    is_update_run=is_update_run,
)
workflow_callbacks.pipeline_end(outputs)

### 3. run pipeline 
# graphrag/index/run/run_pipeline.run_pipeline 
graphrag/index/run/run_pipeline._run_pipeline
async for table in _run_pipeline(
    pipeline=pipeline,
    config=config,
    logger=logger,
    context=context,
):  # 异步迭代
    yield table  # 生成器函数

### 4. run workflow 
# graphrag/index/run/run_pipeline._run_pipeline  
for name, workflow_function in pipeline.run():
    ...
    result = await workflow_function(config, context)
    ...
    yield PipelineRunResult(
        workflow=name, result=result.result, state=context.state, errors=None
    )

### （1） load_input_documents 
# graphrag/index/workflows/load_input_documents
output = await load_input_documents(
    config.input,
    context.input_storage,
    context.progress_logger,
)

### （2） create_base_text_units 
# graphrag/index/workflows/create_base_text_units
output = create_base_text_units(
    documents,
    context.callbacks,
    chunks.group_by_columns,
    chunks.size,
    chunks.overlap,
    chunks.encoding_model,
    strategy=chunks.strategy,
    prepend_metadata=chunks.prepend_metadata,
    chunk_size_includes_metadata=chunks.chunk_size_includes_metadata,
)

###  (3)  create_final_documents 
# graphrag/index/workflows/create_final_documents
output = create_final_documents(documents, text_units)


### （4） extract_graph 
# graphrag/index/workflows/extract_graph
entities, relationships, raw_entities, raw_relationships = await extract_graph(
    text_units=text_units,
    callbacks=context.callbacks,
    cache=context.cache,
    extraction_strategy=extraction_strategy,
    extraction_num_threads=extract_graph_llm_settings.concurrent_requests,
    extraction_async_mode=extract_graph_llm_settings.async_mode,
    entity_types=config.extract_graph.entity_types,
    summarization_strategy=summarization_strategy,
    summarization_num_threads=summarization_llm_settings.concurrent_requests,
)
...
extracted_entities, extracted_relationships = await extractor(
    text_units=text_units,
    callbacks=callbacks,
    cache=cache,
    text_column="text",
    id_column="id",
    strategy=extraction_strategy,
    async_mode=extraction_async_mode,
    entity_types=entity_types,
    num_threads=extraction_num_threads,
)
...
# graphrag/index/operations/extract_graph/extract_graph
async def extract_graph -> tuple[pd.DataFrame, pd.DataFrame]:
    ...
    # run_graph_intelligence -> run_extract_graph
    strategy_exec = _load_strategy(
        strategy.get("type", ExtractEntityStrategyType.graph_intelligence)
    )

    async def run_strategy(row):
        nonlocal num_started
        text = row[text_column]
        id = row[id_column]
        result = await strategy_exec(
            [Document(text=text, id=id)],
            entity_types,
            callbacks,
            cache,
            strategy_config,
        )
        num_started += 1
        return [result.entities, result.relationships, result.graph]

    results = await derive_from_rows(
          text_units,
          run_strategy,
          callbacks,
          async_type=async_mode,
          num_threads=num_threads,
      )
    ...
    return (entities, relationships)
  
# graphrag/index/operations/extract_graph/graph_intelligence_strategy.py
async def run_extract_graph -> EntityExtractionResult:
    ...
    # GraphExtractor
    results = await extractor(
        list(text_list),
        {
            "entity_types": entity_types,   
            "tuple_delimiter": tuple_delimiter,
            "record_delimiter": record_delimiter,
            "completion_delimiter": completion_delimiter,
        },
    )
   ...
   return EntityExtractionResult(entities, relationship, graph)

# graphrag/index/operations/extract_graph/graph_extractor 
class GraphExtractor:
  ...
  def __call__ -> GraphExtractionResult:
    ...
    result = await self._process_document(text, prompt_variables)
    ...
  
  async def _process_document:
    ...
    response = await self._model.achat(
          self._extraction_prompt.format(**{
              **prompt_variables,
              self._input_text_key: text,
          }),
      )
    ...
    for i in range(self._max_gleanings):
      response = await self._model.achat(
          CONTINUE_PROMPT,
          name=f"extract-continuation-{i}",
          history=response.history,
      )
      results += response.output.content or ""


    async def _process_results -> nx.Graph
        graph = nx.Graph() 


###  summarize descriptions

# graphrag/index/operations/summarize_descriptions/summarize_descriptions
async with semaphore:
    results = await strategy_exec(
        id, descriptions, callbacks, cache, strategy_config
    )
    ticker(1)

# finalize graph
# graphrag/index/workflows/finalize_graph
final_entities, final_relationships = finalize_graph(
    entities,
    relationships,
    callbacks=context.callbacks,
    embed_config=config.embed_graph,
    layout_enabled=config.umap.enabled,
)

```

实体关系补充抽取流程
```python
async def _process_document(
    self, text: str, prompt_variables: dict[str, str]
) -> str:
    response = await self._model.achat(
        self._extraction_prompt.format(**{
            **prompt_variables,
            self._input_text_key: text,
        }),
    )
    results = response.output.content or ""

    # if gleanings are specified, enter a loop to extract more entities
    # there are two exit criteria: (a) we hit the configured max, (b) the model says there are no more entities
    if self._max_gleanings > 0:  # 补充抽取次数
        for i in range(self._max_gleanings):
            response = await self._model.achat(
                CONTINUE_PROMPT,
                name=f"extract-continuation-{i}",
                history=response.history,
            )
            results += response.output.content or ""

            # if this is the final glean, don't bother updating the continuation flag
            if i >= self._max_gleanings - 1:
                break

            response = await self._model.achat(
                LOOP_PROMPT,
                name=f"extract-loopcheck-{i}",
                history=response.history,
            )
            if response.output.content != "Y":
                break

    return results
```
这段代码是 GraphExtractor 类中的一个异步方法 _process_document，用于处理单个文档文本，向大语言模型（LLM）发送抽取实体和关系的请求，并根据配置多次补充抽取（gleanings）。

具体流程如下：

首先，使用 self._extraction_prompt 和 prompt_variables 以及当前 text 组装提示词，调用模型的 achat 方法，得到初步抽取结果。
如果配置了 max_gleanings（补充抽取次数），则进入循环，每次用 CONTINUE_PROMPT 让模型继续抽取更多实体/关系，并将新结果追加到 results。
每次补充抽取后，如果不是最后一次，还会用 LOOP_PROMPT 询问模型是否还有更多实体可抽取。如果模型回复不是 "Y"，则提前退出循环。
最终返回所有抽取结果字符串。
简而言之，这段代码实现了“多轮补充抽取”，直到达到最大次数或模型认为没有更多实体可抽取为止。
 



```bash
# 打包
tar -zcvf ragtest.tar.gz ragtest 

# 解压
tar -zxvf ragtest.tar.gz
```

## bug 注意

当运行相同数据时，由于没有清楚缓存cache，很可能导致llm回复不带history，后续需要详细分析代码。
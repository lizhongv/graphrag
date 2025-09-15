
目前使用的 2.3.0 版本


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
# 加载每个文件，根据文件内容生成对应的hash作为id（gen_sha512_hash），最后将item包装成pd.DataFrame
# 然后将pd数据写入 documents.parquet

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
# 加载docuemts.parquet
# 将文档进行切块
# 每个切块，根据块内容生成hash作为id（gen_sha512_hash）
# 然后将pd数据存储为 text_units.parquet

###  (3)  create_final_documents 
# graphrag/index/workflows/create_final_documents
output = create_final_documents(documents, text_units)
# 加载 text_units.parquet文件
# 


### （4） extract_graph 

### （5）finalize_graph
# graphrag/index/workflows/finalize_graph
final_entities, final_relationships = finalize_graph(
    entities,
    relationships,
    callbacks=context.callbacks,
    embed_config=config.embed_graph,
    layout_enabled=config.umap.enabled,
)

### （6）extract_covariates

##   (7) create_communities 

##  （8）
```

# Extract Graph
## workflows

```python
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

# 总结实体和关系
entity_summaries, relationship_summaries = await summarize_descriptions(
    entities_df=extracted_entities,
    relationships_df=extracted_relationships,
    callbacks=callbacks,
    cache=cache,
    strategy=summarization_strategy,
    num_threads=summarization_num_threads,
)
```

## extract_graph

提供批处理引擎，并合并所有的Graph

```python
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

    # 批处理引擎
    results = await derive_from_rows(
          text_units,
          run_strategy,
          callbacks,
          async_type=async_mode,
          num_threads=num_threads,
      )
    ...
    
    # 合并批量构建的Graph
    entity_dfs = []
    relationship_dfs = []
    for result in results:
        if result:
            entity_dfs.append(pd.DataFrame(result[0]))
            relationship_dfs.append(pd.DataFrame(result[1]))

    entities = _merge_entities(entity_dfs)
    relationships = _merge_relationships(relationship_dfs)

    return (entities, relationships)
```


## GraphExtractor

用于抽取实体和关系，并构建出Graph。

```python
# graphrag/index/operations/extract_graph/graph_extractor 
class GraphExtractor:
  ....
  async def __call__():
    ....
    for doc_index, text in enumerate(texts):
        try:
            # Invoke the entity extraction
            result = await self._process_document(text, prompt_variables)
            source_doc_map[doc_index] = text
            all_records[doc_index] = result
    ...
    output = await self._process_results(
        all_records,
        prompt_variables.get(self._tuple_delimiter_key, DEFAULT_TUPLE_DELIMITER),
        prompt_variables.get(self._record_delimiter_key, DEFAULT_RECORD_DELIMITER),
    )
    return GraphExtractionResult(
        output=output,
        source_docs=source_doc_map,
    )

    async def _process_document(
        self, text: str, prompt_variables: dict[str, str]
    ) -> str:
       
        response = await self._model.achat(
            prompt, history=[]
        )
        results = response.output.content or ""
        history = [
            {'role': 'user', 'content': prompt},
            {'role': 'assistant', 'content': response.output.content or ""}
        ]  

        if self._max_gleanings > 0:  # 补充抽取次数
            for i in range(self._max_gleanings):
                response = await self._model.achat(
                    CONTINUE_PROMPT,
                    name=f"extract-continuation-{i}",
                    history=history,
                )
                results += response.output.content or ""
                history.append({'role': 'user', 'content': CONTINUE_PROMPT})
                history.append({'role': 'assistant', 'content': response.output.content or ""})

                if i >= self._max_gleanings - 1:
                    break

                response = await self._model.achat(
                    LOOP_PROMPT,
                    name=f"extract-loopcheck-{i}",
                    history=history,  
                )  # 判断是否继续进行抽取
                history.append({'role': 'user', 'content': LOOP_PROMPT})
                history.append({'role': 'assistant', 'content': response.output.content or ""})
                if response.output.content != "Y":
                    break

        return results
    
    async def _process_results() -> nx.Graph:
        graph = nx.Graph()

        graph.add_node(
            entity_name,
            type=entity_type,
            description=entity_description,
            source_id=str(source_doc_id),
        )

        graph.add_edge(
            source,
            target,
            weight=weight,
            description=edge_description,
            source_id=edge_source_id,
        ) 
```

## SummarizeExtractor
```python


```
 


# 其他
```bash
# 打包
tar -zcvf ragtest.tar.gz ragtest 

# 解压
tar -zxvf ragtest.tar.gz
```

## bug 注意

当运行相同数据时，由于没有清楚缓存cache，很可能导致llm回复不带history，后续需要详细分析代码。

## cache 

```python
# llm cache 
# fnllm/openai/services/openai_text_chat_cache_adapter

class OpenAITextChatCacheAdapter:
    ...
    def build_cache_key(
        self, prompt: OpenAIChatCompletionInput, kwargs: LLMInput[Any, Any, Any]
    ) -> str:
        """Build a cache key from the prompt and kwargs."""
        name = kwargs.get("name")
        return self._cache.create_key(
            self.get_cache_input_data(prompt, kwargs),
            prefix=f"chat_{name}" if name else "chat",
        )
    ...

# fnllm/caching/base
class Cache(ABC):
    ... 
    def create_key(self, data: Any, *, prefix: str | None = None) -> str:
        """Create a custom key by hashing the data. Returns `{data_hash}_v{strategy_version}` or `{prefix}_{data_hash}_v{strategy_version}`."""
        data_hash = _hash(json.dumps(data, sort_keys=True))

        if prefix is not None:
            return f"{prefix}_{data_hash}_v{self.__cache_strategy_version__}"

        return f"{data_hash}_v{self.__cache_strategy_version__}"
    ...

# 先从 cache 中查找，如果存在则直接返回结果，不调用 LLM。
# 但在之前的实体抽取流程中，从 cache 读取 response 后，并没有像直接调用 LLM 那样将结果注入到 history 中。
# 这会导致后续补充抽取（多轮抽取）时，无法利用历史对话（history）继续补充实体，影响抽取的完整性。
```

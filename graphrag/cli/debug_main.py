# run_graphrag_directly.py

import asyncio
from pathlib import Path
from graphrag.config.defaults import graphrag_config_defaults
from graphrag.config.enums import IndexingMethod, SearchMethod
from graphrag.logger.types import LoggerType
from graphrag.prompt_tune.defaults import LIMIT, MAX_TOKEN_COUNT, N_SUBSET_MAX, K
from graphrag.prompt_tune.types import DocSelectionType

# --- 配置区域 ---
# 选择要运行的命令: "init", "index", "update", "prompt-tune", "query"
COMMAND_TO_RUN = "index"  

# --- 通用参数 (对应 CLI 的 --root, --config 等) ---
# PROJECT_ROOT 对应 CLI 的 --root (-r)
PROJECT_ROOT = Path(r"C:\Users\lizhong\Documents\codes\graphrag\ragtest")
# CONFIG_PATH 对应 CLI 的 --config (-c)
CONFIG_PATH = Path(r"C:\Users\lizhong\Documents\codes\graphrag\ragtest\settings.yaml") # 如果文件不存在，CLI 会传 None

# --- Index / Update 命令参数 ---
INDEX_METHOD = IndexingMethod("standard") # 使用默认值 "standard"
INDEX_VERBOSE = False # 对应 --verbose (-v)
INDEX_MEMPROFILE = False # 对应 --memprofile
INDEX_LOGGER = LoggerType("rich") # 使用默认值 "rich"
INDEX_DRY_RUN = False # 对应 --dry-run
INDEX_CACHE = graphrag_config_defaults.cache # 使用默认值 True
INDEX_SKIP_VALIDATION = False # 对应 --skip-validation
# INDEX_OUTPUT_DIR 对应 CLI 的 --output (-o)
# INDEX_OUTPUT_DIR = Path("./my_index_output") # 可以设置为 None 以使用配置文件中的值
INDEX_OUTPUT_DIR = None 

# --- Prompt-Tune 命令参数 ---
PROMPT_TUNE_VERBOSE = False # 对应 --verbose (-v)
PROMPT_TUNE_LOGGER = LoggerType("rich") # 使用默认值 "rich"
PROMPT_TUNE_DOMAIN = None # 对应 --domain (如果为 None，会从数据推断)
PROMPT_TUNE_SELECTION_METHOD = DocSelectionType.RANDOM  # 使用默认值 "random"
PROMPT_TUNE_N_SUBSET_MAX = N_SUBSET_MAX # 对应 --n-subset-max, 默认 300
PROMPT_TUNE_K = K # 对应 --k, 默认 15
PROMPT_TUNE_LIMIT = LIMIT # 对应 --limit, 默认 15
PROMPT_TUNE_MAX_TOKENS = MAX_TOKEN_COUNT # 对应 --max-tokens, 默认 2000
PROMPT_TUNE_MIN_EXAMPLES_REQUIRED = 2 # 对应 --min-examples-required, 默认 2
# 使用 chunks 配置的默认值
PROMPT_TUNE_CHUNK_SIZE = graphrag_config_defaults.chunks.size # 对应 --chunk-size, 默认 1200
PROMPT_TUNE_OVERLAP = graphrag_config_defaults.chunks.overlap # 对应 --overlap, 默认 100
PROMPT_TUNE_LANGUAGE = None # 对应 --language (如果为 None，会使用默认语言)
PROMPT_TUNE_DISCOVER_ENTITY_TYPES = True # 对应 --discover-entity-types/--no-discover-entity-types, 默认 True
# PROMPT_TUNE_OUTPUT_DIR 对应 CLI 的 --output (-o)
PROMPT_TUNE_OUTPUT_DIR = Path("prompts") # 默认 "prompts"

# --- Query 命令参数 ---
QUERY_METHOD = SearchMethod.LOCAL # 对应 --method (-m)
QUERY_TEXT = "What are the main themes?" # 对应 --query (-q)
# QUERY_DATA_DIR 对应 CLI 的 --data (-d)
QUERY_DATA_DIR = Path("./index_outputs") # 包含 parquet 文件的目录
QUERY_COMMUNITY_LEVEL = 2 # 对应 --community-level, 默认 2
QUERY_DYNAMIC_COMMUNITY_SELECTION = False # 对应 --dynamic-community-selection/--no-dynamic-selection, 默认 False
QUERY_RESPONSE_TYPE = "Multiple Paragraphs" # 对应 --response-type, 默认 "Multiple Paragraphs"
QUERY_STREAMING = False # 对应 --streaming/--no-streaming, 默认 False

# --- Init 命令参数 ---
INIT_FORCE = False # 对应 --force (-f)

# --- 直接运行逻辑 ---
def run_init():
    """运行初始化命令."""
    print("Running 'init' command...")
    from graphrag.cli.initialize import initialize_project_at
    # 确保根目录存在
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
    initialize_project_at(path=PROJECT_ROOT, force=INIT_FORCE)
    print("Init command completed.")

def run_index():
    """运行索引命令."""
    print("Running 'index' command...")
    from graphrag.cli.index import index_cli
    # 确保根目录存在
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
    index_cli(
        root_dir=PROJECT_ROOT,
        verbose=INDEX_VERBOSE,
        memprofile=INDEX_MEMPROFILE,
        cache=INDEX_CACHE,
        logger=INDEX_LOGGER,
        config_filepath=CONFIG_PATH if CONFIG_PATH.exists() else None,
        dry_run=INDEX_DRY_RUN,
        skip_validation=INDEX_SKIP_VALIDATION,
        output_dir=INDEX_OUTPUT_DIR if INDEX_OUTPUT_DIR and INDEX_OUTPUT_DIR.exists() else None,
        method=INDEX_METHOD,
    )
    print("Index command completed.")

def run_update():
    """运行更新命令."""
    print("Running 'update' command...")
    from graphrag.cli.index import update_cli
    # 确保根目录存在
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
    update_cli(
        root_dir=PROJECT_ROOT,
        verbose=INDEX_VERBOSE, # 使用与 index 相同的设置
        memprofile=INDEX_MEMPROFILE, # 使用与 index 相同的设置
        cache=INDEX_CACHE,
        logger=INDEX_LOGGER, # 使用与 index 相同的设置
        config_filepath=CONFIG_PATH if CONFIG_PATH.exists() else None,
        skip_validation=INDEX_SKIP_VALIDATION, # 使用与 index 相同的设置
        output_dir=INDEX_OUTPUT_DIR if INDEX_OUTPUT_DIR and INDEX_OUTPUT_DIR.exists() else None, # 可以指定不同的输出目录
        method=INDEX_METHOD,
    )
    print("Update command completed.")

def run_prompt_tune():
    """运行提示调优命令."""
    print("Running 'prompt-tune' command...")
    from graphrag.cli.prompt_tune import prompt_tune
    # 确保根目录存在
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
    # prompt_tune 是一个异步函数，需要使用 asyncio.run()
    asyncio.run(
        prompt_tune(
            root=PROJECT_ROOT,
            config=CONFIG_PATH if CONFIG_PATH.exists() else None,
            domain=PROMPT_TUNE_DOMAIN,
            verbose=PROMPT_TUNE_VERBOSE,
            logger=PROMPT_TUNE_LOGGER,
            selection_method=PROMPT_TUNE_SELECTION_METHOD,
            limit=PROMPT_TUNE_LIMIT,
            max_tokens=PROMPT_TUNE_MAX_TOKENS,
            chunk_size=PROMPT_TUNE_CHUNK_SIZE,
            overlap=PROMPT_TUNE_OVERLAP,
            language=PROMPT_TUNE_LANGUAGE,
            discover_entity_types=PROMPT_TUNE_DISCOVER_ENTITY_TYPES,
            output=PROMPT_TUNE_OUTPUT_DIR,
            n_subset_max=PROMPT_TUNE_N_SUBSET_MAX,
            k=PROMPT_TUNE_K,
            min_examples_required=PROMPT_TUNE_MIN_EXAMPLES_REQUIRED,
        )
    )
    print("Prompt-tune command completed.")

def run_query():
    """运行查询命令."""
    print(f"Running 'query' command with method '{QUERY_METHOD.value}'...")
    from graphrag.cli.query import (
        run_basic_search,
        run_drift_search,
        run_global_search,
        run_local_search,
    )
    # 确保根目录存在
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)

    # 构建传递给查询函数的通用参数字典
    common_kwargs = {
        "config_filepath": CONFIG_PATH if CONFIG_PATH.exists() else None,
        "data_dir": QUERY_DATA_DIR,
        "root_dir": PROJECT_ROOT,
        "streaming": QUERY_STREAMING,
        "query": QUERY_TEXT,
    }

    # 根据方法选择调用相应的查询函数
    if QUERY_METHOD == SearchMethod.LOCAL:
        run_local_search(
            **common_kwargs,
            community_level=QUERY_COMMUNITY_LEVEL,
            response_type=QUERY_RESPONSE_TYPE,
        )
    elif QUERY_METHOD == SearchMethod.GLOBAL:
        run_global_search(
            **common_kwargs,
            community_level=QUERY_COMMUNITY_LEVEL,
            dynamic_community_selection=QUERY_DYNAMIC_COMMUNITY_SELECTION,
            response_type=QUERY_RESPONSE_TYPE,
        )
    elif QUERY_METHOD == SearchMethod.DRIFT:
        run_drift_search(
            **common_kwargs,
            community_level=QUERY_COMMUNITY_LEVEL, # DRIFT 查询通常也需要 community_level
            response_type=QUERY_RESPONSE_TYPE,     # DRIFT 查询通常也需要 response_type
        )
    elif QUERY_METHOD == SearchMethod.BASIC:
        # BASIC 查询不使用 community_level 和 response_type
        run_basic_search(**common_kwargs)
    else:
        raise ValueError(f"Invalid or unsupported query method: {QUERY_METHOD}")
    print("Query command completed.")

if __name__ == "__main__":
    print(f"Starting GraphRAG command: {COMMAND_TO_RUN}")
    try:
        if COMMAND_TO_RUN == "init":
            run_init()
        elif COMMAND_TO_RUN == "index":
            run_index()
        elif COMMAND_TO_RUN == "update":
            run_update()
        elif COMMAND_TO_RUN == "prompt-tune":
            run_prompt_tune()
        elif COMMAND_TO_RUN == "query":
            run_query()
        else:
            raise ValueError(f"Unknown command: {COMMAND_TO_RUN}. Please choose from 'init', 'index', 'update', 'prompt-tune', 'query'.")
    except Exception as e:
        print(f"An error occurred while running '{COMMAND_TO_RUN}': {e}")
        # 重新抛出异常以显示完整堆栈跟踪
        raise

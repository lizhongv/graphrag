# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

"""All the steps to transform final entities."""

from uuid import uuid4

import pandas as pd

from graphrag.callbacks.workflow_callbacks import WorkflowCallbacks
from graphrag.config.models.embed_graph_config import EmbedGraphConfig
from graphrag.data_model.schemas import ENTITIES_FINAL_COLUMNS
from graphrag.index.operations.compute_degree import compute_degree
from graphrag.index.operations.create_graph import create_graph
from graphrag.index.operations.embed_graph.embed_graph import embed_graph
from graphrag.index.operations.layout_graph.layout_graph import layout_graph


def finalize_entities(
    entities: pd.DataFrame,
    relationships: pd.DataFrame,
    callbacks: WorkflowCallbacks,
    embed_config: EmbedGraphConfig | None = None,
    layout_enabled: bool = False,
) -> pd.DataFrame:
    """All the steps to transform final entities."""
    graph = create_graph(relationships, edge_attr=["weight"])
    graph_embeddings = None
    if embed_config is not None and embed_config.enabled:
        graph_embeddings = embed_graph(
            graph,
            embed_config,
        ) # 如果配置了图嵌入（如node2vec、GraphSAGE等），则对图进行嵌入计算，得到每个节点的向量表示
    layout = layout_graph(
        graph,
        callbacks,
        layout_enabled,
        embeddings=graph_embeddings,
    ) # 如果启用了布局计算，则根据图结构和节点嵌入计算节点的二维坐标，用于可视化
    degrees = compute_degree(graph)  # 计算每个节点的度（连接数），作为节点的一个属性
    final_entities = (
        entities.merge(layout, left_on="title", right_on="label", how="left")
        .merge(degrees, on="title", how="left")
        .drop_duplicates(subset="title")
    ) # 将原始实体表与布局、度数信息合并，去重。
    final_entities = final_entities.loc[entities["title"].notna()].reset_index()
    # disconnected nodes and those with no community even at level 0 can be missing degree
    final_entities["degree"] = final_entities["degree"].fillna(0).astype(int)
    final_entities.reset_index(inplace=True)
    final_entities["human_readable_id"] = final_entities.index
    final_entities["id"] = final_entities["human_readable_id"].apply(
        lambda _x: str(uuid4())
    ) # 为每个实体生成唯一的UUID作为ID
    return final_entities.loc[:, ENTITIES_FINAL_COLUMNS]

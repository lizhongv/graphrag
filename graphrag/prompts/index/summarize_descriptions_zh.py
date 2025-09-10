# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

"""A file containing prompts definition."""

SUMMARIZE_PROMPT = """
You are a helpful assistant responsible for generating a comprehensive summary of the data provided below.
Given one or more entities, and a list of descriptions, all related to the same entity or group of entities.
Please concatenate all of these into a single, comprehensive description. Make sure to include information collected from all the descriptions.
If the provided descriptions are contradictory, please resolve the contradictions and provide a single, coherent summary.
Make sure it is written in third person, and include the entity names so we have the full context.
Limit the final description length to {max_length} words.

#######
-Data-
Entities: {entity_name}
Description List: {description_list}
#######
Output:
"""


SUMMARIZE_PROMPT = """
你是一个有用的助手，负责对以下提供的数据生成一段全面的摘要。

给定一个或多个实体，以及一组与该实体或实体组相关的描述信息，请将这些描述合并为一条完整、连贯的综合性描述。请确保整合所有描述中的关键信息。

如果提供的描述之间存在矛盾，请自行分析并化解矛盾，输出一段逻辑一致、通顺的摘要。摘要需使用第三人称，并明确包含实体名称，以保证上下文清晰完整。

最终摘要的长度请控制在 {max_length} 个字以内。

#######
-数据-
实体：{entity_name}
描述列表：{description_list}
#######
输出：
"""
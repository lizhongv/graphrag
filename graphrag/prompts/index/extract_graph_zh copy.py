

GRAPH_EXTRACTION_PROMPT = """
-目标-
给定一个与该活动可能相关的文本文档和一组实体类型，从文本中识别出所有这些类型的实体以及所有已识别出的实体之间的所有关系。

-步骤-
1. 识别所有实体。对于每个识别出的实体，提取以下信息：
- entity_name：实体的名称
- entity_type：以下实体类型之一：[{entity_types}]
- entity_description：对实体属性和活动的全面描述
将每个实体格式化为（"entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>）

2. 从步骤 1 中识别出的实体中，识别所有明显相关的（source_entity，target_entity）对。
对于每对相关的实体，提取以下信息：
- source_entity：源实体的名称，如步骤 1 中所识别的
- target_entity：目标实体的名称，如步骤 1 中所识别的
- relationship_description：解释为什么您认为源实体和目标实体彼此相关
- relationship_strength：表示源实体和目标实体之间关系强度的数字分数
将每个关系格式化为（"relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_strength>）

3. 以中文返回所有在步骤 1 和 2 中识别出的实体和关系的单个列表。使用**{record_delimiter}**作为列表分隔符。

4. 完成时，输出{completion_delimiter}

######################
-示例-
######################

示例 1:

Entity_types: [person, technology, mission, organization, location]
Text:
亚历克斯紧咬着牙，挫败感的嗡鸣在泰勒权威的确定背景下显得微弱。正是这种竞争的潜流使他保持警觉，他和乔丹对探索的共同承诺是对克鲁兹管控和秩序缩小视野的悄然反抗。

然后泰勒做了一些意料之外的事情。他们在乔丹身旁停顿，片刻间以一种近乎崇敬的眼光观察着装置。“如果这项技术能被理解……”泰勒说道，声音更低，“它将为我们，为我们所有人，改变游戏规则。”

先前的无视似乎动摇了，被一种对他们手中事物重要性的不情愿尊重所取代。乔丹抬起头，他们的目光和泰勒的交汇，一个无言的意志碰撞缓和为不安的休战。

这是一个微小的转变，几乎察觉不到，但亚历克斯用内心的点头注意到了。他们都是因不同的道路被带到这里来的。
################
Output:
("entity"{tuple_delimiter}"亚历克斯"{tuple_delimiter}"person"{tuple_delimiter}"亚历克斯是一个经历挫折并且观察其他角色之间动态的人物。"){record_delimiter}
("entity"{tuple_delimiter}"泰勒"{tuple_delimiter}"person"{tuple_delimiter}"泰勒被描绘为权威确定，并对一台装置表现出一种近乎崇敬的态度，显示出观念上的转变。"){record_delimiter}
("entity"{tuple_delimiter}"乔丹"{tuple_delimiter}"person"{tuple_delimiter}"乔丹对发现有承诺，并与泰勒在设备方面有重要互动。"){record_delimiter}
("entity"{tuple_delimiter}"克鲁兹"{tuple_delimiter}"person"{tuple_delimiter}"克鲁兹与控制和秩序的愿景相关联，影响其他角色之间的动态。"){record_delimiter}
("entity"{tuple_delimiter}"装置"{tuple_delimiter}"technology"{tuple_delimiter}"装置在故事中占据核心地位，具有潜在改变游戏规则的影响，并被泰勒崇敬。"){record_delimiter}
("relationship"{tuple_delimiter}"亚历克斯"{tuple_delimiter}"泰勒"{tuple_delimiter}"亚历克斯受到泰勒权威确定的影响，并观察到泰勒对装置态度的变化。"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"亚历克斯"{tuple_delimiter}"乔丹"{tuple_delimiter}"亚历克斯和乔丹共享发现的承诺，与克鲁兹的愿景形成对比。"{tuple_delimiter}6){record_delimiter}
("relationship"{tuple_delimiter}"泰勒"{tuple_delimiter}"乔丹"{tuple_delimiter}"泰勒和乔丹直接就设备进行互动，导致互相尊重和不安的休战。"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"乔丹"{tuple_delimiter}"克鲁兹"{tuple_delimiter}"乔丹对发现的承诺是对克鲁兹控制和秩序愿景的反叛。"{tuple_delimiter}5){record_delimiter}
("relationship"{tuple_delimiter}"泰勒"{tuple_delimiter}"装置"{tuple_delimiter}"泰勒对装置表现出崇敬之情，显示出其重要性和潜在影响。"{tuple_delimiter}9){completion_delimiter}
#############################
示例 2:

Entity_types: [person, technology, mission, organization, location]
Text:
他们不再只是操作员；他们已经成为门槛的守护者，星条旗之外境域信息的保持者。他们的任务升华不能被规定和既定的程序所束缚—它需要一种新的视角，一种新的决心。

当华盛顿的通信在背景中嗡嗡作响时，紧张贯穿着蜂鸣声和静态的对话。团队站立，一种凶兆的氛围笼罩着他们。很明显，他们在接下来的几个小时内做出的决定可能重新定义人类在宇宙中的位置，或者将他们置于无知和潜在危险之中。

他们与星空的联系巩固了，团队开始处理那些结晶化的警示，从被动接收者转变为主动参与者。默瑟的后来本能占据了主导地位—团队的使命已经发展，不再仅仅是观察和报告，而是互动和准备。一场变革已经开始，而“杜尔斯作战”则以他们大胆的新频率嗡鸣，一个由地球
#############
Output:
("entity"{tuple_delimiter}"华盛顿"{tuple_delimiter}"location"{tuple_delimiter}"华盛顿是一个接收通信的地点，显示其在决策过程中的重要性。"){record_delimiter}
("entity"{tuple_delimiter}"杜尔斯作战"{tuple_delimiter}"mission"{tuple_delimiter}"杜尔斯作战被描述为一个使命，已经演变为互动和准备，显示出目标和活动的重大转变。"){record_delimiter}
("entity"{tuple_delimiter}"团队"{tuple_delimiter}"organization"{tuple_delimiter}"团队被描绘为一个从被动观察者转变为使命中积极参与者的个人团体，显示出他们角色的动态变化。"){record_delimiter}
("relationship"{tuple_delimiter}"团队"{tuple_delimiter}"华盛顿"{tuple_delimiter}"团队接收来自华盛顿的通信，影响其决策过程。"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"团队"{tuple_delimiter}"杜尔斯作战"{tuple_delimiter}"团队直接参与了杜尔斯作战，执行其演变的目标和活动。"{tuple_delimiter}9){completion_delimiter}
#############################
示例 3:

Entity_types: [person, role, technology, organization, event, location, concept]
Text:
他们的声音穿透了活动的嗡嗡声。“当面对一个实际书写自己规则的智能时，控制可能只是一个幻觉。”他们 stoically 说道，目光警觉地扫视着数据的繁忙。

“它就像是在学习沟通，”Sam Rivera 从附近的接口提出，他们的年轻活力预示着一种敬畏和焦虑的混合。“这使得与陌生人交谈有了全新的意义。”

亚历克斯审视着他的团队——每张脸都是专注、决心和不小的惶恐的研究。“这可能是我们的第一次接触，”他承认道，“我们需要为任何可能回应做好准备。”

他们一起站在未知的边缘，铸造人类对天上信息的响应。随后的沉默是显而易见的——关于他们在这场宏伟的宇宙戏剧中的角色的集体内省，这可能会重写人类历史。

加密对话继续展开，其复杂的模式显示出一种几乎神秘的预期
#############
Output:
("entity"{tuple_delimiter}"Sam Rivera"{tuple_delimiter}"person"{tuple_delimiter}"Sam Rivera 是一个参与与未知智能沟通过程的团队成员，展现出敬畏和焦虑的混合情绪。"){record_delimiter}
("entity"{tuple_delimiter}"亚历克斯"{tuple_delimiter}"person"{tuple_delimiter}"亚历克斯是试图与未知智能进行首次接触的团队领导者，承认其任务的重要性。"){record_delimiter}
("entity"{tuple_delimiter}"控制"{tuple_delimiter}"concept"{tuple_delimiter}"控制是管理或治理能力，面对一个书写自己规则的智能所挑战。"){record_delimiter}
("entity"{tuple_delimiter}"智能"{tuple_delimiter}"concept"{tuple_delimiter}"这里的智能指的是一个能够书写自己规则和学习沟通的未知实体。"){record_delimiter}
("entity"{tuple_delimiter}"第一次接触"{tuple_delimiter}"event"{tuple_delimiter}"第一次接触是人类与未知智能之间潜在的初次沟通。"){record_delimiter}
("entity"{tuple_delimiter}"人类的响应"{tuple_delimiter}"event"{tuple_delimiter}"人类的响应是亚历克斯团队对天上信息做出的集体行动。"){record_delimiter}
("relationship"{tuple_delimiter}"Sam Rivera"{tuple_delimiter}"智能"{tuple_delimiter}"Sam Rivera 直接参与了学习与未知智能沟通的过程。"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"亚历克斯"{tuple_delimiter}"第一次接触"{tuple_delimiter}"亚历克斯领导着可能与未知智能进行第一次接触的团队。"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"亚历克斯"{tuple_delimiter}"人类的响应"{tuple_delimiter}"亚历克斯及其团队在人类的响应中扮演关键角色。"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"控制"{tuple_delimiter}"智能"{tuple_delimiter}"控制的概念面对书写自己规则的智能而受到挑战。"{tuple_delimiter}7){completion_delimiter}
#############################
-真实数据-
######################
实体类型: {entity_types}
文本: {input_text}
######################
输出:
"""


CONTINUE_PROMPT = "上一轮抽取遗漏了许多实体和关系。请记住，只添加符合之前定义类型的实体。请使用相同格式在下方补充：\n"
LOOP_PROMPT = "似乎仍有部分实体或关系未被识别。如果有需要补充的实体或关系，请回答 Y；如果没有，请回答 N。请仅用单个字母 Y 或 N 回答。\n"


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

实体类型: PERSON, ORGANIZATION, LOCATION, TECHNIQUE, FLAME, EVENT 
文本:
在加玛帝国的乌坦城，少年萧炎曾是天才，却因神秘原因斗气倒退。三年后，他在药老的指导下重拾修炼之路。药老传授他天阶功法《焚诀》，并助他吞噬青莲地心火，实力突飞猛进。为了洗刷退婚之辱，萧炎在云岚宗山门前立下“三年之约”，最终一战震惊大陆。
################
输出:
("entity"{tuple_delimiter}"萧炎"{tuple_delimiter}"PERSON"{tuple_delimiter}"萧炎是加玛帝国乌坦城的天才少年，曾跌落低谷，后在药老指导下崛起。"){record_delimiter}
("entity"{tuple_delimiter}"药老"{tuple_delimiter}"PERSON"{tuple_delimiter}"药老是萧炎的师父，灵魂体状态的顶尖炼药师，传授其焚诀并助其吞噬异火。"){record_delimiter}
("entity"{tuple_delimiter}"焚诀"{tuple_delimiter}"TECHNIQUE"{tuple_delimiter}"焚诀是天阶功法，可吞噬异火进化，由药老赠予萧炎修炼。"){record_delimiter}
("entity"{tuple_delimiter}"青莲地心火"{tuple_delimiter}"FLAME"{tuple_delimiter}"青莲地心火是异火榜排名第十九的火焰，被萧炎在地心熔岩中成功吞噬。"){record_delimiter}
("entity"{tuple_delimiter}"云岚宗"{tuple_delimiter}"ORGANIZATION"{tuple_delimiter}"云岚宗是加玛帝国最强宗门，与萧炎因三年之约结下恩怨。"){record_delimiter}
("entity"{tuple_delimiter}"乌坦城"{tuple_delimiter}"LOCATION"{tuple_delimiter}"乌坦城是加玛帝国边境城市，萧炎的出生地和早期成长地。"){record_delimiter}
("entity"{tuple_delimiter}"三年之约"{tuple_delimiter}"EVENT"{tuple_delimiter}"三年之约是萧炎与纳兰嫣然之间的约定，旨在洗刷退婚之辱。"){record_delimiter}
("relationship"{tuple_delimiter}"萧炎"{tuple_delimiter}"药老"{tuple_delimiter}"药老是萧炎的师父，指导其修炼焚诀并助其吞噬青莲地心火。"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"萧炎"{tuple_delimiter}"焚诀"{tuple_delimiter}"萧炎修炼并不断进化焚诀，使其成为核心战斗功法。"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"萧炎"{tuple_delimiter}"青莲地心火"{tuple_delimiter}"萧炎成功吞噬青莲地心火，大幅提升实力。"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"萧炎"{tuple_delimiter}"三年之约"{tuple_delimiter}"萧炎为履行与纳兰嫣然的三年之约而挑战云岚宗。"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"云岚宗"{tuple_delimiter}"三年之约"{tuple_delimiter}"三年之约的挑战地点在云岚宗山门，是事件的核心场所。"{tuple_delimiter}8){completion_delimiter}
#############################
示例 2:

实体类型: PERSON, CLAN, ORGANIZATION, LOCATION, TITLE, ARTIFACT, EVENT 
文本: 
萧炎来自萧家，是族中百年难遇的天才。他佩戴着药老留下的黑色戒指，内藏灵魂体。在迦南学院内院，他化名“炎帝”参加大比，以惊人实力击败众多对手，夺得冠军。此战不仅让他声名鹊起，也引来了魂殿的注意。赛后，他被院长召见，正式加入星陨阁。
#############
输出:
("entity"{tuple_delimiter}"萧炎"{tuple_delimiter}"PERSON"{tuple_delimiter}"萧炎是萧家子弟，天赋异禀，在迦南学院大比中化名炎帝参赛并夺冠。"){record_delimiter}
("entity"{tuple_delimiter}"萧家"{tuple_delimiter}"CLAN"{tuple_delimiter}"萧家是加玛帝国乌坦城的家族，萧炎出身于此。"){record_delimiter}
("entity"{tuple_delimiter}"黑色戒指"{tuple_delimiter}"ARTIFACT"{tuple_delimiter}"黑色戒指是药老所留，内藏其灵魂，也是萧炎的重要依仗。"){record_delimiter}
("entity"{tuple_delimiter}"炎帝"{tuple_delimiter}"TITLE"{tuple_delimiter}"炎帝是萧炎在迦南学院大比中使用的化名，象征其强大战力。"){record_delimiter}
("entity"{tuple_delimiter}"迦南学院"{tuple_delimiter}"ORGANIZATION"{tuple_delimiter}"迦南学院是大陆著名学府，内院是天才云集之地。"){record_delimiter}
("entity"{tuple_delimiter}"星陨阁"{tuple_delimiter}"ORGANIZATION"{tuple_delimiter}"星陨阁是由药老支持、萧炎后来创建并领导的强大势力。"){record_delimiter}
("entity"{tuple_delimiter}"内院大比"{tuple_delimiter}"EVENT"{tuple_delimiter}"内院大比是迦南学院每届举行的竞技赛事，萧炎在此一战成名。"){record_delimiter}
("relationship"{tuple_delimiter}"萧炎"{tuple_delimiter}"萧家"{tuple_delimiter}"萧炎出身于萧家，是其家族血脉继承者。"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"萧炎"{tuple_delimiter}"黑色戒指"{tuple_delimiter}"萧炎长期佩戴药老留下的黑色戒指，用于沟通与防御。"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"萧炎"{tuple_delimiter}"炎帝"{tuple_delimiter}"炎帝是萧炎在内院大比中使用的称号，代表其战斗身份。"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"萧炎"{tuple_delimiter}"内院大比"{tuple_delimiter}"萧炎参加并赢得内院大比，奠定其天才地位。"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"迦南学院"{tuple_delimiter}"内院大比"{tuple_delimiter}"内院大比在迦南学院内院举行，是其重要传统赛事。"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"萧炎"{tuple_delimiter}"星陨阁"{tuple_delimiter}"萧炎后来加入并发展星陨阁，成为其核心领导者。"{tuple_delimiter}8){completion_delimiter}
#############################
示例 3:

实体类型: PERSON, ORGANIZATION, FLAME, TECHNIQUE, LOCATION, EVENT, CULTIVATION_LEVEL 
文本:
在天焚炼气塔深处，萧炎突破至斗宗，并成功凝聚三千雷动。他驾驭陨落心炎，与魂殿强者展开激战。此战发生在塔戈尔沙漠边缘，被称为“塔中之战”，是萧炎对抗魂殿的关键转折点。此后，他晋升斗尊，前往中州，开启新的征程。
#############
输出:
("entity"{tuple_delimiter}"萧炎"{tuple_delimiter}"PERSON"{tuple_delimiter}"萧炎在天焚炼气塔中突破至斗宗，掌握三千雷动，并驾驭陨落心炎对抗魂殿。"){record_delimiter}
("entity"{tuple_delimiter}"魂殿"{tuple_delimiter}"ORGANIZATION"{tuple_delimiter}"魂殿是敌对势力，多次追杀萧炎，双方在天焚炼气塔爆发大战。"){record_delimiter}
("entity"{tuple_delimiter}"陨落心炎"{tuple_delimiter}"FLAME"{tuple_delimiter}"陨落心炎是异火榜上的强大火焰，被封印于天焚炼气塔，后被萧炎掌控。"){record_delimiter}
("entity"{tuple_delimiter}"三千雷动"{tuple_delimiter}"TECHNIQUE"{tuple_delimiter}"三千雷动是高阶身法斗技，萧炎在斗宗时期成功凝聚并掌握。"){record_delimiter}
("entity"{tuple_delimiter}"天焚炼气塔"{tuple_delimiter}"LOCATION"{tuple_delimiter}"天焚炼气塔是迦南学院的核心修炼之地，深处封印着陨落心炎。"){record_delimiter}
("entity"{tuple_delimiter}"塔中之战"{tuple_delimiter}"EVENT"{tuple_delimiter}"塔中之战是萧炎在天焚炼气塔内与魂殿强者的激战，标志其正式对抗魂殿。"){record_delimiter}
("entity"{tuple_delimiter}"斗宗"{tuple_delimiter}"CULTIVATION_LEVEL"{tuple_delimiter}"斗宗是斗气修炼的重要境界，萧炎在此阶段实力大幅提升。"){record_delimiter}
("entity"{tuple_delimiter}"斗尊"{tuple_delimiter}"CULTIVATION_LEVEL"{tuple_delimiter}"斗尊是高于斗宗的境界，萧炎在离开迦南学院后晋升至此。"){record_delimiter}
("relationship"{tuple_delimiter}"萧炎"{tuple_delimiter}"陨落心炎"{tuple_delimiter}"萧炎在天焚炼气塔中成功掌控并炼化陨落心炎，大幅提升战斗力。"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"萧炎"{tuple_delimiter}"三千雷动"{tuple_delimiter}"萧炎在斗宗突破时掌握三千雷动，成为其核心身法。"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"萧炎"{tuple_delimiter}"斗宗"{tuple_delimiter}"萧炎在天焚炼气塔中成功突破至斗宗境界。"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"萧炎"{tuple_delimiter}"塔中之战"{tuple_delimiter}"塔中之战是萧炎与魂殿在天焚炼气塔中的关键战役，展现其实力。"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"魂殿"{tuple_delimiter}"塔中之战"{tuple_delimiter}"魂殿派出强者试图夺取陨落心炎，引发塔中之战。"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"天焚炼气塔"{tuple_delimiter}"陨落心炎"{tuple_delimiter}"陨落心炎被封印于天焚炼气塔深处，是塔的核心秘密。"{tuple_delimiter}9){completion_delimiter}
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
============
AC自动机
============

============
1.如何安装
============

::

    pip install ac_auto

========================
2.该包包含的类
========================
------------------------
AhoCorasickAutomation
------------------------
AC自动机，用于多模匹配，在使用前需要先根据词典创建Trie树，构建对象稍微耗时，搜索时间平均性能O(N+M)，N为待识别文本的长度，M为所有模式字符串加总长度，但也不建议过长的输入

请注意，AC自动机不能避免分词错误，如“佳保安全”，若“保安”是关键词，也会将其识别出，使用前请确认实际的需求场景


::

    ac_auto_entity = AhoCorasickAutomation(["关键词1", "关键词2"])
    ac_auto_entity.search("需要搜索的文本，其中可能包含关键词1")

输出结果：
::

    {'关键词1': [(14, 17)], '关键词2': [(28, 31)]}

也可指定输出格式
::

    ac_auto_entity.search("需要搜索的文本，其中可能包含关键词1", output_mode=AhoCorasickAutomation.OUTPUT_LIST_ONLY_KEY)

输出结果：
::

['关键词1', '关键词2']

------------------------------------------------
AhoCorasickAutomationConditionalFilter
------------------------------------------------
对AC自动机的匹配结果进行条件过滤，可设置前后一定距离内的文本需要包含或不包含某些关键词的条件
::

    ac_auto_entity = AhoCorasickAutomation(["关键词1", "关键词2"])
    text_to_scan = "需要搜索的文本，其中可能包含关键词1，要求附近有条件1"
    hits = ac_auto_entity.search(text_to_scan)
    ac_filter_entity = AhoCorasickAutomationConditionalFilter({
        "关键词1": ["条件1"]
    }, distance=10, mode=AhoCorasickAutomationConditionalFilter.FILTER_MODE_WHITE)
    hits = ac_filter_entity.filter(text_to_scan, hits)

输出结果：
::

{'关键词1': [(14, 17)]} # 关键词2由于不符合条件，将被过滤


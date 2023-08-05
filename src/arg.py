# -*- coding: utf-8 -*-
# Time    : 2023-08-04 20:13
# Author  : Jiang Liu
# Desc    : 

import argparse

from src.i18n import translate as t

description_text = t({
    "en": r"""
Docsify Merger is a tool that combines multiple Markdown documents into a single document. 
It can recombine documents into a single Markdown file based on the structure defined in the "_sidebar.md" file. 
This tool has the following features:
- Maintains existing hierarchical relationships: Merges multiple Markdown documents based on the hierarchical relationships in the “_sidebar.md” file
- Uniform title numbering: Removes original title numbers and renumbers titles
- Removes internal links: Links within the document pointing to other titles will be removed to avoid non-existent link paths in the exported Markdown document
- Highly customizable: Customize the regular expression for title deletion, customize title generation rules
- High fault tolerance: Provides optional strategies for unprocessed titles and titles beyond the sixth level
You can then convert the exported Markdown document into formats such as PDF, Word, HTML, PNG, etc. Software like Pandoc or Typora can be used to accomplish this step.
You can check out more information on Github:...

""",
    "zh": r"""
Docsify Merger 是一款将多个Markdown文档合并为一个文档的工具。它能够根据 "_sidebar.md" 文件所定义的文档结构，重新合并为单一的Markdown文档。
该工具具有以下特点：
- 维持原有的层级关系：根据“_sidebar.md”文件中的层级关系合并多个Markdown文档
- 统一标题编号：去掉原来的标题编号，并重新给标题编号
- 去除内链：文档中指向其他标题的链接将会被去除，以免导出的Markdown文档出现链接路径不存在的情况
- 高度自定义：自定义标题删除的正则表达式，自定义标题生成规则
- 较高容错率：提供可选的未处理标题和大于六级标题的策略
您可以将导出的Markdown文档转换为PDF、Word、HTML、PNG等格式。可以使用Pandoc或Typora等软件完成这一步。
您可以在Github上查看更多信息：...

"""
})

r_help_text = t({
    "en": r"""
The configuration file path for the regular expression used to remove title numbers, the default value is stored in "./config/remove_number_config.json." 
You can enter the path to the configuration file to customize which title numbers need to be removed. 
The configuration file is a JSON file, with a structure like: ["^(\d+\.)+", "^\d+[\.\\d+]*", ...]
The default values and the corresponding title numbers that will be removed are as follows:
- '^(\d+\.)+': '1.', '1.2.', '1.2.3'
- '^(\d+\.)+': '1.', '1.2.', '1.2.3'
- '^\d+[\.\d+]*': '1.1', '1.2.1'
- '^第[零一二三四五六七八九十]+(章|节|小节|讲|部分)': '第一章', '第十二章', '第六节', '第七小节', '第二讲', '第八部分'
- '^[\(\[\{]?[a-zA-Z0-9]+[\)\]\}]': '(1)', '[a]', '{A}', '1]', 'A)', 'a}', '(a1)', '(Aa)'

""",
    "zh": r"""
用于删除标题编号的正则表达式的配置文件路径，默认值存储在"./config/remove_number_config.json"中。您可以输入配置文件的路径以自定义哪些标题编号需要删除。
配置文件是一个 JSON 文件，其结构为：["^(\d+\.)+", "^\d+[\.\\d+]*", ...]
默认值以及对应将会删除的标题编号如下：
- '^(\d+\.)+': '1.', '1.2.', '1.2.3'
- '^(\d+\.)+': '1.', '1.2.', '1.2.3'
- '^\d+[\.\d+]*': '1.1', '1.2.1'
- '^第[零一二三四五六七八九十]+(章|节|小节|讲|部分)': '第一章', '第十二章', '第六节', '第七小节', '第二讲', '第八部分'
- '^[\(\[\{]?[a-zA-Z0-9]+[\)\]\}]': '(1)', '[a]', '{A}', '1]', 'A)', 'a}', '(a1)', '(Aa)'

"""
})

g_help_text = t({
    "en": r"""
The path to the configuration file used to generate the serial number, the default value is stored in ". /config/serial_number_generate_config.json", you can enter the path to the configuration file to customize the title number generation rules.
The configuration file is a JSON file with the following structure:
[
    {
        "prefix": "",               # Prefix for title numbering
        "suffix": "",               # Suffix for title numbering
        "remove_last_suffix": true, # Whether or not to remove the last suffix
        "independent": true,        # Whether to inherit the parent node's sequence number as a prefix
                                    # If the parent node's title number is "1." and the current title number is "2."
                                    # TRUE: numbering will be set to "1.2.".
                                    # FALSE: Numbering will be set to "2.".
                                    # In addition, if the current heading is not followed by a sub-heading and "remove_last_suffix" is set to true, the numbering will be set to "1.2" and "2" accordingly.
        "serial_number_type": "chinese_lower_case",
                                    # The type of serial number, the following values are supported:
                                    # - "number": "0", "1", "2", "3". Range: Unlimited
                                    # - "roman_lower_case": "i", "ii", "iii". Range: 1 to 3999
                                    # - "roman_upper_case": "I", "II", "III". Range: 1 to 3999
                                    # - "alphabet_lower_case": "a", "b", "c". Range: 1 to 26
                                    # - "alphabet_upper_case": "A", "B", "C". Range: 1 to 26
                                    # - "chinese_lower_case": "〇", "一", "二", "三". Range: 0 to 9999
                                    # - "chinese_upper_case": "零", "壹", "贰", "叁". Range: 0 to 9999
        "start_index": 1            # Starting index of the sequence number, Roman numerals and alphanumerics are not supported 0
    },
    ...
]

""",
    "zh": r"""
用于生成标题编号的配置文件路径，默认值存储在"./config/serial_number_generate_config.json"中，您可以输入配置文件的路径以自定义标题序号生成规则。
配置文件是一个 JSON 文件，其结构如下：
[
    {
        "prefix"： "",               # 标题编号的前缀
        "suffix"： "",               # 标题编号的后缀
        "remove_last_suffix": true, # 是否删除最后一个后缀
        "independent": true,        # 是否继承父节点的序列号作为前缀
                                    # 如果父节点的标题编号为 "1."，当前标题编号为 "2."时
                                    # TRUE：编号将设置为 "1.2."。
                                    # FALSE：编号将设置为 "2."。
                                    # 此外，如果当前标题后面没有子标题，且 remove_last_suffix 设置为 true，则编号将相应地设置为 "1.2" 和 "2"。
        "serial_number_type": "chinese_lower_case",
                                    # 序列号类型，支持以下值：
                                    # - "number"： "0", "1", "2", "3". 范围： 无限制
                                    # - "roman_lower_case"： "i", "ii", "iii"。范围： 无限制 1 至 3999
                                    # - "roman_upper_case"： "I", "II", "III"。范围： 1 至 3999 1 至 3999
                                    # - "alphabet_lower_case"： a", "b", "c"。范围： 1 至 26 1 至 26
                                    # - "alphabet_upper_case"： A", "B", "C"。范围： 1 至 26 1 至 26
                                    # - "chinese_lower_case"： "〇", "一", "二", "三"。范围： 0 至 9999
                                    # - "chinese_upper_case"： "零", "一", "贰", "叁"。范围： 0 至 9999
        "start_index"：1             # 序列号的起始索引，罗马数字和字母数字不支持 0
    },
    ...
]

"""
})

d_help_text = t({
    "en": r"""
Path to the root of the Docsify project, the default value is "./docs".

""",
    "zh": r"""
Docsify 项目根目录路径，默认值为 "./docs"。

""",
})

p_help_text = t({
    "en": r"""
The relative or absolute path to the Docsify project home page, defaulting to ". /README.md".
Note: If it is a relative path, then the path is relative to the Docsify root directory, so the default homepage will be resolved to ". /docs/README.md".

""",
    "zh": r"""
Docsify 项目主页的相对或绝对路径，默认为"./README.md"。
注意：如果是相对路径，那么该路径是 Docsify 根目录的相对路径，因此默认主页将被解析为"./docs/README.md"。

""",
})

o_help_text = t({
    "en": r"""
The output path of the merged Markdown file, the default value is "./merged.md".

""",
    "zh": r"""
合并后的 Markdown 文件的输出路径，默认值为 "./merged.md"。

""",
})

hu_help_text = t({
    "en": r"""
If the title is less than or equal to level six and beyond the scope of title generation rules, then this strategy will be executed.
The default value is "title", and the following values are supported:
- "title": Keeps only the title without any additional processing, for example, "title"
- "normal": Retains the hierarchy and title without any additional processing, for example, "## title"
- "cite": Keeps only the title and converts it into a quotation format, for example, "\n> title\n"

""",
    "zh": r"""
如果标题小于或等于六级，且超出标题生成规则的范围，则将执行此策略。
默认值为 "normal"，支持以下值：
- "title": 只保留标题，不做任何额外处理，例如 "title"。
- "normal": 保留层次结构和标题，不做任何额外处理，例如，"## title"
- "cite": 仅保留标题并将其转换为引文格式，例如："\n> title\n"

"""
})

hg_help_text = t({
    "en": r"""
If the title is greater than level six, then this strategy will be executed.
Even if the title is within the scope of title generation rules, this strategy will be executed.
The default value is "title", and the following values are supported:
- "title": Keeps only the title without any additional processing, for example, "title"
- "normal": Retains the hierarchy and title without any additional processing, for example, "## title"
- "cite": Keeps only the title and converts it into a quotation format, for example, "\n> title\n"

""",
    "zh": r"""
如果标题大于六级，则将执行该策略。
即使标题在标题生成规则的范围内，也会执行此策略。
默认值为 "cite"，支持以下值：
- "title": 只保留标题，不做任何额外处理，例如 "title"。
- "normal": 保留层次结构和标题，不做任何额外处理，例如，"## title"
- "cite": 仅保留标题并将其转换为引文格式，例如："\n> title\n"

"""
})

parser = argparse.ArgumentParser(description=t(description_text), formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-v', '--version', action='version', version='%(prog)s v1.0.0')
parser.add_argument('-r', '--serial_number_remove_config_file', type=str, help=r_help_text)
parser.add_argument('-g', '--serial_number_generate_config_file', type=str, help=g_help_text)
parser.add_argument('-p', '--homepage', type=str, help=p_help_text)
parser.add_argument('-d', '--docsify_path', type=str, help=d_help_text)
parser.add_argument('-o', '--output_file_path', type=str, help=o_help_text)
parser.add_argument('-hu', '--handel_unserial_number_title_strategy', type=str, help=hu_help_text)
parser.add_argument('-hg', '--handle_title_greater_than_level_six_strategy', type=str, help=hg_help_text)

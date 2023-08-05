# -*- coding: utf-8 -*-
# Time    : 2023-08-03 21:48
# Author  : Jiang Liu
# Desc    : 字典，用于实现多语言的支持
import src.log as log

CURRENT_LANGUAGE = 'zh'


def set_language(lang):
    """
    该函数用于设置当前的语言，该变化全局可见
    :param lang:   语言的缩写
    """
    logger = log.get_logger()
    if lang not in translations:
        logger.error(translate('Language not supported:') + lang)
        raise ValueError('Language not supported: ' + lang)
    global CURRENT_LANGUAGE
    CURRENT_LANGUAGE = lang
    logger.info(translate('Language set to:') + lang)


def translate(text, lang=CURRENT_LANGUAGE):
    # 如果text是字符串，则直接返回翻译后的字符串
    if isinstance(text, str):
        if lang == 'en':
            return text
        return translations.get(lang, {}).get(text.strip(), text)
    # 如果text是一个字典，则根据lang的值返回对应的值（针对超长文本的翻译）
    elif isinstance(text, dict):
        # 如果lang的值不在字典中，则返回第一个值
        if lang not in text:
            return text[list(text.keys())[0]]
        return text[lang]


translations = {
    'zh': {
        'Regex': '正则',
        'is invalid': '是不合法的',
        'Config': '配置',
        'Output path': '输出路径',
        'Docsify path': 'Docsify路径',
        'does not exist': '不存在',
        'Homepage': '主页',
        'Title strategy': '标题策略',
        'Language set to:': '语言设置为:',
        'Language not supported:': '不支持的语言:',
        'Load serial number remove config file:': '加载序号移除配置文件:',
        'Load serial number generate config file:': '加载序号生成配置文件:',
        'Set Output file path:': '设置输出文件路径:',
        'Set Docsify path:': '设置Docsify路径:',
        'Set Homepage:': '设置主页:',
        'Set Title strategy:': '设置标题策略:',
        'The path of Docsify is not exists.': 'Docsify路径不存在',
        'The sidebar file is not exists': '侧边栏文件不存在',
        'Load markdown file:': '加载Markdown文件:',
        'Handling links:': '处理链接:',
        'Remove the title sequence number:': '移除标题序号:',
        'Renumbered titles:': '重新编号的标题:',
        'Renumbered titles(Title Strategy):': '重新编号的标题(标题策略):',
        'Write to output file:': '写入输出文件:',

        'Processing Successful!': '处理成功！',
    },
}

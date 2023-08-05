# -*- coding: utf-8 -*-
# Time    : 2023-08-03 21:15
# Author  : Jiang Liu
# Desc    : 实现对 Docsify 的侧边栏文件涉及到的所有Markdown文件的合并

import os
import re

from src.i18n import translate as t
from src.log import get_logger
from src.sidebar_resolver import parse_sidebar


def merge(docsify_root_path, homepage):
    """
    该函数用于实现对 Docsify 的侧边栏文件涉及到的所有Markdown文件的合并。同时为该模块的主函数
    :param docsify_root_path:   Docsify的根目录
    :param homepage:            Docsify的主页文件，用于解析 _sidebar.md 文件时，如果遇到路径为 "/"或空 时，将其替换为主页文件
    :return:                    合并后的Markdown文件的行列表
    """
    logger = get_logger()
    # 首先检查该文件夹是否存在
    if not os.path.exists(docsify_root_path):
        logger.error(t("The path of Docsify is not exists."))
        print(t("The path of Docsify is not exists."))
        return
    # 然后检查该文件夹下是否存在侧边栏文件
    sidebar_path = os.path.join(docsify_root_path, '_sidebar.md')
    if not os.path.exists(sidebar_path):
        logger.error(t("The sidebar file is not exists") + f": {sidebar_path}")
        print(t("The sidebar file is not exists") + f": {sidebar_path}")
        return
    # 解析侧边栏文件
    with open(sidebar_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    root = parse_sidebar(lines, homepage)
    md = recursion_parse(docsify_root_path, root)
    return md.splitlines(keepends=True)


def recursion_parse(docsify_root_path, root):
    """
    递归解析侧边栏文件
    :param docsify_root_path:  Docsify的根目录
    :param root:               侧边栏文件的根节点
    :return:                   合并后的Markdown文件的行列表
    """
    logger = get_logger()
    md = ""
    # 如果有子节点，那么就是目录，需要添加标题
    if len(root.children) > 0:
        if root.level > 0:
            md += f"{'#' * root.level} {root.name}\n\n"
        for child in root.children:
            md += recursion_parse(docsify_root_path, child) + "\n"
    # 如果没有子节点，那么就是文件，需要添加文件内容
    else:
        # 但是也存在没有子节点，但又不是文件的情况
        if root.link is None:
            return f"{'#' * root.level} {root.name}\n"
        # 如果root.link是一个相对路径，那么就需要将其转换为绝对路径
        link = root.link
        if not os.path.isabs(link):
            link = os.path.join(docsify_root_path, link)
        logger.info(f'{t("Load markdown file:")} {link}')
        with open(link, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        lines = relative_heading_to_absolute_heading(lines, root.level)
        lines = remove_internal_link(lines)
        # 在最后添加一个空行，以免和下一个文件的内容连在一起
        md += "".join(lines) + "\n"
    return md


def relative_heading_to_absolute_heading(lines, level):
    """
    将相对标题转换为绝对标题
    :param lines:   Markdown文件的行列表
    :param level:   当前Markdown文件的处于的层级
    :return:        转换后的Markdown文件的行列表
    """
    result = []
    in_code_block = False
    for line in lines:
        # 跳过空行
        if line.strip() == '':
            result.append(line)
            continue
        # 计算该行前面有多少个空格
        previous_spaces = len(line) - len(line.lstrip())
        # 如果有4个及以上的空格，那么就是单行代码块
        if previous_spaces >= 4:
            result.append(line)
            continue
        # 如果有3个及以下的空格，那么就是普通行
        line = line.lstrip()
        # 如果是"```"，就是代码块的开始或结束
        if line.startswith('```'):
            in_code_block = not in_code_block
            result.append(line)
            continue
        if line.startswith('#') and not in_code_block:
            # 保留原格式，即保留原来的空格
            line = " " * previous_spaces + "#" * (level - 1) + line
        result.append(line)
    return result


def remove_internal_link(lines):
    """
    移除内部链接，只保留[]中的内容
    :param lines:   Markdown文件的行列表
    :return:        移除内部链接后的Markdown文件的行列表
    """
    logger = get_logger()

    def replacer(match):
        description = match.group('description')
        url = match.group('url')
        title = match.group('title')
        original_link = match.group(0)
        # 如果是外链，保留链接；否则，只保留描述
        if url and (url.startswith('http://') or url.startswith('https://')):
            new_link = f'[{description}]({url} "{title}")' if title else f'[{description}]({url})'
            logger.info(f'{t("Handling links:")} "{original_link}" -> "{new_link}"')
            return new_link
        else:
            new_link = description
            logger.info(f'{t("Handling links:")} "{original_link}" -> "{new_link}"')
            return description

    md = "".join(lines)
    # 移除内部链接，只保留[]中的内容
    # regex101: https://regex101.com/r/9xw49K/5
    regex = r"\[(?P<description>(?:\\[\[\]]|[^\[\]])*)\]\(\s*(?P<url>[^\s\)]+)?(?:\s+[\"\'](?P<title>.*?)[\"\'])?\s*\)"
    result = re.sub(regex, replacer, md, flags=re.DOTALL)
    return result.splitlines(keepends=True)

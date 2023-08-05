# -*- coding: utf-8 -*-
# Time    : 2023-08-03 22:56
# Author  : Jiang Liu
# Desc    : 解析 Docsify 的侧边栏文件 为 SidebarTreeNode 对象（树形结构）
import re


class SidebarTreeNode:
    """
    该类用于表示侧边栏文件的树形结构
    """

    def __init__(self, name=None, link=None, children=None, level=0):
        """
        该函数用于初始化侧边栏文件的树形结构
        :param name:        节点的名称
        :param link:        节点的链接
        :param children:    节点的子节点
        :param level:       节点的级别
        """
        if children is None:
            children = []
        self.name = name
        self.link = link
        self.children = children
        self.level = level

    def __str__(self):
        """
        递归地将该节点及其子节点转换为字符串
        :return:    节点的字符串表示
        """
        result = ''
        if self.name is not None:
            result += f"{'-' * self.level * 2}" + " {" + f'name: {self.name}, link: {self.link}' + "}\n"
        for child in self.children:
            result += child.__str__()
        return result


def parse_sidebar(lines, homepage):
    """
    该函数用于解析侧边栏文件
    :param lines:       侧边栏文件的行列表
    :param homepage:    Docsify的主页文件，用于解析 _sidebar.md 文件时，如果遇到路径为 "/"或空 时，将其替换为主页文件
    :return:            侧边栏文件的树形结构
    """
    root = SidebarTreeNode()
    stack = [root]

    for line in lines:
        indentation, name, link, title, folder_name = parse_line(line)
        level = indentation // 4 + 1
        while len(stack) > level:
            stack.pop()
        node = SidebarTreeNode(name=name, link=link, children=[], level=level)
        if node.link == '/' or node.link == '' or node.link is None:
            node.link = homepage
        if folder_name is not None:
            node.name = folder_name
            node.link = None
        stack[-1].children.append(node)
        stack.append(node)
    return root


def parse_line(line):
    """
    该函数用于解析侧边栏文件的每一行，通常的格式为：[tabs * 2n]- [name](link "title")
    :param line:    侧边栏文件的每一行
    :return:        该行的缩进、名称、链接、标题
    """
    indentation = len(line) - len(line.lstrip())
    line = line.lstrip()
    name = None
    link = None
    title = None
    folder_name = None
    # regex101: https://regex101.com/r/Iyh4Z1/8
    regex = r"^[ ]*- (?:\[(?P<name>.*)\]\([ ]*(?P<link>\S+)?(?:[ ]+[\"\'](?P<title>.*)[\"\'])?[ ]*\)|(?P<foldername>.*))[ ]*$"
    pattern = re.compile(regex)
    match = pattern.match(line)

    if match:
        name = match.group('name')
        # 替换name中的转义字符：\\ -> \, \[ -> [, \] -> ]
        if name is not None:
            name = name.replace('\\\\', '\\').replace('\\[', '[').replace('\\]', ']')
        link = match.group('link')
        title = match.group('title')
        folder_name = match.group('foldername')
    return indentation, name, link, title, folder_name

# -*- coding: utf-8 -*-
# Time    : 2023-08-04 15:58
# Author  : Jiang Liu
# Desc    : 重新编号标题：删去原来的编号，重新编号
import re
from enum import Enum, unique
from typing import Callable, List

from src.log import get_logger
from src.i18n import translate as t


@unique
class SerialNumberType(Enum):
    """
    该枚举类型用于表示序号的类型，包括阿拉伯数字、罗马数字、字母（大小写）、中文（大小写）
    """
    NUMBER = 'number'
    ROMAN_LOWER_CASE = 'roman_lower_case'
    ROMAN_UPPER_CASE = 'roman_upper_case'
    ALPHABET_LOWER_CASE = 'alphabet_lower_case'
    ALPHABET_UPPER_CASE = 'alphabet_upper_case'
    CHINESE_LOWER_CASE = 'chinese_lower_case'
    CHINESE_UPPER_CASE = 'chinese_upper_case'


class SerialNumberConfig:
    def __init__(self, prefix='', suffix='.', remove_last_suffix=True,
                 independent=False, serial_number_type=SerialNumberType.NUMBER,
                 start_index=1):
        """
        该函数用于初始化序号配置
        :param prefix:              序号的前缀
        :param suffix:              序号的后缀
        :param remove_last_suffix:  是否删除最后一个序号的后缀
        :param independent:         序号是否独立，如果独立，则不包括父节点的序号
        :param serial_number_type:  序号的类型，包括阿拉伯数字、罗马数字、字母（大小写）、中文（大小写），为 SerialNumberType 的枚举类型
        :param start_index:         序号的起始索引
        """
        self.prefix = prefix
        self.suffix = suffix
        self.remove_last_suffix = remove_last_suffix
        self.independent = independent
        self.serial_number_type = serial_number_type
        self.start_index = start_index

    def to_dict(self):
        """
        该函数用于将序号配置转换为字典
        :return:   序号配置的字典
        """
        return {
            'prefix': self.prefix,
            'suffix': self.suffix,
            'remove_last_suffix': self.remove_last_suffix,
            'independent': self.independent,
            'serial_number_type': self.serial_number_type.value,
            'start_index': self.start_index
        }


class SerialNumberUtil:
    """
    该类用于处理序号
    """

    @staticmethod
    def get_serial_number(serial_number_type, index) -> str:
        """
        该函数用于将序号索引转换为序号，index从0开始，序号分三类：阿拉伯数字、罗马数字、字母
        :param serial_number_type:      序号的类型
        :param index:                   序号的索引
        :return:                        序号
        """
        # 如果serial_number_type是对象，则获取其值
        if isinstance(serial_number_type, Enum):
            serial_number_type = serial_number_type.value

        if serial_number_type == SerialNumberType.NUMBER.value:
            return str(index)
        elif serial_number_type == SerialNumberType.ROMAN_LOWER_CASE.value:
            return SerialNumberUtil.int_to_roman_upper_case(index).lower()
        elif serial_number_type == SerialNumberType.ROMAN_UPPER_CASE.value:
            return SerialNumberUtil.int_to_roman_upper_case(index).upper()
        elif serial_number_type == SerialNumberType.ALPHABET_LOWER_CASE.value:
            return SerialNumberUtil.int_to_alphabet_lower_case(index)
        elif serial_number_type == SerialNumberType.ALPHABET_UPPER_CASE.value:
            return SerialNumberUtil.int_to_alphabet_upper_case(index)
        elif serial_number_type == SerialNumberType.CHINESE_LOWER_CASE.value:
            return SerialNumberUtil.int_to_chinese_lower_case(index)
        elif serial_number_type == SerialNumberType.CHINESE_UPPER_CASE.value:
            return SerialNumberUtil.int_to_chinese_upper_case(index)
        else:
            raise ValueError(f'Invalid serial number type: {serial_number_type}')

    @staticmethod
    def int_to_roman(n: int, roman_numerals: list) -> str:
        """
        该函数用于将整数转换为罗马数字
        :param n:               整数
        :param roman_numerals:  罗马数字的列表，包括罗马数字和对应的整数
        :return:                罗马数字
        """
        if n < 1 or n > 3999:
            raise ValueError("Input must be between 1 and 3999")

        result = ""
        for roman, value in roman_numerals:
            while n >= value:
                result += roman
                n -= value

        return result

    @staticmethod
    def int_to_roman_lower_case(n: int) -> str:
        """
        该函数用于将整数转换为罗马数字
        :param n:   整数
        :return:    罗马数字
        """
        if n < 1 or n > 3999:
            raise ValueError("Input must be between 1 and 3999")

        roman_numerals = [
            ("m", 1000), ("cm", 900), ("d", 500), ("cd", 400), ("c", 100),
            ("xc", 90), ("l", 50), ("xl", 40), ("x", 10), ("ix", 9),
            ("v", 5), ("iv", 4), ("i", 1)
        ]

        return SerialNumberUtil.int_to_roman(n, roman_numerals)

    @staticmethod
    def int_to_roman_upper_case(n: int) -> str:
        """
        该函数用于将整数转换为罗马数字
        :param n:   整数
        :return:    罗马数字
        """
        if n < 1 or n > 3999:
            raise ValueError("Input must be between 1 and 3999")

        roman_numerals = [
            ("M", 1000), ("CM", 900), ("D", 500), ("CD", 400), ("C", 100),
            ("XC", 90), ("L", 50), ("XL", 40), ("X", 10), ("IX", 9),
            ("V", 5), ("IV", 4), ("I", 1)
        ]

        return SerialNumberUtil.int_to_roman(n, roman_numerals)

    @staticmethod
    def int_to_alphabet_lower_case(n: int) -> str:
        """
        该函数用于将整数转换为字母序号，a对应1，b对应2，以此类推
        :param n:   整数
        :return:    字母
        """
        if n < 1 or n > 26:
            raise ValueError("Input must be between 1 and 26")
        return chr(n + 96)

    @staticmethod
    def int_to_alphabet_upper_case(n: int) -> str:
        """
        该函数用于将整数转换为字母序号，A对应1，B对应2，以此类推
        :param n:   整数
        :return:    字母
        """
        if n < 1 or n > 26:
            raise ValueError("Input must be between 1 and 26")
        return chr(n + 64)

    @staticmethod
    def int_to_chinese(n: int, chinese_numerals, units) -> str:
        """
        该函数用于将整数转换为中文数字
        :param n:                   整数
        :param chinese_numerals:    中文数字（大写或小写）
        :param units:               单位（大写或小写）
        :return:                    中文数字（大写或小写）
        """
        if n < 0 or n > 9999:
            raise ValueError("Input must be between 1 and 9999")

        def convert_section(num: int) -> str:
            section = ""
            for i in range(len(str(num)) - 1, -1, -1):
                digit = int(num % 10)
                if digit != 0:
                    section = chinese_numerals[digit] + units[i] + section
                elif section and section[0] != chinese_numerals[0]:
                    section = chinese_numerals[0] + section
                num //= 10
            return section

        result = ""
        if n >= 1000:
            result += chinese_numerals[n // 1000] + units[3]
            n %= 1000
        if n >= 100:
            result += convert_section(n)
        else:
            result += convert_section(n).lstrip(chinese_numerals[0])
        return result.replace("一十", "十").replace("壹拾", "拾")

    @staticmethod
    def int_to_chinese_lower_case(n: int) -> str:
        """
        该函数用于将整数转换为中文序号，一对应1，二对应2，以此类推
        :param n:   整数
        :return:    中文小写序号
        """
        chinese_numerals = ["〇", "一", "二", "三", "四", "五", "六", "七", "八", "九"]
        units = ["", "十", "百", "千"]
        return SerialNumberUtil.int_to_chinese(n, chinese_numerals, units)

    @staticmethod
    def int_to_chinese_upper_case(n: int) -> str:
        """
        该函数用于将整数转换为中文序号，壹对应1，贰对应2，以此类推
        :param n:   整数
        :return:    中文大写序号
        """
        chinese_numerals = ["零", "壹", "贰", "叁", "肆", "伍", "陆", "柒", "捌", "玖"]
        units = ["", "拾", "佰", "仟"]
        return SerialNumberUtil.int_to_chinese(n, chinese_numerals, units)


class SerialTitleStrategy:
    @staticmethod
    def all_strategies() -> List[str]:
        """
        该函数用于获取所有标题策略
        :return:    所有标题策略
        """
        return ["normal", "cite", "title"]

    @staticmethod
    def get_strategy(strategy: str) -> Callable[[str, str], str]:
        """
        该函数用于获取标题策略函数
        :param strategy:    标题策略字符串
        :return:            标题策略函数
        """
        if strategy == "normal":
            return SerialTitleStrategy.normal
        elif strategy == "cite":
            return SerialTitleStrategy.cite
        elif strategy == "title":
            return SerialTitleStrategy.title
        else:
            raise ValueError(f"Unknown strategy: {strategy}")

    @staticmethod
    def normal(hashes: str, title: str) -> str:
        """
        该函数用于生成普通标题
        :param hashes:  标题前的井号
        :param title:   标题
        :return:        普通标题
        """
        new_title = f"{hashes} {title}"
        get_logger().info(f'{t("Renumbered titles(Title Strategy):")} {new_title}')
        return new_title

    @staticmethod
    def cite(hashes: str, title: str) -> str:
        """
        该函数用于生成引用标题，例如 "> 标题"，同时标题前的井号会被去除
        为了避免与上下文连成一块或污染上下文，该函数会在字符串前后添加换行符
        :param hashes:  标题前的井号
        :param title:   标题
        :return:        引用标题
        """
        new_title = f"\n> {title}\n"
        get_logger().info(f'{t("Renumbered titles(Title Strategy):")} {new_title}')
        return new_title

    @staticmethod
    def title(hashes: str, title: str) -> str:
        """
        只保留title
        :param hashes:  标题前的井号
        :param title:   标题
        :return:        标题
        """
        new_title = f"{title}\n"
        get_logger().info(f'{t("Renumbered titles(Title Strategy):")} {new_title}')
        return new_title


def remove_title_serial(lines: list, serial_number_regex_list: list = None) -> list:
    """
    该函数用于将Markdown文件中的标题编号去除
    :param serial_number_regex_list:    标题编号与标题的分隔符正则表达式列表
    :param lines:                       Markdown文件的行列表
    :return:                            去除标题编号后的Markdown文件的行列表
    """
    logger = get_logger()
    if serial_number_regex_list is None:
        serial_number_regex_list = [
            # 数字后跟一个点，例如 "1.", "1.1.", "1.1.1.", ...
            r'^(\d+\.)+',

            # 数字点数字，例如 "1.1", "1.1.1"
            r'^\d+[\.\d+]*',

            # 中文数字后跟“章”，例如 "第一章"
            r'^第[零一二三四五六七八九十]+(章|节|小节|讲|部分)',

            # 括号中的数字或字母，例如 "(1)", "[a]", "{A}", "1]", "A)", "a}", "(a1)", "(Aa)"
            r'^[\(\[\{]?[a-zA-Z0-9]+[\)\]\}]'
        ]
    result = []
    in_code_block = False
    for line in lines:
        # 计算该行前面有多少个空格
        previous_spaces = len(line) - len(line.lstrip())
        # 1. 跳过空行
        # 2. 如果有4个及以上的空格，那么就是单行代码块
        if previous_spaces >= 4 or line.strip() == '':
            result.append(line)
            continue

        line = line.lstrip()
        if line.startswith('```'):
            in_code_block = not in_code_block
            result.append(line)
            continue

        if line.startswith('#') and not in_code_block:
            match = re.match(r'^(?P<title_level>#+) (?P<title_name>.*)$', line)
            if match:
                title_level = match.group('title_level')
                title_name = match.group('title_name')
                title_name = title_name.strip()
                # 如果标题名中包含能被标题编号与标题分隔符正则表达式匹配的内容，那么就去除匹配到的内容
                # 如果有多个，就去除最长的那个
                max_length_match = ""
                for serial_number_regex in serial_number_regex_list:
                    match = re.match(serial_number_regex, title_name)
                    if match and len(match.group()) > len(max_length_match):
                        max_length_match = match.group()
                if max_length_match:
                    logger.info(f'{t("Remove the title sequence number:")} {max_length_match}')
                    title_name = title_name.split(max_length_match, 1)[-1].strip()
                line = f"{title_level} {title_name}\n"
        result.append(line)
    return result


def renumber_title(lines: list, serial_number_config_array: list,
                   handel_unserial_number_title: Callable[[str, str], str] = SerialTitleStrategy.normal,
                   handle_title_greater_than_level_six: Callable[[str, str], str] = SerialTitleStrategy.cite) -> list:
    """
    为标题重新编号
    :param lines:                                   Markdown文件的行列表
    :param serial_number_config_array:              标题编号的配置
    :param handel_unserial_number_title:            处理未编号的标题的函数，该函数接收两个参数，第一个参数是标题的级别，第二个参数是标题名称
    :param handle_title_greater_than_level_six:     处理大于六级的标题的函数（因为Markdown最多支持六级标题，第七级将当做普通文本）
                                                    该函数接收两个参数，第一个参数是标题的级别，第二个参数是标题名称
    :return:                                        重新编号后的Markdown文件的行列表
    """
    logger = get_logger()
    if serial_number_config_array is None:
        serial_number_config_array = [
            SerialNumberConfig(prefix='', suffix='.', remove_last_suffix=True, independent=True,
                               serial_number_type=SerialNumberType.NUMBER, start_index=1),
            SerialNumberConfig(prefix='', suffix='.', remove_last_suffix=True, independent=False,
                               serial_number_type=SerialNumberType.NUMBER, start_index=1),
            SerialNumberConfig(prefix='', suffix='.', remove_last_suffix=True, independent=False,
                               serial_number_type=SerialNumberType.NUMBER, start_index=1),
            SerialNumberConfig(prefix='(', suffix=')', remove_last_suffix=False, independent=True,
                               serial_number_type=SerialNumberType.ALPHABET_LOWER_CASE, start_index=1),
            SerialNumberConfig(prefix='', suffix=')', remove_last_suffix=False, independent=True,
                               serial_number_type=SerialNumberType.ROMAN_LOWER_CASE, start_index=1),
        ]
    counters = [0] * len(serial_number_config_array)  # 用于存储每个级别的计数器
    result = []
    in_code_block = False
    for line in lines:
        # 计算该行前面有多少个空格
        previous_spaces = len(line) - len(line.lstrip())
        # 1. 跳过空行
        # 2. 如果有4个及以上的空格，那么就是单行代码块
        if previous_spaces >= 4 or line.strip() == '':
            result.append(line)
            continue
        line = line.lstrip()

        if line.startswith('```'):
            in_code_block = not in_code_block
            result.append(line)
            continue

        match = re.match(r'^(#+) (.+)', line)
        if match and not in_code_block:
            hashes, title = match.groups()
            title = title.strip()
            level = len(hashes)

            # 如果标题的层级大于6，那么就执行handle_title_greater_than_level_six函数
            if level > 6:
                line = handle_title_greater_than_level_six(hashes, title)
                result.append(line)
                continue

            # 如果标题的层级大于配置的层级，那么就执行handel_unserial_number_title函数
            if level > len(serial_number_config_array):
                line = handel_unserial_number_title(hashes, title)
                result.append(line)
                continue

            counters[level - 1] += 1
            # 清空计数器
            for i in range(level, len(counters)):
                counters[i] = 0

            # 为标题添加编号
            serial_number = ''
            for i in range(level):
                serial_number_config = serial_number_config_array[i]
                if serial_number_config.independent:
                    serial_number = ''
                current_serial_number = SerialNumberUtil.get_serial_number(
                    serial_number_config.serial_number_type,
                    counters[i] + serial_number_config.start_index - 1
                )
                if i == level - 1 and serial_number_config.remove_last_suffix:
                    serial_number = f"{serial_number}{serial_number_config.prefix}{current_serial_number}"
                else:
                    serial_number = f"{serial_number}{serial_number_config.prefix}{current_serial_number}{serial_number_config.suffix}"

            new_line = f"{hashes} {serial_number} {title}\n"
            logger.info(f'{t("Renumbered titles:")} {new_line}')
            result.append(new_line)
        else:
            result.append(line)

    return result

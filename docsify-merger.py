import json
import os
import sys

from src.log import init_logging
from src.merger_markdown import merge
from src.renumber_title import remove_title_serial, renumber_title, SerialNumberType
from src.renumber_title import SerialNumberConfig, SerialTitleStrategy
import src.i18n as i18n


def get_os_path():
    if getattr(sys, 'frozen', False):
        # 脚本被打包成可执行文件
        return os.path.dirname(sys.executable)
    else:
        # 脚本在正常的 Python 解释器中运行
        return os.path.dirname(__file__)


def load_application_config():
    # 从 JSON 文件读取配置信息
    config = {}
    with open(os.path.join(get_os_path(), "./config/application_config.json"), 'r') as file:
        config = json.load(file)
    if config is None:
        config = {}

    # 从配置项读取日志配置文件路径，如果没有配置项，则使用默认值”./config/logging_config.ini“
    logging_config_file_path = config.get('logging_config_file_path')
    if logging_config_file_path is None:
        logging_config_file_path = "./config/logging_config.ini"
    # 如果是相对路径，则转换为绝对路径
    if not os.path.isabs(logging_config_file_path):
        logging_config_file_path = os.path.join(get_os_path(), logging_config_file_path)
    init_logging(logging_config_file_path)

    # 从配置项读取语言，如果没有配置项，则使用默认值”en“
    language = config.get('language')
    if language is None:
        language = 'en'
    i18n.set_language(language)


def main():
    load_application_config()
    docsify_path = os.path.join(get_os_path(), "./docs")
    homepage = os.path.join(docsify_path, "./README.md")
    serial_number_regex_list = [
        r'^(\d+\.)+',
        r'^\d+[\.\d+]*',
        r'^第[零一二三四五六七八九十]+(章|节|小节|讲|部分)',
        r'^[\(\[\{]?[a-zA-Z0-9]+[\)\]\}]'
    ]
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
    handel_unserial_number_title = SerialTitleStrategy.normal
    handle_title_greater_than_level_six = SerialTitleStrategy.cite
    output_file_path = os.path.join(get_os_path(), "./merged.md")

    lines = merge(docsify_root_path=docsify_path, homepage=homepage)
    lines = remove_title_serial(lines, serial_number_regex_list=serial_number_regex_list)
    lines = renumber_title(lines, serial_number_config_array=serial_number_config_array,
                           handel_unserial_number_title=handel_unserial_number_title,
                           handle_title_greater_than_level_six=handle_title_greater_than_level_six)
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)


if __name__ == '__main__':
    main()

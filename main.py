import json
import os
import re
import sys

from src.log import init_logging, get_logger
from src.merger_markdown import merge
from src.renumber_title import remove_title_serial, renumber_title
from src.renumber_title import SerialNumberConfig, SerialTitleStrategy
from src.arg import parser
import src.i18n as i18n
from src.i18n import translate as t


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


def parse_args():
    args = parser.parse_args()
    serial_number_regex_list = None
    serial_number_config_array = None
    serial_number_remove_config_file = args.serial_number_remove_config_file
    serial_number_generate_config_file = args.serial_number_generate_config_file
    docsify_path = args.docsify_path
    output_file_path = args.output_file_path
    homepage = args.homepage
    handel_unserial_number_title_strategy = args.handel_unserial_number_title_strategy
    handle_title_greater_than_level_six_strategy = args.handle_title_greater_than_level_six_strategy
    logger = get_logger()
    # 从json文件中读取配置
    if serial_number_remove_config_file is not None:
        # 如果是相对路径，则转换为绝对路径
        if not os.path.isabs(serial_number_remove_config_file):
            serial_number_remove_config_file = os.path.join(get_os_path(), serial_number_remove_config_file)
        logger.info(f"{t('Load serial number remove config file:')} '{serial_number_remove_config_file}'")
        with open(serial_number_remove_config_file, 'r', encoding='utf-8') as file:
            serial_number_remove_regex_list = json.load(file)
            # 检查每一个正则是否合法
            if serial_number_remove_regex_list is not None:
                serial_number_regex_list = []
                for regex in serial_number_remove_regex_list:
                    try:
                        re.compile(regex)
                        serial_number_regex_list.append(regex)
                    except Exception as e:
                        logger.error(f"{t('Regex')} '{regex}' {t('is invalid')}")
                        print(f"{t('Regex')} '{regex}' {t('is invalid')}")
                        sys.exit(1)

    # 检查配置文件是否合法
    if serial_number_generate_config_file is not None:
        # 如果是相对路径，则转换为绝对路径
        if not os.path.isabs(serial_number_generate_config_file):
            serial_number_generate_config_file = os.path.join(get_os_path(), serial_number_generate_config_file)
        logger.info(f"{t('Load serial number generate config file:')} '{serial_number_generate_config_file}'")
        with open(serial_number_generate_config_file, 'r', encoding='utf-8') as file:
            config = json.load(file)
            if config is not None:
                serial_number_config_array = []
                for item in config:
                    try:
                        serial_number_config_array.append(SerialNumberConfig(**item))
                    except Exception as e:
                        logger.error(f"{t('Config')} '{item}' {t('is invalid')}")
                        print(f"{t('Config')} '{item}' {t('is invalid')}")
                        sys.exit(1)

    # 检查输出文件路径是否合法
    if output_file_path is None:
        output_file_path = os.path.join(get_os_path(), r'./merged.md')
    # 如果是相对路径，则转换为绝对路径
    if not os.path.isabs(output_file_path):
        output_file_path = os.path.join(get_os_path(), output_file_path)
    # 如果没有文件夹，创建文件夹
    if not os.path.exists(os.path.dirname(output_file_path)):
        os.makedirs(os.path.dirname(output_file_path))
    try:
        with open(output_file_path, 'w', encoding='utf-8') as file:
            pass
    except Exception as e:
        logger.error(f"{t('Output path')} '{output_file_path}' {t('is invalid')}")
        print(f"{t('Output path')} '{output_file_path}' {t('is invalid')}")
        sys.exit(1)
    logger.info(f"{t('Set Output file path:')} '{output_file_path}'")

    # 检查输入文件夹是否合法
    if docsify_path is None:
        docsify_path = os.path.join(get_os_path(), r'./docs')
    # 如果是相对路径，则转换为绝对路径
    if not os.path.isabs(docsify_path):
        docsify_path = os.path.join(get_os_path(), docsify_path)
    if not os.path.exists(docsify_path):
        logger.error(f"{t('Docsify path')} '{docsify_path}' {t('does not exist')}")
        print(f"{t('Docsify path')} '{docsify_path}' {t('does not exist')}")
        sys.exit(1)
    logger.info(f"{t('Set Docsify path:')} '{docsify_path}'")

    # 检查首页是否存在
    if homepage is None:
        homepage = r'./README.md'
    # 如果是相对路径，则转换为绝对路径
    if not os.path.isabs(homepage):
        homepage = os.path.join(docsify_path, homepage)
    if not os.path.exists(homepage):
        logger.error(f"{t('Homepage')} '{homepage}' {t('does not exist')}")
        print(f"{t('Homepage')} '{homepage}' {t('does not exist')}")
        sys.exit(1)
    logger.info(f"{t('Set Homepage:')} '{homepage}'")

    # 检查标题处理策略是否合法
    def check_title_strategy(strategy):
        if strategy not in SerialTitleStrategy.all_strategies():
            logger.error(f"{t('Title strategy')} '{strategy}' {t('is invalid')}")
            print(f"{t('Title strategy')} '{strategy}' {t('is invalid')}")
            sys.exit(1)

    if handel_unserial_number_title_strategy is None:
        handel_unserial_number_title_strategy = 'normal'
    check_title_strategy(handel_unserial_number_title_strategy)
    handel_unserial_number_title = SerialTitleStrategy.get_strategy(handel_unserial_number_title_strategy)
    logger.info(f"{t('Set Title strategy:')} '{handel_unserial_number_title_strategy}'")

    if handle_title_greater_than_level_six_strategy is None:
        handle_title_greater_than_level_six_strategy = 'cite'
    check_title_strategy(handle_title_greater_than_level_six_strategy)
    handle_title_greater_than_level_six = SerialTitleStrategy.get_strategy(handle_title_greater_than_level_six_strategy)
    logger.info(f"{t('Set Title strategy:')} '{handle_title_greater_than_level_six_strategy}'")

    return serial_number_regex_list, serial_number_config_array, docsify_path, homepage, output_file_path, handel_unserial_number_title, handle_title_greater_than_level_six


def main():
    load_application_config()
    logger = get_logger()
    serial_number_regex_list, serial_number_config_array, docsify_path, homepage, \
        output_file_path, handel_unserial_number_title, handle_title_greater_than_level_six = parse_args()

    lines = merge(docsify_root_path=docsify_path, homepage=homepage)
    lines = remove_title_serial(lines, serial_number_regex_list=serial_number_regex_list)
    lines = renumber_title(lines, serial_number_config_array=serial_number_config_array,
                           handel_unserial_number_title=handel_unserial_number_title,
                           handle_title_greater_than_level_six=handle_title_greater_than_level_six)
    logger.info(f"{t('Write to output file:')} '{output_file_path}'")
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)
    logger.info(f"{t('Processing Successful!')}")


if __name__ == '__main__':
    main()

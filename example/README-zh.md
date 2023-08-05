# 1. 快速开始

你可以在控制台输入以下命令来运行 Docsify Merger

## 1.1 合并样例文档

```shell
./docsify-merger.exe -d ./docs -p ./README.md -r ./config/serial_number_remove_config.json -g ./config/serial_number_generate_config.json -o ./mergerd.md -hu normal -hg cite
```

样例文档给出了以下情况：

- 多级标题
- 超过六级的标题
- 代码中"#"开头的注释（不应该被当做标题处理）
- 内链处理

## 1.2 合并Docsify官方文档

```shell
./docsify-merger.exe -d ./docsify -p ./README.md -r ./config/serial_number_remove_config.json -g ./config/serial_number_generate_config.json -o ./mergerd.md -hu normal -hg cite
```

Docsify官方文档内容较为复杂，但依然可以被正确处理。

# 2. 自定义配置项

现在你可以自定义配置项了，所有默认值都在`./config`目录下。你可以参考项目首页README文档中的说明来理解并修改配置项。

你可以在`./config/application_config.json`中修改语言、日志文件配置文件路径

`./config/application_config.json`默认值：

```json
{
  "language": "zh",
  "logging_config_file_path": "./config/logging_config.ini"
}
```

再修改`./config/serial_number_remove_config.json`和`./config/serial_number_generate_config.json`来设置删除序列号的正则规则和生成标题序号的配置项。

`./config/serial_number_remove_config.json`默认值：

```json
[
  "^(\\d+\\.)+",
  "^\\d+[\\.\\d+]*",
  "^第[零一二三四五六七八九十]+(章|节|小节|讲|部分)",
  "^[\\(\\[\\{]?[a-zA-Z0-9]+[\\)\\]\\}]"
]
```

`./config/serial_number_generate_config.json`默认值：

```json
[
  {
    "prefix": "",
    "suffix": ".",
    "remove_last_suffix": false,
    "independent": true,
    "serial_number_type": "number",
    "start_index": 1
  },
  {
    "prefix": "",
    "suffix": ".",
    "remove_last_suffix": true,
    "independent": false,
    "serial_number_type": "number",
    "start_index": 1
  },
  {
    "prefix": "",
    "suffix": ".",
    "remove_last_suffix": true,
    "independent": false,
    "serial_number_type": "number",
    "start_index": 1
  },
  {
    "prefix": "",
    "suffix": ".",
    "remove_last_suffix": true,
    "independent": false,
    "serial_number_type": "number",
    "start_index": 1
  },
  {
    "prefix": "(",
    "suffix": ")",
    "remove_last_suffix": false,
    "independent": true,
    "serial_number_type": "alphabet_lower_case",
    "start_index": 1
  },
  {
    "prefix": "",
    "suffix": ")",
    "remove_last_suffix": false,
    "independent": true,
    "serial_number_type": "roman_lower_case",
    "start_index": 1
  }
]
```
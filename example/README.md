# 1. Quick Start

You can run Docsify Merger in the console with the following command

## 1.1 Merging Sample Documents

```shell
./docsify-merger.exe -d ./docs -p ./README.md -r ./config/serial_number_remove_config.json -g ./config/serial_number_generate_config.json -o ./mergerd.md -hu normal -hg cite
```

The sample documents provide the following scenarios:

- Multi-level headers
- Headers beyond level six
- Comments starting with "#" in the code (should not be treated as headers)
- Internal link handling

## 1.2 Merging Docsify Official Documents

```shell
./docsify-merger.exe -d ./docsify -p ./README.md -r ./config/serial_number_remove_config.json -g ./config/serial_number_generate_config.json -o ./mergerd.md -hu normal -hg cite
```

The content of Docsify's official documents is more complex, but can still be correctly processed.

# 2. Custom Configuration Items

Now you can customize the configuration items, all default values are in the `./config` directory. You can refer to the instructions in the README document on the project homepage to understand and modify the configuration items.

You can modify the language and log file configuration file path in `./config/application_config.json`

The default value of `./config/application_config.json`:

```json
{
  "language": "zh",
  "logging_config_file_path": "./config/logging_config.ini"
}
```

Then modify `./config/serial_number_remove_config.json` and `./config/serial_number_generate_config.json` to set the regex rules for removing serial numbers and the configuration items for generating title numbers.

The default value of `./config/serial_number_remove_config.json`:

```json
[
  "^(\\d+\\.)+",
  "^\\d+[\\.\\d+]*",
  "^第[零一二三四五六七八九十]+(章|节|小节|讲|部分)",
  "^[\\(\\[\\{]?[a-zA-Z0-9]+[\\)\\]\\}]"
]
```

The default value of `./config/serial_number_generate_config.json`:

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
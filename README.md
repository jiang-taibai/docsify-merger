# <div align="center">Docsify Merger</div>

<div align="center">
  <img src="https://img.shields.io/badge/Build-passing-%2396C40F" alt="Build-passing"/>
  <img src="https://img.shields.io/badge/Version-1.0.0-%231081C1" alt="Version-1.0.0"/>
  <img src="https://img.shields.io/badge/License-Apache_2.0-%2396C40F" alt="License-Apache 2.0-%2396C40F"/>
  <img src="https://img.shields.io/badge/PoweredBy-Jiang_Liu-%2396C40F" alt="PoweredBy-Jiang_Liu"/>
</div>

<div align="center">
    <a href="#">English</a> | <a href="README-zh.md">中文</a>
</div>

## 1. Introduction

Docsify Merger is a tool that merges multiple Markdown documents into a single document.
It can recombine them into a single Markdown document based on the document structure defined in the "_sidebar.md" file.

This tool has the following features:

- Maintain the original hierarchical relationship: Merge multiple Markdown documents according to the hierarchical relationship in the "_sidebar.md" file
- Unified title numbering: Remove the original title numbering and renumber the titles
- Remove internal links: Links to other titles in the document will be removed to avoid non-existent link paths in the exported Markdown document
- Highly customizable: Customize the regular expression for deleting titles, customize the title generation rules
- Higher fault tolerance: Provide optional strategies for unprocessed titles and titles greater than six levels

You can then convert the exported Markdown document into formats such as PDF, Word, HTML, PNG, etc.
You can use [Pandoc](https://pandoc.org/) or [Typora](https://typora.io/) to complete this step.

The following image shows the result of exporting the [Docsify official documentation](https://docsify.js.org):

<div align="center">

  <div>Original Document</div>
  <div>Left: Document Preview; Middle: docs directory structure; Right: _sidebar.md content</div>

![](./img/docsify-official-original-document.png)

</div>

<div align="center">

  <div>Merged Documentation</div>

![](./img/docsify-official-merged-document.png)

</div>

## 2. Usage

### 2.1 Python

If Python is already installed on your computer, you can directly run Docsify Merger using Python.

Enter the following command in the command line to run Docsify Merger:

```shell
python docsify-merger.py
```

Additionally, you can open the `docsify-merger.py` file and modify the values of various parameters within the `main` function.

### 2.2 Executable File

If Python is not installed on your computer, you can run Docsify Merger using the executable file.

Download the `docsify-merger.zip` file, unzip it, and execute `docsify-merger.exe`.

However, in general, you may need to modify some configurations. Below are all the parameters and recommended values:

- Path to the Docsify project root directory: `-d ./doc`
- Path to the Docsify homepage: `-p ./README.md`
- Path to the title serial number removal rule configuration file: `-r ./config/serial_number_remove_config.json`
- Path to the title serial number generation rule configuration file: `-g ./config/serial_number_generate_config.json`
- Path to the output file: `-o ./mergerd.md`
- Strategy for unprocessed titles: `-hu normal`
- Strategy for titles greater than level six: `-hg cite`

You can execute the following command to view the description of all parameters:

```shell
docsify-merger.exe -h
```

If the directory structure is as follows:

```
.
├── docsify-merger.exe
├── config
│   ├── application_config.json
│   ├── logging_config.ini
│   ├── serial_number_generate_config.json
│   └── serial_number_remove_config.json
└── docs
    ├── README.md
    ├── _sidebar.md
    └── md
        ├── overview.md
        └── programming-language
            ├── cpp.md
            └── python.md
```

The content of the `_sidebar.md` file is as follows:

```markdown
- [Guide]()
- [Overview](md/overview.md)
- Programming Language
    - [CPP](md/programming-language/cpp.md)
    - [Python](md/programming-language/python.md)
```

You can enter the following command in the console to run Docsify Merger

```shell
./docsify-merger.exe -d ./docs -p ./README.md -r ./config/serial_number_remove_config.json -g ./config/serial_number_generate_config.json -o ./mergerd.md -hu normal -hg cite
```

## 3. Configuration Explanation

For the .exe file, you can find the configuration files in the `config` folder. If you are running `docsify-merger.py` with Python, you can directly modify the values of various parameters in the `main` function.

### 3.1 Handling Path Parameters

For path parameters, you can use either relative or absolute paths. If you use a relative path, the starting point of the relative path is the directory where the `docsify-merger.exe` file is located.

Specifically, the path to the Docsify homepage is relative to the Docsify project root directory. For example, if the parameters are `-d ./doc -p ./README.md`, then the path to the Docsify homepage would be `./doc/README.md`.

### 3.2 Configuration File for Removing Title Numbers

This configuration file is a JSON file containing an array. Each element in the array is a regular expression used to match title numbers. If a title number matches one of these regular expressions, it will be removed.

Additionally, if a title number matches multiple regular expressions, the longest matched number will be removed. For example, with the two regular expressions `^\d+.` and `^(\d+.)+`, if the title number is `1.1.`, then the first will match `1.`, and the second will match `1.1.`. Since the second title number is longer, `1.1.` will be removed.

Below is the default value for this configuration parameter:

```json
[
  "^(\\d+\\.)+",
  "^\\d+[\\.\\d+]*",
  "^第[零一二三四五六七八九十]+(章|节|小节|讲|部分)",
  "^[\\(\\[\\{]?[a-zA-Z0-9]+[\\)\\]\\}]"
]
```

### 3.3 Configuration File for Title Number Generation Rules

This configuration file is a JSON file containing an array. Each element in the array is a configuration item for a title generation rule. The first element corresponds to the first-level title, the second element corresponds to the second-level title, and so on.

Each title generation rule configuration item includes the following parameters:

- `prefix`: Prefix for the title
- `suffix`: Suffix for the title
- `remove_last_suffix`: Whether to remove the suffix if the title number ends at this level
- `independent`: Whether to number independently; if `true`, the title number will not include the previous level's number
- `serial_number_type`: Numbering type, selectable values include [`"number"`, `"roman_lower_case"`, `"roman_upper_case"`,
  `"alphabet_lower_case"`, `"alphabet_upper_case"`, `"chinese_lower_case"`, `"chinese_upper_case"`]
- `start_index`: Starting value for numbering

Below is the default value for this configuration parameter: (please provide the corresponding default values if needed)

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

### 3.4 Handling Strategy for Unprocessed and Titles Greater Than Level Six

The available options for title handling strategy are as follows (assuming the level of the title to be processed is `##`, and the title is `secondary title`):

- `normal`: Keep both the level and the title, such as `## Secondary Title`
- `title`: Keep only the title, such as `Secondary Title`
- `cite`: Keep only the title, and set it in quotation format, such as `\n> Secondary Title\n`. The line breaks here are to avoid contamination of the surrounding context

### 3.5 Application Configuration

The application will read the application configuration from `./config/application_config.json`. Please do not delete or move this file.

This configuration file contains the following parameters:

- `language`: Language, selectable values are [`"en"`, `"zh"`]
- `logging_config_file_path`: Path to the logging configuration file; if it's a relative path, the logging configuration file will be read relative to the directory where the `docsify-merger.exe` file is located

```json
{
  "language": "zh",
  "logging_config_file_path": "./config/logging_config.ini"
}
```

## 4. Future Plans

- [ ] Add more optional title generation rules
- [ ] Add more optional title handling strategies
- [ ] Support online Markdown documents
- [ ] GUI interface

## 5. License

The project is licensed under the [Apache License 2.0](https://apache.org/licenses/LICENSE-2.0.txt)

Copyright © 2023 Jiang Liu.

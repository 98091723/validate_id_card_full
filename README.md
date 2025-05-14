# validate_id_card_full
# 身份证号校验工具

本项目为一个基于 Python 的中国身份证号码校验工具，支持图形化界面（Tkinter），可对18位身份证号码进行合法性校验，包括区划代码、出生日期和校验码等。

## 功能特性

- 校验身份证号长度、格式、出生日期是否合法
- 校验前6位区划代码是否在提供的区划代码文件（`areas.csv`）中
- 校验身份证校验位（第18位）
- 图形化界面，简洁易用

## 使用方法

### 1. 准备区划代码文件

请确保项目目录下有 `areas.csv` 文件，内容格式如下（可参考样例或使用全国数据）：

```
code,name,cityCode,provinceCode
110101,"东城区",1101,11
110102,"西城区",1101,11
...
```

### 2. 运行程序

首先确保你已安装 Python 3 环境。

直接运行主程序：

```bash
python id_validator_gui.py
```

会弹出图形化窗口，输入18位身份证号后点击“校验”按钮，即可显示校验结果。

### 3. 数据来源

- 区划代码数据可参考[国家统计局官网](https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/)或[modood/Administrative-divisions-of-China](https://github.com/modood/Administrative-divisions-of-China)等开源项目获取。
- 建议定期更新区划代码以保证准确性。

## 依赖

- Python 3.x
- Tkinter（Python 标准库自带）
- `areas.csv` 区划代码数据文件

## 代码结构

- `id_validator_gui.py` 主程序，带有Tkinter界面
- `areas.csv` 行政区划代码数据文件

## 常见问题

- **区划代码不合法/文件找不到**：请确认 `areas.csv` 文件存在于项目根目录，格式正确且为 UTF-8 编码。
- **校验码错误**：请确认身份证号真实有效，或手动检查出生日期、前17位数字是否正确。

## License

MIT License

---

如有建议或需求，欢迎提 issue 或 PR！

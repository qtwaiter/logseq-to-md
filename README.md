# Logseq to Markdown Converter

专门用于将 Logseq 的日记文件和笔记转换为标准 Markdown 格式的工具。

## 功能特点

- **简单实用** - 专注于转换功能,不做复杂的事情
- **保留内容** - 完整保留所有文本、图片、链接
- **移除语法** - 清除 Logseq 特有的块符号和属性
- **标准输出** - 生成符合标准 Markdown 规范的文件

## 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/logseq-to-md.git
cd logseq-to-md
```

## 使用方法

### 方式 1: Python 脚本

```python
from converter import LogseqToMarkdownConverter

converter = LogseqToMarkdownConverter()

# 转换单个文件
converter.convert_file(
    input_path="2025_01_07.md",
    output_path="output/2025_01_07_standard.md"
)

# 转换内容字符串
content = "- 标题\n  - 内容"
converted = converter.convert_content(content)
print(converted)
```

### 方式 2: 命令行

```bash
python converter.py input.md output.md
```

## 转换示例

### Logseq 原始格式
```markdown
- 工作日报
	- 今日日程
		- 菜篮子配送
		  collapsed:: true
		- 食堂会议
	- 工作成果
		- 完成了数据转换
```

### 转换后的标准 Markdown
```markdown
# 工作日报

## 今日日程

### 菜篮子配送

### 食堂会议

## 工作成果

### 完成了数据转换
```

## 支持的转换

| Logseq 特性 | 转换结果 |
|-----------|---------|
| Block 前缀 (`-`) | 移除,转为标题层级 |
| 缩进嵌套 | 转换为 Markdown 标题 |
| `collapsed:: true` | 完全移除 |
| `key:: value` 属性 | 移除 |
| `[[链接]]` | 保留 |
| `#标签` | 保留 |
| `![](图片)` | 保留 |
| `{{query}}` | 保留原样 |

## 技术细节

- **语言**: Python 3
- **依赖**: 仅使用标准库
- **兼容**: Windows, macOS, Linux
- **编码**: UTF-8

## 许可证

MIT License

## 作者

夏威特 (qtwaiter)

## 反馈

如有问题或建议,欢迎提 Issue!

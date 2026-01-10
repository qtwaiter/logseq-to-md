"""
Logseq to Markdown Converter
将 Logseq 的 Markdown 格式转换为标准 Markdown 格式
"""

import re
import os
from pathlib import Path
from typing import List, Tuple


class LogseqToMarkdownConverter:
    """Logseq 到 Markdown 转换器"""

    def __init__(self):
        # 块前缀模式: 以 `-` 开头的行
        self.block_pattern = re.compile(r'^(\s*)-\s+(.*)$')
        # 属性模式: key:: value
        self.property_pattern = re.compile(r'(\w+)::\s*(.+?)(?:\s+|$)')
        # 折叠状态
        self.collapsed_pattern = re.compile(r'collapsed::\s*(true|false)')
        # 图片和链接
        self.image_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
        self.link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
        # 标签
        self.tag_pattern = re.compile(r'#(\w+(?:\/\w+)*)')

    def convert_file(self, input_path: str, output_path: str = None) -> str:
        """
        转换 Logseq 文件为标准 Markdown

        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径(可选)

        Returns:
            转换后的 Markdown 内容
        """
        # 读取文件
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 转换内容
        converted = self.convert_content(content)

        # 保存文件
        if output_path:
            self._save_file(converted, output_path)

        return converted

    def convert_content(self, content: str) -> str:
        """
        转换 Logseq 内容为标准 Markdown

        Args:
            content: Logseq 格式的 Markdown 内容

        Returns:
            标准格式的 Markdown 内容
        """
        lines = content.split('\n')
        result = []
        header_level = 0

        for line in lines:
            # 跳过空行
            if not line.strip():
                result.append('')
                continue

            # 计算缩进级别
            indent = len(line) - len(line.lstrip())
            level = indent // 2  # Logseq 使用2个空格缩进

            # 检查是否是块
            block_match = self.block_pattern.match(line)

            if block_match:
                # 提取块内容
                block_content = block_match.group(2).strip()

                # 跳过折叠状态属性
                if self.collapsed_pattern.search(block_content):
                    continue

                # 移除块属性(但在注释中保留)
                clean_content = self._remove_properties(block_content)

                # 转换为标题
                if clean_content:
                    # 根据层级确定标题级别
                    md_level = min(level + 1, 6)  # Markdown 最多6级标题
                    prefix = '#' * md_level

                    # 添加标题
                    result.append(f"{prefix} {clean_content}")
                    result.append('')  # 标题后空行
                else:
                    result.append('')

            else:
                # 非块内容,直接添加
                result.append(line.lstrip())

        return '\n'.join(result)

    def _remove_properties(self, content: str) -> str:
        """
        移除块属性,但保留主要内容

        Args:
            content: 块内容

        Returns:
            移除属性后的内容
        """
        # 移除常见的块属性
        properties_to_remove = [
            r'collapsed::\s*\w+',
            r'id::\s*[a-f0-9-]+',
        ]

        for prop in properties_to_remove:
            content = re.sub(prop, '', content)

        # 清理多余的空格
        content = re.sub(r'\s+', ' ', content)
        return content.strip()

    def extract_by_tag(self, content: str, tag: str) -> str:
        """
        提取包含特定标签的内容

        Args:
            content: Logseq 内容
            tag: 标签名(不含#)

        Returns:
            包含该标签的 Markdown 内容
        """
        lines = content.split('\n')
        result = []
        found = False

        for line in lines:
            # 检查是否包含标签
            if f'#{tag}' in line:
                found = True

            if found:
                # 移除块前缀
                block_match = self.block_pattern.match(line)
                if block_match:
                    result.append(block_match.group(2))
                else:
                    result.append(line)

        return '\n'.join(result)

    def _save_file(self, content: str, output_path: str):
        """
        保存转换后的内容到文件

        Args:
            content: 转换后的内容
            output_path: 输出文件路径
        """
        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 保存文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)


def main():
    """测试函数"""
    converter = LogseqToMarkdownConverter()

    # 测试内容
    test_content = """- ### 工作日报
	- 今日日程
		- 菜篮子配送
		  collapsed:: true
			- 订单详情
		- 食堂会议
	- 工作成果
		- 完成了数据转换
		- 提写了报告
"""

    # 转换内容
    converted = converter.convert_content(test_content)

    print("转换结果:")
    print("=" * 50)
    print(converted)
    print("=" * 50)

    # 保存测试文件
    output_path = "test_output.md"
    converter._save_file(converted, output_path)
    print(f"\n已保存到: {output_path}")


if __name__ == "__main__":
    main()

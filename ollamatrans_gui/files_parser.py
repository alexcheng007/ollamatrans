"""
Ollama Translator 文件解析模块
作者: alex cheng <xcheng@vidts.com>
版本: 0.1.0
生成日期: 2025-3-10

模块功能：
- 支持PDF、EPUB、FB2等格式的解析
- 提供流式解析和完整内容提取功能
"""
import xml.etree.ElementTree as ET

from ebooklib import epub
import fitz  # PyMuPDF

def extract_pdf_text(file_path: str) -> str:
    try:
        doc = fitz.open(file_path)
        full_text = []
        for page in doc:
            text = page.get_text("text")  # 直接获取带换行符的文本
            paragraphs = text.split('\n\n')  # 双换行分割段落
            # 移除空段落
            paragraphs = [p.strip() for p in paragraphs if p.strip()]
            full_text.extend(paragraphs)
        return '\n\n'.join(full_text)
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_text_from_fb2(file_path):
    ns = {'fb2': 'http://www.gribuser.ru/xml/fictionbook/2.0'}
    tree = ET.parse(file_path)
    root = tree.getroot()
    text_elements = root.findall('.//fb2:p', ns)
    return '\n'.join([elem.text.strip() for elem in text_elements if elem.text])


def parse_epub(epub_file_path):
    """
    解析 EPUB 文件，提取文本内容。

    Args:
        epub_file_path (str): EPUB 文件路径。

    Returns:
        str: EPUB 文件的文本内容。
    """
    try:
        book = epub.read_epub(epub_file_path)
        text = ""
        for item in book.get_items():
            if item.media_type == "application/xhtml+xml":
                content = item.get_content().decode("utf-8")
                # 从 HTML 内容中提取文本
                text += content
        return text
    except Exception as e:
        print(f"解析 EPUB 文件时出错：{e}")
        return None

def parse_epub_stream(epub_file_path):
    """
    流式解析 EPUB 文件，提取文本内容。

    Args:
        epub_file_path (str): EPUB 文件路径。

    Yields:
        str: EPUB 文件的文本内容块。
    """
    try:
        book = epub.read_epub(epub_file_path)
        for item in book.get_items():
            if item.media_type == "application/xhtml+xml":
                content = item.get_content().decode("utf-8")
                # 从 HTML 内容中提取文本
                yield content
    except Exception as e:
        print(f"解析 EPUB 文件时出错：{e}")
        yield None
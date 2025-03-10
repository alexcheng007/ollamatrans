from ebooklib import epub

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
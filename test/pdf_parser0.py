import PyPDF2

def extract_pdf_text(file_path: str) -> str:
    """
    读取PDF文件中的所有文本内容
    :param file_path: PDF文件路径
    :return: 合并后的文本字符串
    """
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            full_text = []
            print(f"pages = {len(pdf_reader.pages)}")
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                if text:
                    full_text.append(text)
            return '\n'.join(full_text)
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

if __name__ == "__main__":
    # 测试代码（请先安装依赖：pip install pypdf）
    TEST_FILE = "test.pdf"
    result = extract_pdf_text(TEST_FILE)
    print("Extracted Text:")
    print("---------------")
    print(result)
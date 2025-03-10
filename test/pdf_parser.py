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

if __name__ == "__main__":
    TEST_FILE = "test.pdf"
    result = extract_pdf_text(TEST_FILE)
    print("Extracted Text:")
    print("---------------")
    print(result)
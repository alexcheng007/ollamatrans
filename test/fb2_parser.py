import sys
import xml.etree.ElementTree as ET

def extract_text_from_fb2(file_path):
    ns = {'fb2': 'http://www.gribuser.ru/xml/fictionbook/2.0'}
    tree = ET.parse(file_path)
    root = tree.getroot()
    text_elements = root.findall('.//fb2:p', ns)
    return '\n'.join([elem.text.strip() for elem in text_elements if elem.text])

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python fb2file.py [file.fb2]")
        sys.exit(1)
    try:
        print(f"Processing file: {sys.argv[1]}")
        text = extract_text_from_fb2(sys.argv[1])
        print(text)
    except Exception as e:
        print(f"Error: {str(e)}")
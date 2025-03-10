"""
Ollama 翻译器主程序模块
作者: alex cheng <xcheng@vidts.com>
版本: 0.1.0
生成日期: 2025-3-10

模块功能：
- 提供图形界面
- 协调文件解析与翻译流程
- 实现翻译结果保存功能
"""
import sys
import threading

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QFileDialog,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QTextEdit,
    QProgressBar,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal

from files_parser import parse_epub_stream, extract_text_from_fb2, extract_pdf_text
from ollama_translator import translate_text

class MainWindow(QWidget):
    """
    主窗口类，包含界面组件和核心功能实现
    """
    text_appended = pyqtSignal(str)         # 原始文本追加信号
    translation_appended = pyqtSignal(str)  # 翻译文本追加信号
    progress_updated = pyqtSignal(int)      # 翻译进度更新信号
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ollama 翻译 GUI")
        # 存储文本分块和翻译结果的列表
        self.chunks = []
        self.translated_chunks = []
        
        # 初始化界面组件
        self._init_components()    # 创建文本框和按钮组件
        self._init_layout()        # 构建界面布局
        self._connect_signals()    # 绑定信号槽函数
        # 默认翻译模型名称
        self.model_name = "sam860/dolphin3-qwen2.5:3b"
        
    def _init_components(self):
        """初始化界面组件"""
        self.original_text_edit = QTextEdit()      # 原始文本显示框
        self.translated_text_edit = QTextEdit()    # 翻译结果显示框
        
        # 创建按钮组件
        self.open_button = QPushButton("打开文件")
        self.start_translate_button = QPushButton("翻译")
        self.save_button = QPushButton("保存为Markdown")
        
        # 初始化进度条组件
        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)               # 初始进度值设为0
        
    def _init_layout(self):
        """构建界面布局"""
        # 设置字体样式
        font = QFont("Arial", 14)
        self.original_text_edit.setFont(font)
        self.translated_text_edit.setFont(font)
        
        # 主布局容器
        main_vbox = QVBoxLayout()
        
        # 工具栏布局：包含打开/翻译按钮
        toolbar = QHBoxLayout()
        toolbar.addWidget(self.open_button)
        toolbar.addWidget(self.start_translate_button)
        main_vbox.addLayout(toolbar)
        
        # 文本框并排布局
        text_area = QHBoxLayout()
        text_area.addWidget(self.original_text_edit)
        text_area.addWidget(self.translated_text_edit)
        main_vbox.addLayout(text_area)
        
        # 底部按钮+进度条布局
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.progressBar)
        main_vbox.addLayout(buttons_layout)
        
        self.setLayout(main_vbox)
        
    def _connect_signals(self):
        """绑定信号与槽函数"""
        self.open_button.clicked.connect(self.open_file)
        self.start_translate_button.clicked.connect(self.start_translation)
        self.save_button.clicked.connect(self.save_to_markdown)
        
        # 绑定文本追加信号到显示控件
        self.text_appended.connect(self.original_text_edit.append)
        self.translation_appended.connect(self.translated_text_edit.append)

    def open_file(self):
        """打开文件对话框并解析文件内容"""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "打开文件", "",
            "PDF 文件 (*.pdf);;EPUB 文件 (*.epub);;FB2 文件 (*.fb2);;文本文件 (*.txt)")

        if not file_path:
            return            # 用户取消选择时直接退出
            
        self.original_text_edit.clear()
        self.translated_text_edit.clear()
        self.epub_file_path = file_path    # 保存EPUB文件路径供其他方法使用
        
        # 根据文件类型调用对应解析方法
        parse_func = {
            '.pdf': self.parse_and_display_pdf,
            '.epub': self.parse_and_display_epub,
            '.txt': self.parse_and_display_text,
            '.fb2': self.parse_and_display_fb2,
        }
        
        # 获取文件扩展名并执行解析
        ext = file_path[file_path.rfind('.'):]
        if ext in parse_func:
            parse_func[ext](file_path)
        else:
            print(f"不支持的文件类型: {ext}")

    def parse_and_display_epub(self, file_path):
        """解析EPUB文件并显示内容"""
        def load_text():
            for chunk in parse_epub_stream(file_path):
                self.chunks.append(chunk)
                self.text_appended.emit(str(chunk))
        threading.Thread(target=load_text).start()

    def parse_and_display_text(self, file_path):
        """解析文本文件并显示内容"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.original_text_edit.setPlainText(content)
        except Exception as e:
            print(f"读取文本文件错误: {str(e)}")

    def parse_and_display_fb2(self, file_path):
        """解析FB2文件并显示内容"""
        try:
            content = extract_text_from_fb2(file_path)
            self.original_text_edit.setPlainText(content)
        except Exception as e:
            print(f"读取fb2文件错误: {str(e)}")

    def parse_and_display_pdf(self, file_path):
        """解析PDF文件并显示内容"""
        try:
            content = extract_pdf_text(file_path)
            self.original_text_edit.setPlainText(content)
        except Exception as e:
            print(f"读取pdf文件错误: {str(e)}")

    def process_chunks(self, chunks):
        """处理文本分块并翻译"""
        for index, chunk in enumerate(chunks):
            if not chunk.strip():
                continue
            self.progress_updated.emit(index + 1)
            self.translate_and_append(chunk)
            
    def translate_and_append(self, chunk):
        """翻译单个分块并追加结果到翻译列表"""
        translated = translate_text(chunk, self.model_name)
        if translated:
            self.translated_chunks.append(translated)
            self.translation_appended.emit(translated)
            
    def start_translation(self):
        """开始翻译流程，将原文本分割为合理大小的分块"""
        self.translated_text_edit.clear()
        self.translated_chunks = []
        text = self.original_text_edit.toPlainText()
        # 按行分割文本，否则文本太长，大模型可能没法完成正确的翻译，而且每段的等待时间太长！
        chunks = []
        current_chunk = ""
        end_chars = {'.', '?', '!', '"', '”', '。', '？', '！'}
        
        lines = text.split('\n')
        for line in lines:
            stripped_line = line.rstrip()
            if not stripped_line:
                continue  # 跳过空行
            current_line_with_newline = line + '\n'
            current_chunk += current_line_with_newline
        
            last_char = stripped_line[-1]
            if last_char in end_chars:
                chunks.append(current_chunk.strip('\n'))
                current_chunk = ""
        
        # 处理剩余内容
        if current_chunk:
            chunks.append(current_chunk.strip('\n'))
        # 连接进度信号并初始化进度条
        self.progressBar.setMaximum(len(chunks))
        self.progressBar.setValue(0)
        self.progress_updated.connect(self.progressBar.setValue)
        thread = threading.Thread(target=self.process_chunks, args=(chunks,))
        thread.start()

    def save_to_markdown(self):
        """保存翻译结果为Markdown文件"""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(
            self, "保存为 Markdown", "", "Markdown 文件 (*.md)"
        )

        if file_path:
            text = '\n\n'.join(self.translated_chunks)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())
    
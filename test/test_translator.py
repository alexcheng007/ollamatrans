import sys
import os
import unittest
import time
from translator import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestTranslator(unittest.TestCase):

    def test_translate_text(self):
        # 定义测试文本和模型名称
        test_text = '''I’ve uploaded the quants of these models that I find most useful. 
        I quantized them myself using the fp16 GGUF files provided by mradermacher. 
        The default temperature has been adjusted - 
        as I find the smaller qwen models tends to hallucinate too much at higher temps.'''
        
        model_name = "sam860/dolphin3-qwen2.5:3b"  # 替换为你的 Ollama 模型名称

        # 记录开始时间
        start_time = time.time()

        # 调用翻译函数
        translated_text = translate_text(test_text, model_name)

        # 记录结束时间
        end_time = time.time()

        # 计算执行时间
        execution_time = end_time - start_time

        # 验证翻译结果
        self.assertIsNotNone(translated_text, "翻译结果不应为 None")
        self.assertIsInstance(translated_text, str, "翻译结果应为字符串")
        self.assertTrue(len(translated_text) > 0, "翻译结果不应为空字符串")

        # 打印测试结果
        print("测试文本:", test_text)
        print("模型名称:", model_name)
        print("翻译后的文本:", translated_text)
        print("执行时间:", execution_time, "秒")
        print("测试通过")

if __name__ == '__main__':
    unittest.main()
"""
Ollama 翻译接口模块
作者: alex cheng <xcheng@vidts.com>
版本: 0.1.0
生成日期: 2025-3-10

模块功能：
- 封装Ollama API调用
- 实现文本翻译功能
"""
import ollama

def translate_text(text, model_name):
    import traceback
    try:
        print(f"正在翻译：模型={model_name}, 文本长度={len(text)}")
        prompt_text = f"请将以下文本翻译成中文：\n{text}"
        response = ollama.generate(model=model_name, prompt=prompt_text)
        print(f"API响应：{response}")
        return response.get('response', None)
    except Exception as e:
        print(f"翻译错误：{str(e)}\n堆栈跟踪：{traceback.format_exc()}")
        return None
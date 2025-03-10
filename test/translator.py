import ollama

def translate_text(text, model_name):
    import traceback
    try:
        '''
        if not text.strip():
            return "*** [空 行] ***"
        '''
        
        #print(f"正在翻译：模型={model_name}, 文本长度={len(text)}")
        prompt_text = f"请将以下文本翻译成中文：\n{text}"
        response = ollama.generate(model=model_name, prompt=prompt_text)
        #print(f"API响应：{response}")
        return response.get('response', None)
    except Exception as e:
        print(f"翻译错误：{str(e)}\n堆栈跟踪：{traceback.format_exc()}")
        return None
import os
import openai

class Translator:
    def __init__(self):
        self.client = openai.OpenAI(
            base_url=os.getenv('OPENAI_BASE_URL'),
            api_key=os.getenv('OPENAI_API_KEY'),
        )

    def translate(self, text, lang='cn'):
        lang_prompt = '请把以下句子翻译成中文:' if lang == 'cn' else '日本語に翻訳してください:'
        
        translation = self.client.chat.completions.create(
            model=os.getenv('MODEL'),
            messages=[
                {"role": "system", "content": 'You are an expert in translation and I will give you a sentence that you will translate into another language. You just need to return the translation without any other extra words.'},
                {"role": "user", "content": lang_prompt + text},
            ],
            stream=True,
            temperature=0.5,
        )
        
        result = ''
        for chunk in translation:
            if chunk.choices[0].delta.content is not None:
                result += chunk.choices[0].delta.content
        return result

    def optimize_query(self, query, lang='cn'):
        if lang != 'cn':
            query = self.translate(query, lang)
        
        better_query = self.client.chat.completions.create(
            model='Qwen/Qwen2-72B-Instruct',
            messages=[
                {"role": "system", "content": 'You are an expert in search engine utilization and I will give you a question that you will optimize into a search term more suitable for the search engines to hand over to me. Usually it will be in the form of a keyword with a space so that you can cover most of the answers. You just need to return the optimization results without any other extra words.'},
                {"role": "user", "content": query},
            ],
            stream=True,
            temperature=0.3,
        )
        
        result = ''
        for chunk in better_query:
            if chunk.choices[0].delta.content is not None:
                result += chunk.choices[0].delta.content
        return result.strip('"')
    
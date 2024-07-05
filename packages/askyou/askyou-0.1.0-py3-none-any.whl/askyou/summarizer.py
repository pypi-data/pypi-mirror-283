import os
import openai
from bs4 import BeautifulSoup
from askyou.utils import requests_retry_session

class Summarizer:
    def __init__(self):
        self.client = openai.OpenAI(
            base_url=os.getenv('OPENAI_BASE_URL'),
            api_key=os.getenv('OPENAI_API_KEY'),
        )

    def fetch_and_summarize(self, url):
        content = self._fetch_content(url)
        return self._summarize(content)

    def _fetch_content(self, url):
        response = requests_retry_session().get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for meta in soup.find_all('meta'):
            if 'content' in meta.attrs:
                content = meta['content']
                charset_pos = content.lower().find('charset=')
                if charset_pos != -1:
                    charset = content[charset_pos + 8:].split(';')[0]
                    response.encoding = 'gbk' if charset == 'GB2312' else 'utf-8'
                    break

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        
        text_content_list = [url]
        for tag in soup.find_all(['p', 'code']):
            text_content_list.append(tag.get_text())
        
        return ' '.join(text_content_list)

    def _summarize(self, content):
        response = self.client.chat.completions.create(
            model=os.getenv('MODEL'),
            messages=[
                {"role": "system", "content": '你是总结文章的专家，我会给你一篇文章，你需要将文章进行总结，请尽量详细易懂，使用中文。'},
                {"role": "user", "content": content},
            ],
            max_tokens=4056,
            stream=True,
            temperature=0.6,
        )
        
        summary = ''
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                summary += chunk.choices[0].delta.content
        return summary
    
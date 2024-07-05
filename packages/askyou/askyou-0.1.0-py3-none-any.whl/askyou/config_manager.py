import os
import json
from dotenv import load_dotenv, set_key

class ConfigManager:
    def __init__(self):
        self.env_file = '.env'
        load_dotenv(self.env_file)

    def get_token(self, key):
        return os.getenv(key)

    def set_token(self, key, value):
        set_key(self.env_file, key, value)
        os.environ[key] = value

    def check_tokens(self):
        required_tokens = ['BING_SUBSCRIPTION_KEY', 'OPENAI_API_KEY', 'OPENAI_BASE_URL', 'MODEL']
        missing_tokens = [token for token in required_tokens if not self.get_token(token)]
        return missing_tokens
    
    def load_config(self):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(project_root, 'askyou/config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    
    def update_config(self, new_text):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(project_root, 'askyou/config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        target_sentence = 'You will be given a set of related contexts to the question'
        index = config['rag_query_text'].find(target_sentence)
        if index != -1:
            config['rag_query_text'] = new_text + config['rag_query_text'][index:]
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
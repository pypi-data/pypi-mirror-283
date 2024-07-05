import os
import requests
from loguru import logger

class BingSearchEngine:
    BING_MKT = "en-US"
    BING_SEARCH_V7_ENDPOINT = "https://api.bing.microsoft.com/v7.0/search"
    DEFAULT_SEARCH_ENGINE_TIMEOUT = 5
    REFERENCE_COUNT = 8

    def __init__(self):
        self.subscription_key = os.getenv('BING_SUBSCRIPTION_KEY')

    def search(self, query: str):
        params = {"q": query, "mkt": self.BING_MKT}
        response = requests.get(
            self.BING_SEARCH_V7_ENDPOINT,
            headers={"Ocp-Apim-Subscription-Key": self.subscription_key},
            params=params,
            timeout=self.DEFAULT_SEARCH_ENGINE_TIMEOUT,
        )
        if not response.ok:
            logger.error(f"{response.status_code} {response.text}")
        json_content = response.json()
        try:
            contexts = json_content["webPages"]["value"][:self.REFERENCE_COUNT]
        except KeyError:
            logger.error(f"Error encountered: {json_content}")
            return []
        return contexts
    
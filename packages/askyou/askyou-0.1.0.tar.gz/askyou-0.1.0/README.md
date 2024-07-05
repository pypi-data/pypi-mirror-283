# ASK YOU

AI Search Assistant is a command-line tool that leverages AI to perform intelligent searches and summarizations.

## Installation

```bash
git clone https://github.com/xieweicong/ask-you.git
cd ask-you
pip install .
```

```bash
askyou set-token OPENAI_BASE_URL ${OPENAI_BASE_URL}
askyou set-token BING_SUBSCRIPTION_KEY ${BING_SUBSCRIPTION_KEY}
askyou set-token OPENAI_API_KEY ${OPENAI_API_KEY}
askyou set-token MODEL ${MODEL_NAME}
```
Not only openai, you can use all openai-compatible services, such as siliconflow.

```bash
askyou whoami '${about youself}'
```
You can use this command to give him information about yourself so that you can understand what you need and what you are more interested in when searching.
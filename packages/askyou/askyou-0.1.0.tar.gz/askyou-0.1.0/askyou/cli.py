import click
import re
from askyou.search_engine import BingSearchEngine
from askyou.translator import Translator
from askyou.summarizer import Summarizer
from askyou.config_manager import ConfigManager
import concurrent.futures
import time

import openai
import os

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        ctx.invoke(query_function)

@cli.command(name='set-token')
@click.argument('key')
@click.argument('value')
def set_token(key, value):
    """This command is used to set an API token and model."""
    config_manager = ConfigManager()
    """Set an API token."""
    config_manager.set_token(key, value)
    click.echo(f"Token {key} has been set.")

def check_tokens():
    config_manager = ConfigManager()
    missing_tokens = config_manager.check_tokens()
    if missing_tokens:
        click.echo("The following tokens are missing:")
        for token in missing_tokens:
            click.echo(f"- {token}")
        click.echo("Please set them using the 'set-token' command.")
        return False
    return True

@cli.command(name='about')
@click.option('--lang', default='cn', help='language of the search query')
@click.option('--all', is_flag=True, help='fetch the all context')
@click.argument('query', default='Who said "live long and prosper"?')
def query_function(query, lang, all):
    """This command is used to query the AI search engine."""
    query = query or "Who said 'live long and prosper'?"
    query = re.sub(r"\[/?INST\]", "", query)
    
    translator = Translator()
    search_query = translator.optimize_query(query, lang)
    print('search_query:', search_query)
    
    search_engine = BingSearchEngine()
    contexts = search_engine.search(search_query)
    
    if all:
        start_time = time.time()
        summarizer = Summarizer()
        
        def process_context(context):
            url = context['url']
            context['snippet'] += summarizer.fetch_and_summarize(url)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_context, context) for context in contexts]
            concurrent.futures.wait(futures)
        
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")

    system_prompt = _create_system_prompt(contexts)
    
    client = openai.OpenAI(
        base_url=os.getenv('OPENAI_BASE_URL'),
        api_key=os.getenv('OPENAI_API_KEY'),
    )
    
    response = client.chat.completions.create(
        model=os.getenv('MODEL'),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
        max_tokens=1024,
        stream=True,
        temperature=0.8,
    )

    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end='')
    print('\n')
    print('\n'.join([f"[[citation:{i+1}]] {c['url']}" for i, c in enumerate(contexts)]))

def _create_system_prompt(contexts):
    config_manager = ConfigManager()
    config = config_manager.load_config()
    rag_query_text = config['rag_query_text']
    return rag_query_text.format(
        context="\n\n".join(
            [f"[[citation:{i+1}]] {c['snippet']}" for i, c in enumerate(contexts)]
        )
    )

@cli.command(name='whoami')
@click.argument('prompt')
def whoami(prompt):
    """This command is used to update the prompt."""
    config_manager = ConfigManager()
    config_manager.update_config(prompt)

@cli.command(name='url')
@click.argument('url')
def summarize_url(url):
    """This command is used to process the given URL."""
    summarizer = Summarizer()
    summary = summarizer.fetch_and_summarize(url)
    print(summary)

if __name__ == "__main__":
    cli()

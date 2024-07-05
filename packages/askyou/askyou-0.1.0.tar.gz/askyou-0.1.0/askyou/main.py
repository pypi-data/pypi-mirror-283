import os
from dotenv import load_dotenv

from askyou.cli import cli, check_tokens

def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 构建 .env 文件的路径
    env_path = os.path.join(project_root, '.env')

    # 加载 .env 文件
    load_dotenv(env_path)
    check_tokens()
    cli()

if __name__ == "__main__":
    main()
from setuptools import setup, find_packages

setup(
    name="askyou",
    version="0.1.0",
    author="xie weicong",
    author_email="xieweicong95@gmail.com",
    description="A ai search cli",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/xieweicong/askyou",
    packages=find_packages(),
    package_data={
        'askyou': ['*.json'],
    },
    install_requires=[
        "click",
        "requests",
        "beautifulsoup4",
        "openai",
        "python-dotenv",
        "loguru",
    ],  # 项目依赖
    entry_points={
        "console_scripts": [
            "askyou=askyou.main:main",  # 这定义了命令行入口点
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # 指定 Python 版本要求
)
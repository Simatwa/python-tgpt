from pathlib import Path

from setuptools import setup


DOCS_PATH = Path(__file__).parents[0] / "docs/README.md"
PATH = Path("README.md")
if not PATH.exists():
    with Path.open(DOCS_PATH, encoding="utf-8") as f1:
        with Path.open(PATH, "w+", encoding="utf-8") as f2:
            f2.write(f1.read())

setup(
    name="python-tgpt",
    version="0.1.4",
    license="MIT",
    author="Smartwa",
    maintainer="Smartwa",
    author_email="simatwacaleb@proton.me",
    description="Interact with AI without API key",
    packages=["tgpt"],
    url="https://github.com/Simatwa/python-tgpt",
    project_urls={
        "Bug Report": "https://github.com/Simatwa/python-tgpt/issues/new",
        "Homepage": "https://github.com/Simatwa/python-tgpt",
        "Source Code": "https://github.com/Simatwa/python-tgpt",
        "Issue Tracker": "https://github.com/Simatwa/python-tgpt/issues",
        "Download": "https://github.com/Simatwa/python-tgpt/releases",
        "Documentation": "https://github.com/Simatwa/python-tgpt/blob/main/docs",
    },
    entry_points={
        "console_scripts": [
            "tgpt = tgpt.console:main",
        ],
    },
    install_requires=[
        "requests==2.28.2",
        "click==8.1.3",
        "rich==13.3.4",
        "clipman==3.1.0",
        "pyperclip==1.8.2",
        "appdirs==1.4.4",
    ],
    python_requires=">=3.9",
    keywords=[
        "chatgpt",
        "gpt",
        "tgpt" "chatgpt-cli",
        "chatgpt-sdk",
        "chatgpt-api",
        "llama-api",
    ],
    long_description=Path.open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: Free For Home Use",
        "Intended Audience :: Customer Service",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)

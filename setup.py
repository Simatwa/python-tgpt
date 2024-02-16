from pathlib import Path

from setuptools import setup

from setuptools import find_packages


INSTALL_REQUIRE = [
    "requests==2.28.2",
    "appdirs==1.4.4",
    "pyyaml==6.0.1",
    "webchatgpt==0.2.7",
    "GoogleBard1==2.1.1",
    "poe-api-wrapper==1.3.6",
]

cli_reqs = [
    "click==8.1.3",
    "rich==13.3.4",
    "clipman==3.1.0",
    "pyperclip==1.8.2",
    "colorama==0.4.6",
    "g4f>=0.2.1.2",
    "python-dotenv==1.0.0",
]

EXTRA_REQUIRE = {
    "cli": cli_reqs,
    "all": ["g4f[all]>=0.2.1.0", "matplotlib", "gpt4all==2.2.0"] + cli_reqs,
}

DOCS_PATH = Path(__file__).parents[0] / "docs/README.md"
PATH = Path("README.md")
if not PATH.exists():
    with Path.open(DOCS_PATH, encoding="utf-8") as f1:
        with Path.open(PATH, "w+", encoding="utf-8") as f2:
            f2.write(f1.read())

setup(
    name="python-tgpt",
    version="0.5.3",
    license="MIT",
    author="Smartwa",
    maintainer="Smartwa",
    author_email="simatwacaleb@proton.me",
    description="Interact with AI without API key",
    packages=find_packages("src"),
    package_dir={"": "src"},
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
            "pytgpt = pytgpt.console:main",
        ],
    },
    install_requires=INSTALL_REQUIRE,
    extras_require=EXTRA_REQUIRE,
    python_requires=">=3.9",
    keywords=[
        "chatgpt",
        "gpt",
        "tgpt",
        "pytgpt",
        "chatgpt-cli",
        "chatgpt-sdk",
        "chatgpt-api",
        "llama-api",
        "leo",
        "llama2",
        "blackboxai",
        "opengpt",
        "koboldai",
        "openai",
        "bard",
        "gpt4free",
        "gpt4all-cli",
        "gptcli",
        "poe-api",
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

from setuptools import setup, find_packages

setup(
    name="sentiment-analysis-alan-garcia",
    version="0.1.0",
    description="Sentiment analysis of Alan García death news",
    author="Harold Eustaquio",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "nltk",
    ],
    python_requires=">=3.7",
)

from setuptools import setup, find_packages

setup(
    name="hashtbl",
    version="1.0.1",
    author="khiat Mohammed Abderrezzak",
    author_email="khiat.dev@gmail.com",
    license="MIT",
    description="Sophisticate Hash Table",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/hashtbl/",
    packages=find_packages(),
    install_requires=[
        "tabulate>=0.9.0",
        "linkedit>=1.1.0",
    ],
    keywords=[
        "hash table",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)

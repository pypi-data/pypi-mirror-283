from setuptools import setup, find_packages

setup(
    name="sophisticate",
    version="1.0.5",
    author="khiat Mohammed Abderrezzak",
    author_email="khiat.abderrezzak@gmail.com",
    license="MIT",
    description="Sophisticate Libraries Collection",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/sophisticate/",
    packages=find_packages(),
    install_requires=[
        "conf-mat>=1.0.7",
        "linkedit>=1.0.9",
        "cqueue>=1.0.5",
        "lstack>=1.0.5",
        "hashall>=1.0.1",
        "thri>=1.0.0",
        "heep>=1.0.0",
        "hashtbl>=1.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
)

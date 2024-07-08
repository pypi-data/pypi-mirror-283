from setuptools import setup, find_packages

setup(
    name="chattemplate",
    version="0.1.0-dev4",
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    install_requires=[
        "gradio",
        "transformers",
        "openai",
        "sentencepiece",
        "protobuf",
        "accelerate",
    ],
    entry_points={
        "console_scripts": [
            "chattemplate=chattemplate.cli:main",
        ],
    },
    author="ericmccpr",
    author_email="ericweb781@gmail.com",
    description="ChatTemplate",
    url="https://github.com/mccpr/chattemplate",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)

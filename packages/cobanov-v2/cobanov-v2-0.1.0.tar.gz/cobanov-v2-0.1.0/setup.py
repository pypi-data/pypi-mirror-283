from setuptools import setup, find_packages

setup(
    name="cobanov-v2",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "cobanov=cobanov.main:main",
        ],
    },
    install_requires=[
        # Add your dependencies here, e.g.,
        # 'requests',
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="cobanov command line tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/cobanov/cobanov",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

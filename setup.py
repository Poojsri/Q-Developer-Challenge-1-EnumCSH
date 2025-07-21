from setuptools import setup, find_packages

setup(
    name="enumcsh",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    py_modules=["enumcsh"],
    install_requires=[
        "typer>=0.4.0",
        "rich>=10.0.0",
        "click>=8.0.0",
        "shellingham>=1.3.0",
        "typing-extensions>=3.7.4.3",
        "markdown-it-py>=2.2.0",
        "pygments>=2.13.0",
        "mdurl>=0.1.0",
    ],
    entry_points={
        'console_scripts': [
            'enumcsh=enumcsh:app',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A CLI tool that automates and simplifies port enumeration for penetration testing",
    keywords="penetration testing, port enumeration, security, nmap, metasploit",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
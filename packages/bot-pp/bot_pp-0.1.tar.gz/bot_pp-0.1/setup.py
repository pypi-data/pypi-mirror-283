from setuptools import setup, find_packages

setup(
    name="bot-pp",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'p!c=scripts.p_c:main',
        ],
    },
    author="P",
    author_email="parepare2154@gmail.com",
    description="A library that creates a Python bot",
    url="https://ppbot.web.app/mylibrary",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

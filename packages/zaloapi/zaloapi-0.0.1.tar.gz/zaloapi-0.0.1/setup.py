from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'zaloapi: Zalo Chat for Python'
LONG_DESCRIPTION = 'Zalo Chat for Python. This project was inspired by fbchat. No XMPP or API key is needed. Just use your email and password (Not support yet) or cookies.'

# Setting up
setup(
    name="zaloapi",
    version=VERSION,
    author="Lê Quốc Việt (Vexx)",
    author_email="<vrxxdev@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests', 'asyncio', 'aenum', 'attr', 'datetime'],
    keywords=['python', 'zalo', 'api', 'zalo api', 'zalo chat', 'requests'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ]
)

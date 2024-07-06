from setuptools import setup, find_packages

setup(
    name='arbitrum-sdk',
    version='0.1.0',
    packages=find_packages(),
    description='Python library for client-side interactions with Arbitrum',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Mert Köklü',
    author_email='mert@yk-labs.com',
    url="https://github.com/justmert/arbitrum-python-sdk",
    install_requires=[
        "web3==6.3.0",
        "rlp==3.0.0",
        "eth-utils==2.3.1",
        "python-dotenv==1.0.0",
        "eth-typing==3.5.2",
        "asyncio==3.4.3",
        "eth-abi==4.2.1",
        "pyyaml==6.0.1",
        "addict==2.4.0",
        "py-evm==0.8.0b1",
    ],

    classifiers=[
        # Choose your license as you wish
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires=">=3.8",
)
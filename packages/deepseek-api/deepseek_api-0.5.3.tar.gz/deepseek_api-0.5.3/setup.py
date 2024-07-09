from setuptools import setup, find_packages

setup(
    name='deepseek_api',
    version='0.5.3',
    packages=find_packages(),
    install_requires=[
        'certifi',
        'charset-normalizer',
        'idna',
        'python-dotenv',
        'requests',
        'urllib3',
        'PyJWT',
        'aiofiles',
        'aiohttp'
    ],
    description='An unofficial Python API wrapper for chat.Deepseek.com',
)
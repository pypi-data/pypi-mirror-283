from setuptools import setup

setup(
    name='wezahttp',
    version='1.0.8',
    py_modules=['wezahttp'],
    install_requires=[
        'aiohttp',
        'asyncio',
    ],
    author='wezaxyy',
    author_email='wezababass@gmail.com',
    description='A simple async HTTP client module.',
    url='https://github.com/wezaxy/wezahttp',
)

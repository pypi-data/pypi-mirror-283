from setuptools import setup, find_packages

setup(
    name='millennium',
    version='0.1.0',
    author='Steam Client Homebrew',
    description='A support library for creating plugins with Millennium.',
    long_description=open('../README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/SteamClientHomebrew/PluginComponents',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.11.8'
)
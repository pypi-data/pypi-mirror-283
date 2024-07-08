from setuptools import setup, find_packages
import os

# Ensure the README file is read correctly
def read_readme():
    try:
        with open('README.md', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""

setup(
    name='flexiai',
    version='0.8.44',
    packages=find_packages(include=['flexiai', 'flexiai.*']),
    include_package_data=True,
    package_data={
        'flexiai': [
            'assistant/*.py',
            'config/*.py',
            'core/*.py',
            'core/utils/*.py'
        ],
    },
    install_requires=[
        'openai==1.35.0',
        'azure-common==1.1.28',
        'azure-core==1.30.2',
        'azure-identity==1.17.1',
        'azure-mgmt-core==1.4.0',
        'azure-mgmt-resource==23.1.1',
        'pytest==8.2.2',
        'pytest-mock==3.14.0',
        'pydantic==2.7.4',
        'pydantic-settings==2.3.3',
        'pydantic_core==2.18.4',
        'platformdirs==3.7.0',
        'python-dotenv==1.0.1',
        'urllib3==2.2.2',
    ],
    entry_points={
        'console_scripts': [
            # Define command line scripts here if needed
        ],
    },
    author='Savin Ionut Razvan',
    author_email='razvan.i.savin@gmail.com',
    description='FlexiAI is a powerful AI framework that simplifies the integration and management of OpenAI and Azure OpenAI services, featuring advanced Retrieval-Augmented Generation (RAG) capabilities for efficient AI-driven application development.',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/SavinRazvan/flexiai',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
    ],
    python_requires='>=3.10',
    project_urls={
        'Bug Reports': 'https://github.com/SavinRazvan/flexiai/issues',
        'Source': 'https://github.com/SavinRazvan/flexiai',
    },
    license='MIT',
)

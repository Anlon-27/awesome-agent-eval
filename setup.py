# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='awesome-agent-eval',
    version='1.0.0',
    description='The Definitive Guide, Methodology & Engineering Toolkit for AI Agent Evaluation',
    author='Awesome Agent Eval Contributors',
    packages=find_packages(),
    python_requires='>=3.10',
    install_requires=[
        'pydantic>=2.5.0',
        'tabulate>=0.9.0',
        'pytest>=8.0.0',
    ],
    entry_points={
        'console_scripts': [
            'agent-eval=agent_eval.cli:main',
        ],
    },
)\n
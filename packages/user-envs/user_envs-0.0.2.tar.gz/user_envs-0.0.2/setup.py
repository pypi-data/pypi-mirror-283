import setuptools
from pathlib import Path


setuptools.setup(
    name='user_envs',
    version='0.0.2',
    description='An openAI gym environment from user',
    long_description=Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(include='user_envs*'),
    install_requires=["gymnasium>=0.26.0", "pygame>=2.1.0"]
)

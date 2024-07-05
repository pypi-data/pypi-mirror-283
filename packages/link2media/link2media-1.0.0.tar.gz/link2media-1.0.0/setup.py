from setuptools import setup, find_packages

setup(
    name='link2media',
    version='1.0.0',
    author='tawsif',
    author_email='sleeping4cat@outlook.com',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'pytube',
        'ffmpeg-python',
    ],
)

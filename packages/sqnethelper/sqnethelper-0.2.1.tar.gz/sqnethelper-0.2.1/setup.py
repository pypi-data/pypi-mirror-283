from setuptools import setup, find_packages

setup(
    name='sqnethelper',
    version='0.2.1',
    packages=find_packages(),
    install_requires=[
        'click',
        'aliyun-python-sdk-core',
        'aliyun-python-sdk-ecs',
    ],
    entry_points={
        'console_scripts': [
            'sqnethelper=sqnethelper.cli:cli',
        ],
    },
    author='weisq',
    author_email='weishqdev@gmail.com',
    description='A command line tool to manage Alibaba Cloud ECS instances',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

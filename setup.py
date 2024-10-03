from setuptools import setup, find_packages

setup(
    name='moneytalks',
    version='0.1',
    description='Convert numbers to ru currency strings',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ivan Dovbnya',
    author_email='supreltd@gmail.com',
    url='https://github.com/yourusername/moneytalks',
    packages=find_packages(),
    install_requires=[],
    license='GNU',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

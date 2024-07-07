# setup.py

from setuptools import setup, find_packages

setup(
    name='pyfun_my',
    version='0.1',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        # Add any dependencies here
    ],
    tests_require=[
        'pytest',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    url='https://github.com/mywyau/pyfun',  # Replace with your GitHub URL
    author='Michael Yi wing Yau',
    author_email='m.yw.yau@gmail.com',
    description='personal library for functional programming',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

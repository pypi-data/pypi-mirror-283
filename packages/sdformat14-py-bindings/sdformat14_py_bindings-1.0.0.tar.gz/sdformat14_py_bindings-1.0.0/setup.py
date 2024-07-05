from setuptools import setup, find_packages

setup(
    name='sdformat14-py-bindings',
    version='1.0.0',
    description='Python 3.11 bindings for Gazebo sdformat14 library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Jc Cloete',
    author_email='jc@truevolve.technology',
    url='https://github.com/Jc-Cloete',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    package_data={
        'sdformat14': [
            '*.so',
            '*.py',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.11',
)

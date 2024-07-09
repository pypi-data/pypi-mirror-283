from setuptools import setup, find_packages

setup(
    name='dbx_utils',
    version='0.3.1',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'requests',
        'databricks-api'
    ],
    author='Ranjit Maity',
    author_email='ranjitmaity95@gmail.com',
    description='A utility package for managing Databricks folders and permissions',
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

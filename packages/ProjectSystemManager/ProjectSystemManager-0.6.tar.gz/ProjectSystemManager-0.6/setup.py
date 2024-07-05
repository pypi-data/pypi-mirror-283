from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='ProjectSystemManager',
    version='0.6',
    packages=find_packages(),
    install_requires=[
        'configparser',
    ],  # Add a comma here
    author='A. Sharan',
    author_email='hemsharan3050@gmail.com',
    description='ProjectSystemManager is a Python library designed to manage projects by creating, updating, searching, and fetching project details. It allows you to organize projects in a specified directory and store relevant information such as project name, creation date, technologies used, and a summary.',

    long_description=long_description,
    long_description_content_type='text/markdown',

    keywords='project management, python library, project system',
    python_requires='>=3.7',
    license='MIT',
     project_urls={
           'Source Repository': 'https://github.com/AHSharan/ProjectManager/',
           'YouTube': 'https://www.youtube.com/@A.Sharan'
    }
)

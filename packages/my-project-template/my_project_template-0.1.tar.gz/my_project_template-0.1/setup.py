from setuptools import setup, find_packages
from setuptools.command.install import install
import my_project_template

class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        my_project_template.initialize_project()

setup(
    name='my_project_template',
    version='0.1',
    author='Your Name',
    author_email='your.email@example.com',
    description='A template that creates a project structure upon installation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ravi46931/my_project_template',
    packages=find_packages(),
    include_package_data=True,
    cmdclass={
        'install': CustomInstallCommand,
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

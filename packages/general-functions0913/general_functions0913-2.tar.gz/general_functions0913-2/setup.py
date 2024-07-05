from setuptools import setup, find_packages

setup(
    name='general_functions0913',
    version='2',
    description='this sdk is a working protype with file encryption',
    author='rishabh_sharma',
    author_email='rishabhsharmabwr@gmail.com',
    packages=find_packages(),
    install_requires=[
        # Add any other dependencies here
    ],
)

#command to run setup.py
    # -> python3 setup.py sdist
#command to uplode sdk package to PyPi account
    # -> twine upload dist/*
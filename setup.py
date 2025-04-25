from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT = '-e .'
'''
After hiting 'pip install -r requirements.txt', download dependencies and thenautomatically trigers setup.py 
'''

def get_requirements(file_path:str)->List[str]:
    '''
        This function will return the list of requirements.txt
    '''
    requirements =[]
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        [req.replace("\n", "") for req in requirements]

        if(HYPEN_E_DOT in requirements):
            requirements.remove(HYPEN_E_DOT)
    return requirements


setup(
    name='ML-Project-1',
    version='0.0.1',
    author="Dinesh Gupta",
    author_email='dineshgupta08710@gmail.com',
    packages=find_packages(),
    install_requires = get_requirements('requirements.txt')
)
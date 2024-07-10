from setuptools import find_packages, setup


setup(
    name='artifactory-vk',
    version='0.0.3',
    python_requires='>=3.12',
    packages=find_packages(),
    install_requires=[
        'pydantic~=2.8.2',
        'requests~=2.32.3',
        'tuspy~=1.0.3',
    ],
)

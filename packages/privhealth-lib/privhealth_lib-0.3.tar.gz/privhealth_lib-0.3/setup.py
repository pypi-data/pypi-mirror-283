from setuptools import setup, find_packages

setup(
    name='privhealth_lib',
    version='0.3',
    packages=find_packages(),
    description='PrivHealth Library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='LASID Team',
    #author_email='joaofelipe.amorim@aluno.uece.br',
    url='https://github.com/macc-uece/privhealth-lib',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
    install_requires=[
        # KeyCloak
        'fastapi_keycloak',
        'Pyjwt',
        'requests',
        'starlette',
        # Open Clean
        "openclean",
        "pandas",
        'numpy'
    ],
)
from setuptools import setup, find_packages

setup(
    name='hosttimer1py',  # Nome único do projeto
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'colorama',
        # Adicione outras dependências que você precisar
    ],
    author='bruno',
    author_email='miguel100eduardoluiz@gmail.com',
    description='Uma biblioteca para estilizar interfaces e texto em Python, tornando-os mais bonitos e atraentes',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/seunome/hosttimer1py',  # Atualize com o URL correto do seu projeto
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: User Interfaces',
    ],
    python_requires='>=3.6',
)

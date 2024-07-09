from setuptools import setup, find_packages

setup(
    name='p8xxpy',  # Nome único do projeto
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Adicione outras dependências que você precisar, por exemplo:
        # 'tkinter', 'PyQt5'
    ],
    author='bruno',
    author_email='miguel100eduardoluiz@gmail.com',
    description='Uma biblioteca para estilizar interfaces gráficas em Python, tornando-as mais bonitas e atraentes',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/seunome/p8xxpy',  # Atualize com o URL correto do seu projeto
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

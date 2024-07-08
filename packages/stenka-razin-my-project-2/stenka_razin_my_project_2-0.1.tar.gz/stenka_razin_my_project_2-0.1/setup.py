# setup.py : in questo file andiamo a configurare i dettagli di distribuzione di un progetto.
# Viene eseguito quando esegui comandi come: 

# 1. python setup.py install, 
# 2. python setup.py sdist, 
# 3. python setup.py bdist_wheel.


from setuptools import setup, find_packages

setup(
    name='stenka_razin_my_project_2',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    author='Stenka Razin',
    author_email='stenka_razin1234@mailinator.com',
    description='Un esempio di progetto con namespace',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/stenka_razin/my_project_2',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

# find_packages(): Viene chiamato all'interno di setup.py per trovare automaticamente tutti i pacchetti da 
# includere nella distribuzione. Questo avviene quando setup.py viene eseguito. Cosa fa? 

# 1.    Identifica i Pacchetti: Rileva le directory che contengono un file __init__.py e le considera pacchetti.
#       Lo fa ricorsivamente a partire da dove abbiamo collocato setup.py
#  
# 2.    Ritorna una Lista: Restituisce una lista di pacchetti trovati, che viene poi utilizzata nell'argomento 
#       packages di setup().



# FUG HV Power Supply

#### Interface to the FUG HV Power Supply source

## Clone repository
```
cd <path-to-directory>
git clone git@gitlab.com:pass-testing-solutions/fug-power-supply.git
cd fug-power-supply/
git pull origin main
git checkout -b <your-new-branch>  # Please follow the branch naming convention as mentioned in the coding guidelines
```
## Virtual environment on MacOS

### 1. Virtualenvwrapper
You can install virtualenv and virtualenvwrapper with:
```
pip3 install virtualenv
pip3 install virtualenvwrapper
mkdir ~/.virtualenvs
# Might need to query where the virtualenv and virtualenvwrapper.sh are
which virtualenv
which virtualenvwrapper.sh
which python3
```
Add these lines in the ~/.zshrc file 
````
# Setting PATH for Python 3 installed by brew
export PATH=<path-to-your-python3>:$PATH

# Configuration for virtualenv
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=<path-to-your-python3>
export VIRTUALENVWRAPPER_VIRTUALENV=<path-to-your-virtualenv>
source <path-to-your-virtualenvwrapper.sh>

source $ZSH/oh-my-zsh.sh
````
Make sure to save these changes in your file and close your terminal for them to take effect.
Now you can create a virtual environment by simply typing:
```
mkvirtualenv <name-of-your-virtual-env>
cd <your-git-repository>
workon <name-of-your-virtual-env>
deactivate <name-of-your-virtual-env>
```
To add the correct interpreter for your repository on PyCharm:
```
- PyCharm IDE > Preferences > Project > Python Interpreter
- Select the 'Add' button for interpreters
- Choose the 'Existing environments' in 'Virtualenv'
- Add the python3 file from /bin/ of your venv folder
E.g. - .virtualenvs/demo_repo_venv/bin/python3
```
After setting up the venv for the repo please install all the 
requirements and allow some time for the IDE to do indexing. If your repository has a requirements.txt: 
```
pip3 install -r requirements.txt
```

### 2. Pipenv
Install pipenv
```
pip3 install pipenv 
# or
brew install pipenv

pipenv shell         # will create a virtualenv for the project
pipenv install       # will install dependencies for the repo from the Pipfile and Pipfile.lock

# Install any further packages in this environment as

pipenv install rich  # rich is a python library to nicely print on terminal
```
Your pipenv environment will be in the ~./virtualenvs folder.
Make sure to add the interpreter on your IDE if not automatically added by navigating to the virtualenv folder for your repo and selecting the correct python3 file from /bin/.

***

## Maintainers
Maintainers: @julianpass and @shuparnadeb_pts

echo "The current python versions and environments:"
pyenv versions
ENV_STEM='venv_'
echo "Please enter a name to give your environment. The name should not have spaces"
read ENV_NAME
ENV_NAME="$ENV_STEM$ENV_NAME"
echo "An environment with the name: $ENV_NAME will be created using pyenv"
echo "What version of Python should be used in the environment?"
read PY_VER
pyenv virtualenv $PY_VER $ENV_NAME
echo "The python versions and environments are now:"
pyenv versions
pyenv local $ENV_NAME
echo 'Virtual environment activated'
python -m ensurepip --upgrade
python -m pip install --upgrade pip
ls
pip list
pip install -r requirements.txt --no-cache-dir
echo 'Packages installed'
pip list
code .
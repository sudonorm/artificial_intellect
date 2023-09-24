echo "What's your username? "
read USER_NAME
ls
rm .python-version
ls
pyenv versions
echo "Please enter the name of your environment from the list above"
read ENV_NAME
cd /Users/$USER_NAME/.pyenv/versions
rm -r $ENV_NAME
pyenv versions
echo "What version of Python was used in the environment?"
read PY_VER
cd /Users/$USER_NAME/.pyenv/versions/$PY_VER/envs
rm -r $ENV_NAME
echo "Clean up done!"
echo -e $PWD

echo -e $USER

echo -e $SHELL

echo -e '\e[1m\e[34mActivate virtual environment...\e[0m\n'

. ~/apps/twitter2telegram/venv/bin/activate

echo $VIRTUAL_ENV

echo -e '\e[1m\e[34mStarting app...\e[0m\n'

python ~/apps/twitter2telegram/main.py

echo -e '\e[1m\e[34mA\Deactivate virtual environment...\e[0m\n'

deactivate

echo $VIRTUAL_ENV

echo -e '\e[1m\e[34mDone\e[0m\n'

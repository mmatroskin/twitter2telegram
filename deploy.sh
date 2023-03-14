echo -e $PWD

echo -e '\e[1m\e[34mEntering into app directory...\e[0m\n'

cd ~/apps/twitter2telegram

echo -e $PWD

echo -e '\e[1m\e[34mStopping processes...\e[0m\n'

pids=$(ps axu |grep python | grep ~/apps/twitter2telegram | awk {'print $2'})

for pid in $pids
do
    kill -9 $pid
done

echo -e '\e[1m\e[34mRemove existing virtual environment...\e[0m\n'

rm -r ~/apps/twitter2telegram/venv

echo -e '\e[1m\e[34mCloning from source...\e[0m\n'

git checkout release

git pull origin release

echo -e '\e[1m\e[34mActivate virtual environment...\e[0m\n'

python3 -m venv ~/apps/twitter2telegram/venv

. ~/apps/twitter2telegram/venv/bin/activate

echo $VIRTUAL_ENV

echo -e '\e[1m\e[34mInstalling requirements...\e[0m\n'

pip install -r ~/apps/twitter2telegram/requirements.txt

echo -e '\e[1m\e[34mA\Deactivate virtual environment...\e[0m\n'

deactivate

echo $VIRTUAL_ENV

echo -e '\e[1m\e[34mStarting app script...\e[0m\n'

~/apps/twitter2telegram/start.sh > ~/apps/twitter2telegram/nohup.out &

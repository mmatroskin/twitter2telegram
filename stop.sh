echo -e $PWD

echo -e $USER

echo -e $SHELL

echo -e '\e[1m\e[34mStopping processes...\e[0m\n'

pids=$(ps axu |grep python | grep ~/apps/twitter2telegram | awk {'print $2'})

for pid in $pids
do
    kill -9 $pid
done

echo -e '\e[1m\e[34mProcesses stopped\e[0m\n'

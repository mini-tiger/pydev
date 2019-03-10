#!/bin/bash
kill_agent() {
agent_pid=`ps -eo pid,command|grep -v grep|grep agent|grep cfg|awk -F " " '{print $1}'`
kill -9 $agent_pid
}

# kill old agent
kill_agent


tar_filename="agent*"
workdir="/tmp/install_agent"
bin_name="falcon"
agent_name="agent"
install_dir="/home/work/${bin_name}"
if [ -d $install_dir ]; then
	rm -rf $install_dir &> /dev/null
fi

mkdir -p $install_dir

pushd $install_dir &> /dev/null
cp ${workdir}/${tar_filename} .
tar xf $tar_filename
sleep 1
# run agent
${install_dir}/${bin_name} start ${agent_name} &> /dev/null

# check agent
sleep 3
num=`${install_dir}/${bin_name} check ${agent_name}|grep -c -i up`
if [ $num -eq 1 ]; then
	echo 0
else
	echo 1
fi



#! /bin/bash/env bash
echo $1
IP=10.2.20.91
echo $IP
cd ~/.ssh
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/capstone
ssh-copy-id -i capstone.pub $1@$IP

ssh -XY $1@$IP 


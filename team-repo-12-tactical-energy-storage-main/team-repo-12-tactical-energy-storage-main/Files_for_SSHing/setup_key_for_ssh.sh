#! /bin/bash/env bash
set "IP=10.2.20.91"
mkdir ~/.ssh
cd ~/.ssh
echo PLEASE NAME YOUR KEY "capstone" PLEASE OR ELSE EVERYTHING WILL BREAK
ssh-keygen
eval "$(ssh-agent -s)"
echo What did you save your key as?
read key_name
ssh-add ~/.ssh/$key_name
ssh-copy-id -i $key_name.pub $1@$IP

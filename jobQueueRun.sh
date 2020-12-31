#!/bin/bash
oldDir=$(pwd)

#Get script dir
scriptSrc=$(dirname "${BASH_SOURCE[0]}")
cd $scriptSrc

source $scriptSrc/secretkey.sh
python3 jobQueueRun.py

cd $oldDir
#!/usr/bin/env python3

import collections
import string
import platform
import subprocess
import re
import os.path
import datetime
import json
import requests
import argparse

from slackUtils import *

def main():
    #Open Jobs to run
    jobFile = open('jobQueue.txt', 'a+')
    jobs = []
    for line in jobFile:
        jobs.append(line.strip())

    if not jobs:
        print('No Jobs Pending to Run')
        jobFile.close()
        return

    cmd = ''

    while jobs or cmd:
        #Ignore empty lines
        if not jobs[0]:
            jobs = jobs[1:]
        else:
            cmd = jobs[0]

    hostname = platform.node()

    cmd = jobs[0]

    #From https://unix.stackexchange.com/questions/396630/the-proper-way-to-test-if-a-service-is-running-in-a-script
    systemctlCode = subprocess.call('systemctl is-active --quiet setupCPUForDSP.service', shell=True, executable='/bin/bash')

    if systemctlCode != 0:
        print('Warning! setupCPUForDSP.service did not run!')
        slackStatusPost('Warning! setupCPUForDSP.service did not run on ' + hostname)

    cur_time = datetime.datetime.now()
    print("Starting: {}\n".format(str(cur_time)))
    slackStatusPost('*Job Runner Executing*\nHost: ' + hostname + '\nTime: ' + str(cur_time) + '\nCMD: ' + cmd)

    print('\nRunning: {}\n'.format(cmd))

    rtnCode = subprocess.call(cmd, shell=True, executable='/bin/bash')

    cur_time = datetime.datetime.now()
    if rtnCode == 0:
        print("\nJob Finished: {}\n".format(str(cur_time)))
    else:
        print("\nJob Errored: {}\n".format(str(cur_time)))

    if rtnCode == 0:
        slackStatusPost('*Job Finished :white_check_mark:*\nHost: ' + hostname + '\n' + 'Time: ' + str(cur_time))
    else:
        slackStatusPost('*Job Errored :x:*\nHost: ' + hostname + '\n' + 'Time: ' + str(cur_time))

    #Remove executed job from list
    jobs = jobs[1:]

    nextJob = ''

    while jobs or nextJob:
        #Ignore empty lines
        if not jobs[0]:
            jobs = jobs[1:]
        else:
            nextJob = jobs[0]
    
    #Write new jobs to list using trick from https://stackoverflow.com/questions/6648493/how-to-open-a-file-for-both-reading-and-writing
    jobFile.seek(0)
    for job in jobs:
        jobFile.write(job + '\n')
    jobFile.trunkate()
    jobFile.close()

    #Reboot if there is another job
    if jobs:
        print('\nNext Job: ' + nextJob[0])
        slackStatusPost('*Job Runner Next Job*\nHost: ' + hostname + '\nCMD: ' + nextJob[0] + '\nRebooting ...')
        subprocess.call('reboot', shell=True, executable='/bin/bash')

if __name__ == "__main__":
    main()
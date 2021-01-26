# jobQueue
A service for executing jobs where a reboot is required between them

NOTE: This service should be run as a *unprivalaged* user as it stores commands to be run in a file which can be edited

Commands to run must be contained in single lines.  Commands will be executed sequentially starting from the top.  Commands will be removed from the file as they are run

Make sure to change the user to run these commands as.  A privalaged user will be required to enable the service.

The user the commands are being run as need to be allowed to reboot the system.  See https://unix.stackexchange.com/questions/85663/poweroff-or-reboot-as-normal-user for an example of how to do that.  Using visudo with -f to specify a file in /etc/sudoers.d may be helpful.  Note that because of this, the job scheduler can create problems in multi-user environments.

Example (replace `username` with the desired username):
```
sudo visudo -f /etc/sudoers.d/usernameReboot
```

Set the following in the file:
```
## username is allowed to execute reboot without a password
username ALL=NOPASSWD: /sbin/reboot
```

# jobQueue
A service for executing jobs where a reboot is required between them

NOTE: This service should be run as a *unprivalaged* user as it stores commands to be run in a file which can be edited

Commands to run must be contained in single lines.  Commands will be executed sequentially starting from the top.  Commands will be removed from the file as they are run

Make sure to change the user to run these commands as.  A privalaged user will be required to enable the service.
